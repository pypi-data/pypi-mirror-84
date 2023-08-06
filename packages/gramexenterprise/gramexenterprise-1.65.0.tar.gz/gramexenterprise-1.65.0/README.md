# Gramex Enterprise Edition

Install the [enterprise edition of Gramex](https://learn.gramener.com/guide/):

```bash
pip install gramexenterprise
```

[Read the documentation for details](https://learn.gramener.com/guide/)


## Changelog

### 1.65.0

- DBAuth: remove `table` as an explicit kwarg. It is not required for files, and will fail for
  non-Excel files from Gramex CE 1.65.0 onwards.
- Auth: When Gramex is behind a proxy, use `handler.xredirect_uri` to redirect to the end-user URL,
  not the proxied URL (which would be `localhost:port`).

### 1.56.1

- DBAuth: `reset_url` should be ?forgot key

### 1.56.0

- DBAuth: extend signup to configure email like forgot configuration
