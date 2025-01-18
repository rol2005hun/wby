import socket
import os

class WbyServer:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"[Start] Server started at {self.host}:{self.port}")

    def handle_request(self, client_socket):
        try:
            request = client_socket.recv(1024).decode().strip()
            print(f"[Req] Received request: {request}")
            if request.startswith("GET"):
                url_path = request[4:].split(" ")[0]
                file_path = url_path if url_path.endswith(".wby") else url_path + ".wby"
                file_location = os.path.join('C:/Users/rrol2/Documents/rol2005hun/Browserke', file_path).replace("\\", "/")
                if os.path.exists(file_location):
                    print(f"[Res] Sending file: {file_location}")
                    with open(file_location, 'r') as f:
                        file_content = f.read()
                    response = "WBY/1.0 100 SENT\r\n\r\n" + file_content
                    client_socket.sendall(response.encode())
                else:
                    error_msg = f"[Error] File not found: {file_path}"
                    print(error_msg)
                    client_socket.sendall(error_msg.encode())
            else:
                client_socket.sendall("[Error] Invalid protocol. Use 'wby:'.".encode())
        except Exception as e:
            error_msg = f"[Error] Error processing request: {str(e)}"
            print(error_msg)
            client_socket.sendall(error_msg.encode())
        finally:
            client_socket.close()

    def start(self):
        print("[Info] Server is running and ready to accept connections...")
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"[Req] Connection from {addr}")
            self.handle_request(client_socket)


if __name__ == "__main__":
    server = WbyServer()
    server.start()