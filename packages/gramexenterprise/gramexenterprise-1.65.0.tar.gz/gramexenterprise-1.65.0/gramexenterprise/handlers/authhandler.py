from __future__ import unicode_literals
import os
import csv
import json
import time
import uuid
import base64
import string
import tornado.escape
import tornado.httpclient
from random import choice
from socket import gethostname
from cachetools import TTLCache
from tornado.auth import FacebookGraphMixin, TwitterMixin, OAuth2Mixin
from tornado.gen import coroutine, Return
from tornado.web import HTTPError
from urllib.parse import urlencode, parse_qs, urlsplit
from orderedattrdict import AttrDict
import gramex
import gramex.cache
from gramex.http import UNAUTHORIZED, BAD_REQUEST, INTERNAL_SERVER_ERROR
from gramex.config import app_log, str_utf8, merge
from gramex.transforms import build_transform
from gramex.handlers.authhandler import AuthHandler, SimpleAuth, _auth_template

_folder = os.path.dirname(os.path.abspath(__file__))
_forgot_template = os.path.join(_folder, 'forgot.template.html')
_signup_template = os.path.join(_folder, 'signup.template.html')

# Python 3 csv.writer.writerow writes as str(), which is unicode in Py3.
# Python 2 csv.writer.writerow writes as str(), which is bytes in Py2.
# So we use cStringIO.StringIO in Py2 (which handles bytes).
# Since Py3 doesn't have cStringIO, we use io.StringIO (which handles unicode)
try:
    import cStringIO
    StringIOClass = cStringIO.StringIO
except ImportError:
    import io
    StringIOClass = io.StringIO


class OAuth2(AuthHandler, OAuth2Mixin):
    '''
    The OAuth2 handler lets users log into any OAuth2 service. It accepts this
    configuration:

    :arg str client_id: Create an app with the OAuth2 provider to get this ID
    :arg str client_secret: Create an app with the OAuth2 provider to get this ID
    :arg dict authorize: Authorization endpoint configuration:
        - url: Authorization endpoint URL
        - scope: an optional a list of string scopes
        - extra_params: an optional dict of URL query params passed
    :arg dict access_token: Access token endpoint configuration
        - url: Access token endpoint URL
        - session_key: optional key in session to store access token information. \
            default: `access_token`
        - headers: optional dict containing HTTP headers to pass to access token URL. \
            By default, sets `User-Agent` to `Gramex/<version>`.
        - body: optional dict containing arguments to pass to access token URL \
            (e.g. `{grant_type: authorization_code}`)
    :arg dict user_info: Optional user information API endpoint
        - url: API endpoint to fetch URL
        - headers: optional dict containing HTTP headers to pass to user info URL. \
            e.g. `Authorization: 'Bearer {access_token}'`. \
            Default: `{User-Agent: Gramex/<version>}`
        - method: HTTP method to use (default: `GET`)
        - body: optional dict containing POST arguments to pass to user info URL
        - user_id: Attribute in the returned user object that holds the user ID. \
          This is used to identify the user uniquely. default: `id`
    :arg str user_key: optional key in session to store user information.
        default: `user`
    '''
    AUTHORIZE_DEFAULTS = {
        'scope': [],
        'extra_params': {},
        'response_type': 'code',
    }
    ACCESS_TOKEN_DEFAULTS = {
        'headers': {
            'User-Agent': 'Gramex/' + gramex.__version__
        },
        'body': {
            'redirect_uri': '{redirect_uri}',
            'code': '{code}',
            'client_id': '{client_id}',
            'client_secret': '{client_secret}',
        },
        'session_key': 'access_token'
    }
    USER_INFO_DEFAULTS = {
        'headers': {
            'User-Agent': 'Gramex/' + gramex.__version__
        },
        'user_id': 'id'
    }

    @classmethod
    def setup(cls, client_id, client_secret, authorize, access_token,
              user_info=None, **kwargs):
        super(OAuth2, cls).setup(**kwargs)
        cls.client_id = client_id
        cls.client_secret = client_secret

        cls._OAUTH_AUTHORIZE_URL = authorize.url
        cls._OAUTH_ACCESS_TOKEN_URL = access_token.url
        cls.authorize = merge(authorize, cls.AUTHORIZE_DEFAULTS, mode='setdefault')
        cls.access_token = merge(access_token, cls.ACCESS_TOKEN_DEFAULTS, mode='setdefault')
        cls.user_info = merge({} if user_info is None else user_info,
                              cls.USER_INFO_DEFAULTS, mode='setdefault')

    @coroutine
    def get(self):
        code = self.get_arg('code', '')
        # Step 1: user visits this page and is redirected to the OAuth provider
        if not code:
            self.save_redirect_page()
            yield self.authorize_redirect(
                redirect_uri=self.xredirect_uri,
                client_id=self.client_id,
                client_secret=self.client_secret,
                extra_params=self.authorize.extra_params,
                scope=self.authorize.scope,
                response_type=self.authorize.response_type,
            )
        # Step 2: after logging in, user is redirected back here to continue
        else:
            # Step 2a: Exchange code for access token
            http = self.get_auth_http_client()
            params = {
                'name': self.name,
                "redirect_uri": self.xredirect_uri,
                "code": code,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            }
            response = yield http.fetch(
                self._OAUTH_ACCESS_TOKEN_URL, method='POST', raise_error=False,
                **self._request_conf(self.access_token, params))
            self.validate(response)
            # Parse the response based on the HTTP Content Type
            body = tornado.escape.native_str(response.body)
            mime_type = response.headers['Content-Type']
            if mime_type.startswith('application/x-www-form-urlencoded'):
                args = parse_qs(body)
                args = {key: value[-1] for key, value in args.items()}
            elif mime_type.startswith('application/json'):
                args = json.loads(body)
            else:
                self.validate(AttrDict(
                    error=True, code=BAD_REQUEST, reason='Invalid access token',
                    body=('Access token response not form-encoded nor JSON:\n\n' +
                          'Content-Type: %s\n\n%s') % (mime_type, body),
                    headers={}))
                raise Return()
            # Save the returned session info in a config-specified session key.
            # This defaults to 'access_token'
            params.update(args)
            session_key = self.access_token['session_key']
            self.session[session_key] = args

            # Step 2b: Use access token to fetch the user info
            if 'url' in self.user_info:
                response = yield http.fetch(
                    self.user_info['url'].format(**params),
                    raise_error=False,
                    **self._request_conf(self.user_info, params))
                self.validate(response)
                try:
                    user = json.loads(response.body)
                except Exception:
                    self.validate(AttrDict(
                        error=True, code=BAD_REQUEST, reason='Invalid user JSON',
                        body='User info not JSON:\n\n%s' % response.body,
                        headers={}))
                else:
                    user_id = self.user_info['user_id']
                    yield self.set_user(user, id=user_id)
            self.redirect_next()

    def _request_conf(self, conf, params):
        result = {}
        if 'method' in conf:
            result['method'] = conf['method']
        if 'headers' in conf:
            result['headers'] = {
                key: val.format(**params) for key, val in conf['headers'].items()
            }
        if 'body' in conf:
            result['body'] = urlencode({
                key: val.format(**params) for key, val in conf['body'].items()
            })
        return result

    def get_auth_http_client(self):
        """Returns the `.AsyncHTTPClient` instance to be used for auth requests.

        May be overridden by subclasses to use an HTTP client other than
        the default.
        """
        return tornado.httpclient.AsyncHTTPClient()

    def validate(self, response):
        if response.error:
            app_log.error(response.body)
            self.set_status(response.code, reason=response.reason)
            mime_type = response.headers.get('Content-Type', 'text/plain')
            self.set_header('Content-Type', mime_type)
            self.write(response.body)
            raise Return()


