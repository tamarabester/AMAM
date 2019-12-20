import functools
import http.server
import re
from pathlib import Path


class Handler(http.server.BaseHTTPRequestHandler):



    def do_GET(self):
        
        methods = self.supported_methods
        path = self.path

        for pat in methods.keys():
            pattern = re.compile(f'^{pat}$')
            match = re.match(pattern,path)
            if match:
                match_key = pat
                break
            
        if not match:
            self.send_response(404)
            self.end_headers()
            return
            
        f = methods[match_key] 
        response, data = f(*match.groups())

        self.send_response(response)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(data ))
        self.end_headers()
        self.wfile.write(data.encode("utf-8"))
        return


class Website:
    supported_webpages = {}

    def route(self, path):
        def decorator(f):
            self.supported_webpages[f'{path}'] = f
#            func[re.compile(f'^{path}$')] = f
            @functools.wraps(f)
            def wrapper(f):
                return f(path)
            return wrapper
        return decorator

    def run(self, address):
        try:
            http_server = http.server.HTTPServer(address, Handler)
            Handler.supported_methods = self.supported_webpages
            http_server.serve_forever()
        except Exception as error:
            print(f'ERROR: {error}')
            return 1

