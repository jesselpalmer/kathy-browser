import socket
import sys


def is_valid_url(url):
    return url.startswith('http://')


def request(url):
    s = socket.socket()

    if not is_valid_url(url):
        return None

    url = url[len('http://'):]

    host, path = url.split('/', 1)
    path = '/' + path
    host_string = f'Host: {host}\r\n\r\n'
    host_string_bytes = bytes(host_string, encoding='utf-8')
    s.connect((host, 80))
    s.send(b'GET /index.html HTTP/1.0\r\n' +
           host_string_bytes)

    response = s.makefile("r", encoding="utf8", newline="\r\n")

    status_line = response.readline()
    version, status, explanation = status_line.split(" ", 2)
    assert status == "200", "{}: {}".format(status, explanation)

    headers = {}
    while True:
        line = response.readline()

        if line == "\r\n":
            break

        header, value = line.split(":", 1)
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


if __name__ == "__main__":
    if len(sys.argv) >= 1:
        url = sys.argv[1]
    else:
        url = 'http://example.org/'
    load(url)