class FacebookAuth(AuthHandler, FacebookGraphMixin):
    @coroutine
    def get(self):
        code = self.get_arg('code', '')
        if code:
            user = yield self.get_authenticated_user(
                redirect_uri=self.xredirect_uri,
                client_id=self.kwargs['key'],
                client_secret=self.kwargs['secret'],
                code=code)
            yield self.set_user(user, id='id')
            self.redirect_next()
        else:
            self.save_redirect_page()
            yield self.authorize_redirect(
                redirect_uri=self.xredirect_uri,
                client_id=self.kwargs['key'],
                extra_params={
                    'fields': ','.join(self.kwargs.get('fields', [
                        'name', 'email', 'first_name', 'last_name', 'gender',
                        'link', 'username', 'locale', 'timezone',
                    ])),
                })


class TwitterAuth(AuthHandler, TwitterMixin):
    @coroutine
    def get(self):
        oauth_token = self.get_arg('oauth_token', '')
        if oauth_token:
            user = yield self.get_authenticated_user()
            yield self.set_user(user, id='username')
            self.redirect_next()
        else:
            self.save_redirect_page()
            yield self.authenticate_redirect(callback_uri=self.xredirect_uri)

    def _oauth_consumer_token(self):
        return dict(key=self.kwargs['key'], secret=self.kwargs['secret'])


