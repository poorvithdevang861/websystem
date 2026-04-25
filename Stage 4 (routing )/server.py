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
        request_text = data.decode()
        print(request_text)

        # ---- Stage 3 parsing ----
        method = ""
        path = ""

        lines = request_text.split("\r\n")
        if len(lines) > 0:
            first_line = lines[0]

            parts = first_line.split(" ")
            if len(parts) > 1:
                method = parts[0]
                path = parts[1]

                print("Method:", method)
                print("Path:", path)
        # ---- end parsing ----

        # ---- Stage 4 routing ----
        routes = {
            "/": "Home Page",
            "/products": "Product List",
            "/about": "About Page"
        }

        if path in routes:
            body = routes[path]
        else:
            body = "404 Not Found"
        # ---- end routing ----

        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type: text/plain\r\n"
        response += "Connection: close\r\n"
        response += "\r\n"
        response += body

        client_socket.send(response.encode())

    client_socket.close()