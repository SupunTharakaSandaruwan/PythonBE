from http.server import BaseHTTPRequestHandler, HTTPServer
import time
class ChunkedHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/file':
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Transfer-Encoding", "chunked")
            self.end_headers()

            with open('payload.txt', 'r') as file:
                payload = file.read()


            chunk_size = 10  # Specify the chunk size

            # Send the payload in chunks

            for i in range(0, len(payload), chunk_size):
                chunk = payload[i:i+chunk_size]
                chunk_hex = "{:X}".format(len(chunk))
                self.wfile.write(bytes(chunk_hex, "utf-8") + b"\r\n")
                self.wfile.write(bytes(chunk, "utf-8") + b"\r\n")
                self.wfile.flush()


            # Send the final zero-size chunk to indicate the end

            self.wfile.write(b"0\r\n\r\n")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

def run(server_class=HTTPServer, handler_class=ChunkedHandler, port=8001):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