class SAMLAuth(AuthHandler):
    '''
    SAML Authentication.

    Reference: https://github.com/onelogin/python3-saml

    Sample configuration::

        kwargs:
          sp_domain: myapp.gramener.com         # Domain where your app is hosted
          request_uri: ...                      # Path to your app
          https: true                           # Use HTTPS scheme for your app
          custom_base_path: $YAMLPATH/.saml/    # Path to settings.json & certs/
          lowercase_encoding: True              # True for ADFS
    '''
    @classmethod
    def setup(cls, sp_domain, custom_base_path, https, lowercase_encoding=True,
              request_uri='', **kwargs):
        super(SAMLAuth, cls).setup(**kwargs)
        cls.sp_domain = sp_domain
        cls.custom_base_path = custom_base_path
        cls.https = 'on' if https is True else 'off'
        cls.default_params = {
            'lowercase_urlencoding': lowercase_encoding,
            'request_uri': request_uri,
        }

    @coroutine
    def get(self):
        '''Process sso request and metadata request.'''
        auth = self.initiate_saml_login()
        # SAML server requests metadata at https://<sp_domain>/<request_uri>?metadata
        if 'metadata' in self.args:
            settings = auth.get_settings()
            metadata = settings.get_sp_metadata()
            errors = settings.validate_metadata(metadata)
            if errors:
                app_log.error('%s: SAML metadata errors: %s', self.name, errors)
                raise HTTPError(INTERNAL_SERVER_ERROR, reason='Errors in metadata')
            self.set_header('Content-Type', 'text/xml')
            self.write(metadata)
        # Logout
        elif 'sls' in self.args:
            raise NotImplementedError()
        # Login redirect
        else:
            self.save_redirect_page()
            self.redirect(auth.login())

    @coroutine
    def post(self):
        '''Validate and authenticate user based upon SAML response.'''
        auth = self.initiate_saml_login()

        # Process IDP response, and create session.
        if 'acs' in self.args:
            auth.process_response()
            errors = auth.get_errors()
            if errors:
                app_log.error('%s: SAML ACS error: %s', self.name, errors)
                raise Return()
            yield self.set_user({
                'samlUserdata': auth.get_attributes(),
                'samlNameId': auth.get_nameid(),
                'samlSessionIndex': auth.get_session_index(),
            }, id='samlNameId')
            self.redirect_next()

    def initiate_saml_login(self):
        # TODO: onelogin is not part of requirements.txt. Add it
        from onelogin.saml2.auth import OneLogin_Saml2_Auth
        req = merge({
            'http_host': self.sp_domain,
            'https': self.https,
            'script_name': urlsplit(self.xredirect_uri).path,
            'get_data': self.request.query_arguments,
            'post_data': {k: v[0] for k, v in self.args.items()}
        }, self.default_params, mode='setdefault')
        return OneLogin_Saml2_Auth(req, custom_base_path=self.custom_base_path)


class LDAPAuth(AuthHandler):
    @classmethod
    def setup(cls, **kwargs):
        super(LDAPAuth, cls).setup(**kwargs)
        cls.template = kwargs.get('template', _auth_template)

    def get(self):
        self.save_redirect_page()
        self.render_template(self.template, error=None)

    errors = {
        'bind': 'Unable to log in bind.user at {host}',
        'conn': 'Connection error at {host}',
        'auth': 'Could not log in user',
        'search': 'Cannot get attributes for user on {host}',
    }

    def report_error(self, code, exc_info=False):
        error = self.errors[code].format(host=self.kwargs.host, args=self.args)
        app_log.error('LDAP: ' + error, exc_info=exc_info)
        self.log_user_event(event='fail')
        self.set_status(UNAUTHORIZED)
        self.set_header('Auth-Error', code)
        self.render_template(self.template, error={'code': code, 'error': error})
        raise Return()

    @coroutine
    def bind(self, server, user, password, error):
        import ldap3
        conn = ldap3.Connection(server, user, password)
        try:
            result = yield gramex.service.threadpool.submit(conn.bind)
            if not result:
                self.report_error(error, exc_info=False)
                conn = None
            raise Return(conn)
        except ldap3.core.exceptions.LDAPException:
            self.report_error('conn', exc_info=True)

    @coroutine
    def post(self):
        import ldap3
        kwargs = self.kwargs
        # First, bind the server with the provided user ID and password.
        q = {key: vals[0] for key, vals in self.args.items()}
        server = ldap3.Server(kwargs.host, kwargs.get('port'), kwargs.get('use_ssl', True))
        cred = kwargs.bind if 'bind' in kwargs else kwargs
        user, password = cred.user.format(**q), cred.password.format(**q)

        error_code = 'bind' if 'bind' in kwargs else 'auth'
        conn = yield self.bind(server, user, password, error_code)
        if not conn:
            return

        # search: for user attributes if specified
        if 'search' in kwargs:
            search_base = kwargs.search.base.format(**q)
            search_filter = kwargs.search.filter.format(**q)
            search_user = kwargs.search.get('user', '{dn}')
            try:
                result = conn.search(search_base, search_filter, attributes=ldap3.ALL_ATTRIBUTES)
                if not result or not len(conn.entries):
                    self.report_error('search', exc_info=False)
                user = json.loads(conn.entries[0].entry_to_json())
                attrs = user.get('attributes', {})
                attrs['dn'] = user.get('dn', '')
                user['user'] = search_user.format(**attrs)
            except ldap3.core.exceptions.LDAPException:
                self.report_error('conn', exc_info=True)

            if 'bind' in kwargs:
                # REBIND: ensure that the password matches
                validate_user = yield self.bind(
                    server, user['dn'], kwargs.search.password.format(**q), 'auth')
                if not validate_user:
                    return
        else:
            user = {'user': user}

        yield self.set_user(user, id='user')
        self.redirect_next()


