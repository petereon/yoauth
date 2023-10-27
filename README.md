# YOAuth

Getting a token has never been easier. You only need few URLs, few secrets and a web browser. No dependencies, no fuss.

## Installation

```
pip install git+https://github.com/petereon/yoauth.git
```

## Usage

Google `oauth2` example:

```python
from yoauth import get_oauth_token

google_token = get_oauth_token(
    authorization_url="https://accounts.google.com/o/oauth2/v2/auth",
    token_url="https://oauth2.googleapis.com/token",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    scopes=GOOGLE_SCOPES,
)
```

By default the function will require private key and certificate pair to be provided. These take a form of a file in the filesystem and are used to facilitate TLS for the web-server which gets created to consume the OAuth redirect. Default expected names of these files are `key.pem` and `cert.pem` respectively. You can configure this as follows:

```python
from yoauth import get_oauth_token, SSLCerts

google_token = get_oauth_token(
    authorization_url="https://accounts.google.com/o/oauth2/v2/auth",
    token_url="https://oauth2.googleapis.com/token",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    scopes=GOOGLE_SCOPES,
    ssl_certs=SSLCerts(
        cert_file="myRadCertName.pem",
        key_file="/secret/path/very_secret_private_key.pem",
    )
)
```

:warning: If you really REALLY trust your network you can disable this by setting `require_tls=False`, but be aware that **tokens** that provide access to your potentially expensive cloud resources or sensitive data **will be sent around in plain-text**. This software is distributed under MIT license. I will not be held responsible for any damages caused by your negligence.


### How it works

The function `get_oauth_token` does a few things:

1. Opens a system default web browser with the `authorization_url`, this will generally be a login page.
2. Creates a short-lived `localhost` web-server on a free system-provided port and waits for authorization request redirect. The browser will automatically be redirected after a successful login.
3. Server receives the authorization code from the redirect and stops serving.
4. Request is sent to `token_url` utilizing the authorization_code and token is recieved in response.
