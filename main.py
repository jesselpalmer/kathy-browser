import socket
import ssl
import sys

HTTP_PORT = 80
HTTPS_PORT = 443
HTTP_SCHEME = 'http'
HTTPS_SCHEME = 'https'
URL_DELIMITER = '://'
HTTP_BEGINNING = HTTP_SCHEME + URL_DELIMITER
HTTPS_BEGINNING = HTTPS_SCHEME + URL_DELIMITER
DEFAULT_CHAR_ENCODING = 'utf-8'
EOL = '\r\n'
OK_STATUS_CODE = '200'


def is_valid_url(url):
    return url.startswith(HTTP_BEGINNING) or url.startswith(HTTPS_BEGINNING)


def request(url):
    s = socket.socket()

    if not is_valid_url(url):
        return None

    scheme, url = url.split(URL_DELIMITER, 1)
    assert scheme in [HTTP_SCHEME, HTTPS_SCHEME], \
        'Unknown scheme {}'.format(scheme)

    host, path = url.split('/', 1)
    path = '/' + path

    if ":" in host:
        host, port = host.split(":", 1)
        port = int(port)
    else:
        port = HTTP_PORT if scheme == HTTP_SCHEME else HTTPS_PORT

    if scheme == HTTPS_SCHEME:
        ctx = ssl.create_default_context()
        s = ctx.wrap_socket(s, server_hostname=host)

    s.connect((host, port))

    http_request_string = f'GET /index.html HTTP/1.0{EOL}'
    http_request_string_bytes = bytes(http_request_string, encoding=DEFAULT_CHAR_ENCODING)

    host_string = f'Host: {host}{EOL}{EOL}'
    host_string_bytes = bytes(host_string, encoding=DEFAULT_CHAR_ENCODING)

    s.send(http_request_string_bytes + host_string_bytes)

    response = s.makefile('r', encoding=DEFAULT_CHAR_ENCODING, newline=EOL)

    status_line = response.readline()
    version, status, explanation = status_line.split(' ', 2)
    assert status == OK_STATUS_CODE, '{}: {}'.format(status, explanation)

    headers = {}
    while True:
        line = response.readline()

        if line == EOL:
            break

        header, value = line.split(':', 1)
        headers[header.lower()] = value.strip()

    body = response.read()
    s.close()

    return headers, body


def show(body):
    in_angle = False

    for c in body:
        if c == '<':
            in_angle = True
        elif c == '>':
            in_angle = False
        elif not in_angle:
            print(c, end='')


def load(url):
    headers, body = request(url)
    show(body)


if __name__ == '__main__':
    default_site = 'http://example.org:80/'

    if len(sys.argv) >= 2:
        site = sys.argv[1]
    else:
        site = default_site

    load(site)