class DBAuth(SimpleAuth):
    '''
    The configuration (``kwargs``) for DBAuth looks like this::

        template: $YAMLPATH/auth.template.html  # Render the login form template
        url: sqlite:///$YAMLPATH/auth.db    # List of users is in this sqlalchemy URL or file
        table: users                        # ... and this table (if url is a database)
        prepare: some_function(args)
        user:
            column: user                    # The users.user column is matched with
            arg: user                       # ... the ?user= argument from the form
        password:
            column: password                # The users.password column is matched with
            arg: password                   # ... the ?password= argument from the form
                                            # Optional encryption for password
            function: passlib.hash.sha256_crypt.encrypt(content, salt='secret-key')
            hash: true                      # hash password on browser in template
        forgot:
            key: forgot                     # ?forgot= is used as the forgot password parameter
            arg: email                      # ?email= is used as the email parameter
            template: $YAMLPATH/forgot.html # Forgot password template
            minutes_to_expiry: 15           # Minutes after which the link will expire
            email_column: user              # Database table column with email ID
            email_from: email-service       # Name of the email service to use for sending emails
            email_as: email-id              # Name of the person sending email (optional)
            email_text: 'This email is for {user}, {email}'
        # signup: true                      # Enables signup using ?signup
        signup:
            key: signup                     # ?signup= is used as the signup parameter
            template: $YAMLPATH/signup.html # Signup template
            columns:                        # Mapping of URL query parameters to database columns
                name: user_name             # ?name= is saved in the user_name column
                gender: user_gender         # ?gender= is saved in the user_gender column
                                            # Other than email, all other columns are ignored
            validate: app.validate(args)    # Optional validation method is passed handler.args
                                            # This may raise an Exception or return False to stop.

    The login flow is as follows:

    1. User visits the DBAuth page => shows template (with the user name and password inputs)
    2. User enters user name and password, and submits. Browser redirects with a POST request
    3. Application checks username and password. On match, redirects.
    4. On any error, shows template (with error)

    The forgot password flow is as follows:

    1. User visits ``GET ?forgot`` => shows forgot password template (with the user name)
    2. User submits user name. Browser redirects to ``POST ?forgot&user=...``
    3. Application generates a new password link (valid for ``minutes_to_expiry`` minutes).
    4. Application emails new password link to the email ID associated with user
    5. User is sent to ``?forgot=<token>`` => shows forgot password template (with password)
    6. User submits new password (entered twice) => ``POST ?forgot=<token>&password=...``
    7. Application checks if token is valid. If yes, sets associated user's password and redirects
    8. On any error, shows forgot password template (with error)

    The signup password flow is as follows:

    1. User visits ``GET ?signup`` => show signup template
    2. User submits email and other information. Browser redirects to ``POST ?signup&...``
    3. Application checks if email exists => suggest password recovery
    4. Application validates fields using validation function if it exists
    5. Else, Application adds the following fields to the database:
        - fields mentioned in ``signup.columns:``
        - email from ``forgot.arg:`` into ``forgot.email_column:``
        - random password using into ``password.column`` - no encryption
    6. Application says "I've sent an email to reset password" (and does so)
    '''
    # Number of characters in password
    PASSWORD_LENGTH = 20
    PASSWORD_CHARS = string.digits + string.ascii_letters

    @classmethod
    def setup(cls, url, user, password, forgot=None, signup=None, **kwargs):
        super(DBAuth, cls).setup(user=user, password=password, **kwargs)
        # Create a private copy, without overridding parent's special_keys
        cls.special_keys = list(cls.special_keys) + [
            'template', 'delay', 'prepare', 'action', 'session_expiry', 'session_inactive']
        cls.clear_special_keys(kwargs)
        cls.forgot, cls.signup = forgot, signup
        cls.query_kwargs = {'url': url}
        cls.query_kwargs.update(kwargs)
        if isinstance(cls.forgot, AttrDict):
            default_minutes_to_expiry = 15
            cls.forgot.setdefault('template', _forgot_template)
            cls.forgot.setdefault('key', 'forgot')
            cls.forgot.setdefault('arg', 'email')
            cls.forgot.setdefault('email_column', 'email')
            cls.forgot.setdefault('minutes_to_expiry', default_minutes_to_expiry)
            cls.forgot.setdefault('email_subject', 'Password reset')
            cls.forgot.setdefault('email_as', None)
            cls.forgot.setdefault(
                'email_text', 'Visit {reset_url} to reset password for user {%s} ({%s})' % (
                    cls.user.get('column', 'user'), cls.forgot['email_column']
                ))
            setattr(cls, cls.forgot.get('key'), cls.forgot)
            cls.recover = OTP()
            # TODO: default email_from to the first available email service
        if cls.signup is True:
            cls.signup = AttrDict()
        if isinstance(cls.signup, AttrDict):
            if not cls.forgot:
                app_log.error('url:%s.signup requires .forgot.email_column', cls.name)
            cls.signup.setdefault('template', _signup_template)
            cls.signup.setdefault('key', 'signup')
            cls.signup.setdefault('columns', {})
            if 'validate' in cls.signup:
                validate = cls.signup.validate
                if isinstance(validate, (str, bytes)):
                    validate = {'function': validate}
                cls.signup.validate = build_transform(
                    validate, vars=AttrDict(handler=None, args=None),
                    filename='url:%s:signup.validate' % cls.name, iter=False)
            setattr(cls, cls.signup.get('key'), cls.signup)
        cls.encrypt = []
        if 'function' in password:
            cls.encrypt.append(build_transform(
                password, vars=AttrDict(handler=None, content=None),
                filename='url:%s:encrypt' % (cls.name)))

    def report_error(self, status, event, error, data=None):
        '''
        Set the HTTP status. Log user event. Return an error object.
        '''
        self.set_status(status, reason=error)
        self.log_user_event(event='fail')
        return {'code': 'auth', 'error': data or error}

    def get(self):
        self.save_redirect_page()
        template = self.template
        if self.forgot and self.forgot.key in self.args:
            template = self.forgot.template
        elif self.signup and self.signup.key in self.args:
            template = self.signup.template
        self.render_template(template, error=None)

    @coroutine
    def post(self):
        if self.forgot and self.forgot.key in self.args:
            yield self.forgot_password()
        elif self.signup and self.signup.key in self.args:
            yield self.signup_user()
        else:
            yield self.login()

    @coroutine
    def login(self):
        user = self.get_arg(self.user.arg, None)
        password = self.get_arg(self.password.arg, None)

        if not user or not password:
            # Note: all users who log in without a password will be treated as the same
            yield self.fail_user({'user': user}, 'user')
            self.render_template(self.template, error=self.report_error(
                BAD_REQUEST, 'fail', 'User name or password is empty'))
            raise Return()

        for encrypt in self.encrypt:
            for result in encrypt(handler=self, content=password):
                password = result

        users = yield gramex.service.threadpool.submit(gramex.data.filter, args={
            self.user.column: [user],
            self.password.column: [password],
        }, **self.query_kwargs)
        if len(users) > 0:
            # Delete password from user object before storing it in the session
            del users[self.password.column]
            yield self.set_user(users.iloc[0].to_dict(), id=self.user.column)
            self.redirect_next()
        else:
            yield self.fail_user({'user': user}, 'user')
            self.render_template(self.template, error=self.report_error(
                UNAUTHORIZED, 'fail', 'Cannot log in'))

    @coroutine
    def forgot_password(self):
        action = (list(self.args) or ['forgot'])[0]
        forgot_config = merge(getattr(self, action), self.forgot, 'setdefault')
        template = forgot_config.template
        error = {}
        forgot_key = self.get_arg(forgot_config.key, None)

        # Step 1: user submits their user ID / email via POST ?forgot&user=...
        if not forgot_key:
            # Get the user based on the user ID or email ID (in that priority)
            forgot_user = self.get_arg(self.user.arg, None)
            forgot_email = self.get_arg(forgot_config.arg, None)
            if forgot_user:
                query = {self.user.column: [forgot_user]}
            elif forgot_email:
                query = {forgot_config.email_column: [forgot_email]}
            else:
                self.render_template(template, error=self.report_error(
                    BAD_REQUEST, 'forgot-invalid-user', 'user/email cannot be empty'))
                raise Return()
            users = yield gramex.service.threadpool.submit(
                gramex.data.filter, args=query, **self.query_kwargs)
            user = None if len(users) == 0 else users.iloc[0].to_dict()
            email_column = forgot_config.get('email_column', 'email')

            # If a matching user exists in the database
            if user is not None and user[email_column]:
                # generate token and set expiry
                token = yield gramex.service.threadpool.submit(
                    self.recover.token,
                    user=user[self.user.column],
                    email=user[email_column],
                    expire=time.time() + forgot_config.minutes_to_expiry * 60,
                )
                # send password reset mail to user
                mailer = gramex.service.email[forgot_config.email_from]
                reset_url = self.xredirect_uri + '?' + urlencode({self.forgot.key: token})
                kwargs = {
                    'to': user[email_column],
                    'subject': forgot_config.email_subject.format(reset_url=reset_url, **user),
                    'body': forgot_config.email_text.format(reset_url=reset_url, **user),
                }
                if forgot_config.email_as:
                    kwargs['from'] = forgot_config.email_as
                yield gramex.service.threadpool.submit(mailer.mail, **kwargs)
            # If no user matches the user ID or email ID
            else:
                if user is None:
                    msg = 'No user matching %s found' % (forgot_user or forgot_email)
                elif not user[email_column]:
                    msg = 'No email matching %s found' % (forgot_user or forgot_email)
                error = self.report_error(UNAUTHORIZED, 'forgot-nouser', msg)

        # Step 2: User clicks on email, submits new password via POST ?forgot=<token>&password=...
        else:
            row = yield gramex.service.threadpool.submit(self.recover.pop, forgot_key)
            # if system generated token in database
            if row is not None:
                password = self.get_arg(self.password.arg, None)
                if not password:
                    self.render_template(template, error=self.report_error(
                        BAD_REQUEST, 'forgot-invalid-password', 'password cannot be empty'))
                    raise Return()
                for encrypt in self.encrypt:
                    for result in encrypt(handler=self, content=password):
                        password = result
                # Update password in database
                yield gramex.service.threadpool.submit(
                    gramex.data.update, id=[self.user.column], args={
                        self.user.column: [row['user']],
                        self.password.column: [password]
                    }, **self.query_kwargs)
            else:
                error = self.report_error(UNAUTHORIZED, 'forgot-token-invalid', 'Invalid Token')
        self.render_template(template, error=error)

    @coroutine
    def signup_user(self):
        # Checks if email exists => suggest password recovery
        signup_user = self.get_arg(self.user.arg, None)
        if not signup_user:
            self.render_template(self.signup.template, error=self.report_error(
                BAD_REQUEST, 'signup-invalid-user', 'User cannot be empty'))
            raise Return()

        users = yield gramex.service.threadpool.submit(
            gramex.data.filter, args={self.user.column: [signup_user]}, **self.query_kwargs)
        if len(users) > 0:
            self.render_template(self.signup.template, error=self.report_error(
                BAD_REQUEST, 'signup-exists', 'User exists'))
            raise Return()

        # Validates fields using validation function if they exists
        if 'validate' in self.signup:
            validate_error = self.signup.validate(handler=self, args=self.args)
            if validate_error:
                self.render_template(self.signup.template, error=self.report_error(
                    BAD_REQUEST, 'signup-invalid', 'Validation failed', validate_error))
                raise Return()

        # Else, add the following fields to the database:
        #  - fields mentioned in ``signup.columns:``
        #  - email from ``forgot.arg:`` into ``forgot.email_column:``
        #  - password using random 20 char password into ``password.column`` - no encryption
        pwd = ''.join(choice(self.PASSWORD_CHARS) for c in range(self.PASSWORD_LENGTH))   # nosec
        values = {
            self.user.column: [signup_user],
            # TODO: allow admins (maybe users) to enter their own passwords in case of no email
            self.password.column: [pwd],
        }
        for field, column in self.signup.columns.items():
            values[field] = self.args.get(column, [])
        if self.forgot and self.forgot.arg in self.args:
            values[self.forgot.email_column] = self.args.get(self.forgot.arg, [])
        yield gramex.service.threadpool.submit(
            gramex.data.insert, id=[self.user.column], args=values, **self.query_kwargs)

        # Send a password reset link
        yield self.forgot_password()


