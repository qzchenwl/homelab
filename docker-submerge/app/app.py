from http.server import BaseHTTPRequestHandler, HTTPServer
from dotenv import load_dotenv
from string import Template
from yaml_transformer import TransformerLoader

import os
import yaml

load_dotenv()

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        with open('config.yaml', 'r') as f:
            origin_yaml = f.read()
        template = Template(origin_yaml).safe_substitute(os.environ)
        result = yaml.load(template, Loader=TransformerLoader)
        del result['subscribers']
        content = yaml.dump(result, allow_unicode=True, sort_keys=False)
        self.send_response(200)
        self.send_header('Content-Type', 'text/yaml; charset=utf-8')
        self.end_headers()
        self.wfile.write(bytes(content, 'utf-8'))


if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8080), Server)
    print('Listen 0.0.0.0:8080')
    server.serve_forever()

