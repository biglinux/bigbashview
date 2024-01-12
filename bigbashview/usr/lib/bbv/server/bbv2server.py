from bbv import globaldata
import web
import sys
import socket
import threading
import time
import json
from . import views
import os

# Define a custom URL handler class
class FileHandler(views.url_handler):
    __url__ = "/api/file"

    def resolve_filename(self, filename):
        """Resolve $HOME to the home directory."""
        home_dir = os.path.expanduser("~")
        return filename.replace("$HOME", home_dir)

    def handle_request(self, method):
        # Get the filename from the request parameters
        params = web.input()
        filename = params.get('filename')
        if not filename:
            # If no filename is specified, return an error response
            web.ctx.status = '400 Bad Request'
            return json.dumps({"error": "No filename specified"})
        
        # Resolve $HOME in the filename
        filename = self.resolve_filename(filename)

        # Delegate to the actual HTTP method
        return method(filename)

    def GET(self):
        def method(filename):
            try:
                # Read the contents of the file and return as JSON
                with open(filename, 'r') as f:
                    data = json.load(f)
                return json.dumps(data)
            except FileNotFoundError:
                # If the file is not found, return an error response
                web.ctx.status = '404 Not Found'
                return json.dumps({"error": f"File {filename} not found"})
            except json.JSONDecodeError:
                # If the file contains invalid JSON, return an error response
                web.ctx.status = '400 Bad Request'
                return json.dumps({"error": f"Could not decode JSON in {filename}"})
            except Exception as e:
                # If any other exception occurs, return an error response
                web.ctx.status = '500 Internal Server Error'
                return json.dumps({"error": str(e)})
        return self.handle_request(method)

    def POST(self):
        def method(filename):
            # Parse the JSON data from the request body
            data = json.loads(web.data().decode())
            try:
                # Write the JSON data to the file
                with open(filename, 'w') as f:
                    json.dump(data, f)
                return json.dumps({"success": True})
            except Exception as e:
                # If any exception occurs, return an error response
                web.ctx.status = '500 Internal Server Error'
                return json.dumps({"error": str(e)})
        return self.handle_request(method)

    def PUT(self):
        def method(filename):
            # Parse the JSON data from the request body
            data = json.loads(web.data().decode())
            try:
                # Update the existing JSON data in the file
                with open(filename, 'r+') as f:
                    existing_data = json.load(f)
                    existing_data.update(data)
                    f.seek(0)
                    json.dump(existing_data, f)
                    f.truncate()
                return json.dumps({"success": True})
            except FileNotFoundError:
                # If the file is not found, return an error response
                web.ctx.status = '404 Not Found'
                return json.dumps({"error": f"File {filename} not found"})
            except json.JSONDecodeError:
                # If the file contains invalid JSON, return an error response
                web.ctx.status = '400 Bad Request'
                return json.dumps({"error": f"Could not decode JSON in {filename}"})
            except Exception as e:
                # If any other exception occurs, return an error response
                web.ctx.status = '500 Internal Server Error'
                return json.dumps({"error": str(e)})
        return self.handle_request(method)

    def DELETE(self):
        def method(filename):
            try:
                # Delete the file
                os.remove(filename)
                return json.dumps({"success": True})
            except FileNotFoundError:
                # If the file is not found, return an error response
                web.ctx.status = '404 Not Found'
                return json.dumps({"error": f"File {filename} not found"})
            except Exception as e:
                # If any other exception occurs, return an error response
                web.ctx.status = '500 Internal Server Error'
                return json.dumps({"error": str(e)})
        return self.handle_request(method)

# Define a custom server class
class Server(threading.Thread):
    def _get_subclasses(self, classes=None):
        """ Get subclasses recursively """
        if classes is None:
            classes = views.url_handler.__subclasses__()
        result = classes
        for cls in classes:
            result += self._get_subclasses(cls.__subclasses__())
        return result

    def get_urls(self):
        """ Return supported URLs. """
        classes = self._get_subclasses()
        result = ["/api/file", "FileHandler"]
        for cls in classes:
            result.append(cls.__url__)
            result.append(cls.__name__)
        return tuple(result)

    def get_classes(self):
        """ Return all view classes. """
        classes = self._get_subclasses()
        classes.append(FileHandler)  # Add the new class
        result = {}
        for cls in classes:
            result[cls.__name__] = cls
        return result

    def run(self):
        """ Run the webserver """
        ip = globaldata.ADDRESS
        port = globaldata.PORT
        sys.argv = [sys.argv[0], '']
        sys.argv[1] = ':'.join((ip, str(port)))

        urls = self.get_urls()
        classes = self.get_classes()
        self.app = web.application(urls, classes)
        self.app.run()

    def stop(self):
        os.kill(os.getpid(), 15)

# Function to run the server
def run_server(ip='127.0.0.1', background=True):
    # Find an available port to bind the server
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for port in range(19000, 19100):
        try:
            soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            soc.bind((ip, port))
            soc.close()
            break
        except socket.error as e:
            if e.errno != 98:
                raise socket.error(e)
            print('Port %d already in use, trying next one' % port)

    globaldata.ADDRESS = ip
    globaldata.PORT = port

    server = Server()

    if not background:
        web.config.debug = True
        return server.run()

    server.daemon = True
    web.config.debug = False
    server.start()
    time.sleep(0.05)
    # Wait for server to respond...
    while True:
        try:
            con = socket.create_connection((ip, port))
            con.close()
            break
        except socket.error as e:
            if e.errno != 111:
                raise socket.error(e)
            print('Waiting for server...')
            time.sleep(0.05)

    return server

# Run the server if the script is executed directly
if __name__ == "__main__":
    run_server(background=False)