class IntegratedAuth(AuthHandler):
    @classmethod
    def setup(cls, realm=None, maxsize=1000, ttl=300, **kwargs):
        super(IntegratedAuth, cls).setup(**kwargs)
        cls.realm = realm if realm is not None else gethostname()
        # Security contexts are stored in a dict with the session ID as keys.
        # Only retain the latest contexts, and limit the duration
        cls.csas = TTLCache(maxsize, ttl)

    def negotiate(self, msg=None):
        self.set_status(UNAUTHORIZED)
        self.add_header('WWW-Authenticate',
                        'Negotiate' if msg is None else 'Negotiate ' + msg)

    def unauthorized(self):
        self.log_user_event(event='fail')
        self.set_status(UNAUTHORIZED)
        self.csas.pop(self.session['id'], None)
        self.write('Unauthorized')

    @coroutine
    def get(self):
        try:
            import sspi
            import sspicon
        except ImportError:
            app_log.exception('%s: requires Windows, sspi package', self.name)
            raise
        self.save_redirect_page()

        # Spec: https://tools.ietf.org/html/rfc4559
        challenge = self.request.headers.get('Authorization')
        if not challenge:
            self.negotiate()
            raise Return()

        scheme, auth_data = challenge.split(None, 2)
        if scheme != 'Negotiate':
            app_log.error('%s: unsupported Authorization: %s', self.name, challenge)
            self.unauthorized()
            raise Return()

        # Get the security context
        session_id = self.session['id']
        if session_id not in self.csas:
            realm = self.realm
            spn = 'http/%s' % realm
            self.csas[session_id] = yield gramex.service.threadpool.submit(
                sspi.ServerAuth, "Negotiate", spn=spn)
        csa = self.csas[session_id]

        try:
            err, sec_buffer = yield gramex.service.threadpool.submit(
                csa.authorize, base64.b64decode(auth_data))
        except Exception:
            # The token may be invalid, password may be wrong, or server unavailable
            app_log.exception('%s: authorize() failed on: %s', self.name, auth_data)
            self.unauthorized()
            raise Return()

        # If SEC_I_CONTINUE_NEEDED, send challenge again
        # If err is anything other than zero, we don't know what it is
        if err == sspicon.SEC_I_CONTINUE_NEEDED:
            self.negotiate(base64.b64encode(sec_buffer[0].Buffer))
            raise Return()
        elif err != 0:
            app_log.error('%s: authorize() unknown response: %s', self.name, err)
            self.unauthorized()
            raise Return()

        # The security context contains the user ID. Retrieve it.
        # Split the DOMAIN\username into its parts. Add to the user object
        user_id = yield gramex.service.threadpool.submit(
            csa.ctxt.QueryContextAttributes, sspicon.SECPKG_ATTR_NAMES)
        parts = user_id.split('\\', 2)
        user = {
            'id': user_id,
            'domain': parts[0] if len(parts) > 1 else '',
            'username': parts[-1],
            'realm': self.realm,
        }
        self.csas.pop(session_id, None)

        yield self.set_user(user, 'id')
        self.redirect_next()


