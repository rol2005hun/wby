import socket
import os

class WBYSERVER:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server started at {self.host}:{self.port}")

    def handle_request(self, client_socket):
        request = client_socket.recv(1024).decode()
        print(f"Received request: {request}")

        if request.startswith("GET"):
            try:
                url_path = request[4:].split(" ")[0]
                file_path = url_path
                
                file_location = os.path.join('C:/Users/rrol2/Documents/rol2005hun/Browserke', file_path)

                if os.path.exists(file_location):
                    print(f"Sending file: {file_location}")
                    with open(file_location, 'r') as f:
                        file_content = f.read()
                    
                    response = "WBY/1.0 100 SENT\r\n\r\n"
                    response += file_content
                    client_socket.sendall(response.encode())
                else:
                    client_socket.sendall(f"Error: File not found: {file_path}".encode())
            except Exception as e:
                client_socket.sendall(f"Error processing request: {str(e)}".encode())
        else:
            client_socket.sendall("Error: Invalid protocol. Use 'wby:'.".encode())

        client_socket.close()

    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connection from {addr}")
            self.handle_request(client_socket)


if __name__ == "__main__":
    server = WBYSERVER()
    server.start()