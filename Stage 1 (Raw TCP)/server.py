import socket

host = "localhost"
port = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((host, port))
server_socket.listen(1)

print("Server listening on", host, port)

while True:  # loop = yes
    client_socket, addr = server_socket.accept()
    
    data = client_socket.recv(1024)  # recv_bytes = 1024

    if data:
        print(data.decode())  # print_request = yes
        client_socket.send(data)  # echo_back = yes

    client_socket.close()  # close_after_response = yes