class SMSAuth(SimpleAuth):
    '''
    The configuration (kwargs) for SMSAuth looks like this::

        # Required configuration
        service: exotel-sms       # Send messages using this provider
        # Send this string with the %s replaced with the OTP.
        # The string should only contain one %s
        message: 'Your OTP is %s. Visit https://bit.ly/sms2auth'

        # Optional configuration. The values shown below are the defaults
        minutes_to_expiry: 15     # Minutes after which the OTP will expire
        size: 6                   # Number of characters in the OTP
        sender: gramex            # Sender ID. Works in some countries
        template: $YAMLPATH/auth.sms.template.html    # Login template
        user:
            arg: user             # ?user= contains the mobile number
        password:
            arg: password         # ?password= contains the OTP

    The SMSAuth flow is as follows:

    1. User visits ``GET /``. App shows form template asking for phone (``user`` field)
    2. User submits phone number. Browser redirects to ``POST /?user=<phone>``
    3. App generates a new OTP (valid for ``minutes_to_expiry`` minutes).
    4. App SMSs the OTP to the user phone number. On fail, ask for phone again
    5. App shows form template with blank OTP (``password``) field
    6. User submits OTP => ``POST /?user=<phone>&password=<otp>``
    7. App checks if OTP is valid. If yes, logs user in and redirects
    8. On any error, shows form template with error
    '''
    @classmethod
    def setup(cls, service, message, sender='Gramex', size=6, minutes_to_expiry=15, **kwargs):
        super(SMSAuth, cls).setup(**kwargs)
        cls.template = kwargs.get('template', os.path.join(_folder, 'auth.sms.template.html'))
        cls.expire = minutes_to_expiry * 60
        cls.service = service
        cls.message = message
        cls.sender = sender
        cls.recover = OTP(size=size)

    def get(self):
        self.save_redirect_page()
        self.render_template(self.template, phone=None, error=None)

    @coroutine
    def post(self):
        user = self.get_arg(self.user.arg, None)
        password = self.get_arg(self.password.arg, None)
        if password is None:
            expire = time.time() + self.expire
            token = yield gramex.service.threadpool.submit(
                self.recover.token, user=user, email=user, expire=expire)
            notifier = gramex.service.sms[self.service]
            try:
                yield gramex.service.threadpool.submit(
                    notifier.send, to=user, subject=self.message % token, sender=self.sender)
            except Exception as e:
                app_log.exception('%s: cannot send SMS OTP', self.name)
                self.render_template(self.template, phone=user, error='not-sent', msg=e)
            else:
                app_log.debug('%s: sent OTP to %s', self.name, user)
                self.render_template(self.template, phone=user, error=None)
        else:
            row = yield gramex.service.threadpool.submit(self.recover.pop, password)
            if row is not None:
                yield self.set_user({'user': user}, id='user')
                self.redirect_next()
            else:
                self.render_template(self.template, phone=user, error='wrong-pw',
                                     msg='Invalid password')


