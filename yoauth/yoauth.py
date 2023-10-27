from dataclasses import dataclass
import http.server
import json
import ssl
import webbrowser
from urllib.parse import parse_qs, urlencode
import urllib.request

@dataclass
class SSLCerts():
    certfile: str = "cert.pem"
    keyfile: str = "key.pem"



def get_oauth_token(authorization_url, token_url, client_id, client_secret, scopes=[], require_tls=True, ssl_certs=SSLCerts()):
    params: dict = {}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            params.update(parse_qs(self.path.split("?")[1]))
            self.send_response(200, "OK")
            self.end_headers()
            self.wfile.write(
                "Authorized. This tab can be safely closed.".encode("utf-8")
            )

    with http.server.HTTPServer(("", 0), Handler) as httpd:
        _, port = httpd.server_address
        redirect_uri = f"{'https' if require_tls else 'http'}://localhost:{port}"

        if require_tls:
            httpd.socket = ssl.wrap_socket(
                httpd.socket,
                server_side=True,
                certfile=ssl_certs.certfile,
                keyfile=ssl_certs.keyfile,
            )

        authorization_path = urlencode(
            {
                "client_id": client_id,
                "redirect_uri": redirect_uri,
                "response_type": "code",
                "scope": ",".join(scopes),
            }
        )

        full_authorization_url = f"{authorization_url}?{authorization_path}"
        webbrowser.open_new_tab(full_authorization_url)
        while not params:
            httpd.handle_request()

    body = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": params["code"][0],
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri,
    }

    req = urllib.request.Request(token_url, data=json.dumps(body).encode('utf8'),
                             headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(req)

    return json.loads(response.read().decode('utf8'))
