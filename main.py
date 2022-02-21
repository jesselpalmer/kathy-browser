from re import I
import socket

def is_valid_url(url):
  return url.startswith('http://')

def request(url):
  s = socket.socket()

  if not is_valid_url(url):
    return None

  url = url[len('http://'):]


  host, path = url.split('/', 1)
  path = '/' + path


  s.connect((host, 80))
  s.send(b'GET /index.html HTTP/1.0\r\n' + 
        b'Host: example.org\r\n\r\n')

  response = s.makefile("r", encoding="utf8", newline="\r\n")

  statusline = response.readline()
  version, status, explanation = statusline.split(" ", 2)
  assert status == "200", "{}: {}".format(status, explanation)

  headers = {}
  while True:
      line = response.readline()
      if line == "\r\n": break
      header, value = line.split(":", 1)
      headers[header.lower()] = value.strip()

  body = response.read()
  s.close()

  return headers, body

url = 'http://example.org/'
headers, body = request(url)
print(headers, body)

in_angle = False
for c in body:
    if c == '<':
        in_angle = True
    elif c == '>':
        in_angle = False
    elif not in_angle:
        print(c, end='')