class EmailAuth(SimpleAuth):
    '''
    The configuration (kwargs) for EmailAuth looks like this::

        # Required configuration
        service: gramex-guide-gmail     # Send messages using this provider
        # Send the strings below as subject and body. You can use variables
        # user=email ID, password=OTP, link=one-time login link
        subject: 'OTP for Gramex'
        body: 'The OTP for {user} is {password}. Visit {link}'

        # Optional configuration. The values shown below are the defaults
        minutes_to_expiry: 15     # Minutes after which the OTP will expire
        size: 6                   # Number of characters in the OTP
        template: auth.email.template.html    # Login template
        user:
            arg: user             # ?user= contains the user email
        password:
            arg: password         # ?password= contains the OTP

    The EmailAuth flow is as follows:

    1. User visits ``/``. App shows form template asking for email (``user`` field)
    2. User submits email. Browser redirects to ``POST /?user=<email>``
    3. App generates a new OTP (valid for ``minutes_to_expiry`` minutes).
    4. App emails the OTP link to the user's email. On fail, ask for email again
    5. If email was sent, app shows a message asking user to check email
    6. User clicks on email and visits link with OTP (``GET /?password=<otp>&next=...``)
    7. App checks if OTP is valid. If yes, logs user in and redirects
    8. On any error, shows form template with error
    '''
    @classmethod
    def setup(cls, service, subject, body, size=6, minutes_to_expiry=15, **kwargs):
        super(EmailAuth, cls).setup(**kwargs)
        cls.template = kwargs.get('template', os.path.join(_folder, 'auth.email.template.html'))
        cls.expire = minutes_to_expiry * 60
        cls.service = service
        cls.subject = subject
        cls.body = body
        cls.recover = OTP(size=size)
        cls.redirect_key = kwargs.get('redirect', {}).get('query', 'next')

    @coroutine
    def get(self):
        self.save_redirect_page()
        password = self.get_arg(self.password.arg, None)
        if password is None:
            self.render_template(self.template, email=None, error=None)
        else:
            row = yield gramex.service.threadpool.submit(self.recover.pop, password)
            if row is not None:
                email = row['email']
                hd = email.rsplit('@', 2)[-1]       # host domain
                yield self.set_user({'email': email, 'hd': hd}, id='email')
                self.redirect_next()
            else:
                self.render_template(self.template, email=None, error='wrong-pw',
                                     msg='Invalid token')

    @coroutine
    def post(self):
        user = self.get_arg(self.user.arg, None)
        token = yield gramex.service.threadpool.submit(
            self.recover.token, user=user, email=user, expire=time.time() + self.expire)
        emailer = gramex.service.email[self.service]
        info = {
            'user': user,
            'password': token,
            'link': self.xredirect_uri + '?' + urlencode({
                self.password.arg: token,
                self.redirect_key: self.session.pop('_next_url', '/')
            }),
        }
        try:
            yield gramex.service.threadpool.submit(
                emailer.mail, to=user, subject=self.subject.format(**info),
                body=self.body.format(**info))
        except Exception as e:
            app_log.exception('%s: cannot send email OTP', self.name)
            self.render_template(self.template, email=user, error='not-sent', msg=e)
        else:
            app_log.debug('%s: sent email OTP to %s', self.name, user)
            self.render_template(self.template, email=user, error=None)


