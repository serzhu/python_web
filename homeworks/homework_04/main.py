from http.server import HTTPServer, BaseHTTPRequestHandler
import mimetypes
import socket
import json
import urllib.parse
import logging
from pathlib import Path
from threading import Thread
from time import sleep
from  datetime import datetime

BASE_DIR = Path(__file__).parent
DATAFILE = BASE_DIR / 'storage' / 'data.json'
BUFFER_SIZE = 1024
HTTP_PORT = 3000
SOCKET_PORT = 5000
HTTP_HOST = '0.0.0.0'
SOCKET_HOST = '127.0.0.1'

def load_data_from_file():
    DATAFILE.parent.mkdir(exist_ok=True, parents=True)
    if not DATAFILE.exists():
        with open(DATAFILE, 'w', encoding='utf-8') as file:
            json.dump({}, file, ensure_ascii=False, indent=4)
    with open(DATAFILE, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


data_dict = load_data_from_file()

def save_data_from_form(data: bytes):
    data_parse = urllib.parse.unquote_plus(data.decode()) 
    try:
        messages_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
        data_dict[str(datetime.now())] = messages_dict
        with open(DATAFILE, 'w', encoding='utf-8') as file:
            json.dump(data_dict, file, ensure_ascii=False, indent=4)
    except ValueError as e:
        logging.error(e)
    except OSError as e: 
        logging.error(e)


class WebServer(Thread):
    def __init__(self, host=HTTP_HOST, port=HTTP_PORT):
        super().__init__()
        self.host = host
        self.port = port
        self.http_server = HTTPServer((self.host, self.port), HttpHandler)
    
    def run(self):
        self.http_server.server_name
        logging.info(f'Starting HTTP server on port {self.port}')
        self.http_server.serve_forever() 
    
    def shutdown(self):
        logging.info('Shutting down HTTP server')
        self.http_server.shutdown()
        logging.info('Closing HTTP server')
        self.http_server.server_close()
        logging.info('Closing thread HTTP server')
        self.join()


class SocketServer(Thread):
    def __init__(self, host = SOCKET_HOST, port = SOCKET_PORT):
        super().__init__()
        self.host = host
        self.port = port
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def run(self):
        logging.info(f'Starting SOCKET server')
        self.socket_server.bind((self.host, self.port))
        try:
            while True:
                data, address = self.socket_server.recvfrom(BUFFER_SIZE)
                logging.info(f'Received message: {data} from {address}')
                save_data_from_form(data)
        except OSError:
            pass

    def shutdown(self):
        logging.info(f'Closing SOCKET')
        self.socket_server.close()
        logging.info('Closing thread SOCKET server')
        self.join()


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file(BASE_DIR / 'index.html')
        elif pr_url.path == '/message':
            self.send_html_file(BASE_DIR / 'message.html')
        else:
            file = BASE_DIR.joinpath(pr_url.path[1:])
            if file.exists():
                self.send_static(file)
            else:
                self.send_html_file(BASE_DIR / 'error.html', 404)

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.sendto(data, (SOCKET_HOST, SOCKET_PORT))
        client_socket.close()
        self.send_response(302)
        self.send_header('Location', '/message')
        self.end_headers()

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())
    
    def send_static(self, filename, status=200):
        self.send_response(status)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s:%(message)s')

    http_server = WebServer()
    http_server.start()
    socket_server = SocketServer()
    socket_server.start()
    while True:
        try:
            sleep(1)
        except KeyboardInterrupt:
            logging.info('Keyboard Interrupt sent')
            socket_server.shutdown()
            sleep(1)
            http_server.shutdown()
            exit(0)
