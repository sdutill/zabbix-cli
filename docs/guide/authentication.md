# Authentication

Zabbix-cli provides several ways to authenticate. They are tried in the following order if multiple are set:

1. [API token from config file](#api-token)
2. [Auth token from auth token file](#auth-token-file)
3. [Username and password from config file](#config-file)
4. [Username and password from auth file](#auth-file)
5. [Username and password from environment variables](#environment-variables)
6. [Username and password from prompt](#prompt)

## Username and Password

Password-based authentication is the default way to authenticate with Zabbix-cli. If the application is unable to determine authentication from other sources, it will prompt for a username and password.

### Config file

The password can be set directly in the config file:

```toml
[api]
zabbix_url = "https://zabbix.example.com/"
username = "Admin"
password = "zabbix"
```

### Auth file

An auth file named `.zabbix-cli_auth` can be created in the user's home directory. The content of this file should be in the `USERNAME::PASSWORD` format.

```bash
echo "Admin::zabbix" > ~/.zabbix-cli_auth
```

The location of this file can be changed in the config file:

```toml
[app]
auth_file = "/path/to/auth/file"
```

### Environment variables

The username and password can be set as environment variables:

```bash
export ZABBIX_USERNAME="Admin"
export ZABBIX_PASSWORD="zabbix"
```

### Prompt

By omitting the `password` parameter in the config file or when all other authentication methods have been exhausted, you will be prompted for a password when starting zabbix-cli:

```toml
[api]
zabbix_url = "https://zabbix.example.com/"
username = "Admin"
```

## API token

Zabbix-cli supports authentication with an API token specified directly in the config file:

```toml
[api]
auth_token = "API_TOKEN"
```

## Auth token file

The application can store the auth token returned by the Zabbix API. This is most useful when authenticating with a username and password from a prompt, which would otherwise require you to enter your password every time you start the application.

The feature can be enabled in the config file:

```toml
[app]
use_auth_token_file = true
```

The location of the auth token file can be changed in the config file:

```toml
[app]
auth_token_file = "/path/to/auth/token/file"
```

By default, the auth token file is not required to have secure permissions. If you want to require the file to have `600` (rw-------) permissions, you can set `allow_insecure_auth_file=false` in the config file. This has no effect on Windows.

```toml
[app]
allow_insecure_auth_file = false
```

Zabbix-cli attempts to set `600` permissions when writing the auth token file if `allow_insecure_auth_file=false`.
