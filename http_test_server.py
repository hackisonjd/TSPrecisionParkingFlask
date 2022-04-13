from http.server import BaseHTTPRequestHandler, HTTPServer
import time, json, random
import logging

# CHANGE HOSTNAME TO YOUR LOCAL IP
hostName = "10.0.0.7"
serverPort = 8000
def generate_data(length):
    data = {}
    for i in range(0, length):
        data[f'address{i}'] =  round(random.uniform(30.5, 95.5), 2)
    data = json.dumps(data)
    return data


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()
        self.wfile.write(bytes(f"{generate_data(4)}", "utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))
        print(post_data)
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
    


if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")