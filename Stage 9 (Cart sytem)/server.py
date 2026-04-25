import socket

host = "localhost"
port = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((host, port))
server_socket.listen(1)

print("Server listening on", host, port)

products = [
    {"id": 1, "name": "Shirt", "price": 500},
    {"id": 2, "name": "Shoes", "price": 1500}
]

# ---- Stage 9 cart ----
cart = []
# ---- end cart ----

while True:
    client_socket, addr = server_socket.accept()
    
    data = client_socket.recv(1024)

    if data:
        request_text = data.decode()
        print(request_text)

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

        # ---- query parsing ----
        query_params = {}

        if "?" in path:
            parts = path.split("?")
            base_path = parts[0]
            query_string = parts[1]

            pairs = query_string.split("&")
            for pair in pairs:
                if "=" in pair:
                    kv = pair.split("=")
                    query_params[kv[0]] = kv[1]
        else:
            base_path = path

        body = ""

        # ---- POST add to cart ----
        if method == "POST" and base_path == "/add-to-cart":
            raw_body = ""
            if "\r\n\r\n" in request_text:
                raw_body = request_text.split("\r\n\r\n")[1]

            form_data = {}
            pairs = raw_body.split("&")
            for pair in pairs:
                if "=" in pair:
                    kv = pair.split("=")
                    form_data[kv[0]] = kv[1]

            print("POST DATA:", form_data)

            if "id" in form_data:
                try:
                    product_id = int(form_data["id"])
                    found = False

                    for p in products:
                        if p["id"] == product_id:
                            cart.append(p)
                            found = True
                            break

                    if found:
                        body = "<h1>Item Added</h1>"
                    else:
                        body = "<h1>Invalid Product</h1>"

                except:
                    body = "<h1>Invalid Product</h1>"
            else:
                body = "<h1>Invalid Product</h1>"

        # ---- GET routes ----
        else:
            if base_path == "/":
                body = "<h1>Home Page</h1>"

            elif base_path == "/products":
                body = "<h1>Product List</h1><ul>"
                for p in products:
                    body += "<li>" + p["name"] + " - " + str(p["price"]) + "</li>"
                body += "</ul>"

            elif base_path == "/about":
                body = "<h1>About Page</h1>"

            elif base_path == "/product":
                if "id" in query_params:
                    try:
                        product_id = int(query_params["id"])
                        found = False

                        for p in products:
                            if p["id"] == product_id:
                                body = "<h1>Product Detail</h1>"
                                body += "<p>Name: " + p["name"] + "</p>"
                                body += "<p>Price: " + str(p["price"]) + "</p>"
                                found = True
                                break

                        if not found:
                            body = "<h1>Product Not Found</h1>"

                    except:
                        body = "<h1>Product Not Found</h1>"
                else:
                    body = "<h1>Product Not Found</h1>"

            elif base_path == "/cart":
                body = "<h1>Cart</h1><ul>"
                total = 0

                for item in cart:
                    body += "<li>" + item["name"] + " - " + str(item["price"]) + "</li>"
                    total += item["price"]

                body += "</ul>"
                body += "<h2>Total: " + str(total) + "</h2>"

            else:
                body = "<h1>404 Not Found</h1>"

        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type: text/html\r\n"
        response += "Connection: close\r\n"
        response += "\r\n"
        response += body

        client_socket.send(response.encode())

    client_socket.close()