class OTP(object):
    '''
    OTP: One-time password. Also used for password recovery
    '''
    def __init__(self, size=None):
        '''
        Set up the database that stores password recovery tokens.
        ``size`` is the length of the OTP in characters. Defaults to the
        full hashing string
        '''
        self.size = size
        # create database at GRAMEXDATA
        path = os.path.join(gramex.variables.GRAMEXDATA, 'auth.recover.db')
        url = 'sqlite:///{}'.format(path)
        self.engine = gramex.data.create_engine(url, encoding=str_utf8)
        conn = self.engine.connect()
        conn.execute('CREATE TABLE IF NOT EXISTS users '
                     '(user TEXT, email TEXT, token TEXT, expire REAL)')
        self.table = gramex.data.get_table(self.engine, 'users')

    def token(self, user, email, expire):
        '''Generate a one-tie token, store it in the recovery database, and return it'''
        token = uuid.uuid4().hex[:self.size]
        query = self.table.insert().values({
            'user': user, 'email': email, 'token': token, 'expire': expire,
        })
        self.engine.execute(query)
        return token

    def pop(self, token):
        '''Return the row matching the token, and deletes it from the list'''
        where = self.table.c['token'] == token
        query = self.table.select().where(where)
        result = self.engine.execute(query)
        if result.returns_rows:
            row = result.fetchone()
            if row is not None:
                self.engine.execute(self.table.delete(where))
                if row['expire'] >= time.time():
                    return row
        return None


def csv_encode(values, *args, **kwargs):
    '''
    Encode an array of unicode values into a comma-separated string. All
    csv.writer parameters are valid.
    '''
    buf = StringIOClass()
    writer = csv.writer(buf, *args, **kwargs)
    writer.writerow([
        v if isinstance(v, str) else
        v.decode('utf-8') if isinstance(v, bytes) else repr(v)
        for v in values])
    return buf.getvalue().strip()
