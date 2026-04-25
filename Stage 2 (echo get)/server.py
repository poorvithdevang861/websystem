import socket

host = "localhost"
port = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((host, port))
server_socket.listen(1)

print("Server listening on", host, port)

while True:
    client_socket, addr = server_socket.accept()
    
    data = client_socket.recv(1024)

    if data:
        print(data.decode())

        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type: text/plain\r\n"
        response += "Connection: close\r\n"
        response += "\r\n"
        response += "Hello World"

        client_socket.send(response.encode())

    client_socket.close()