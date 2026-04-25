# server.py

import socket

host = "localhost"
port = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)

print("Server listening on", host, port)

products = [
    {"id": 1, "name": "Shirt", "price": 500},
    {"id": 2, "name": "Shoes", "price": 1500}
]

cart = []

while True:
    client_socket, addr = server_socket.accept()
    data = client_socket.recv(4096)

    if data:
        request_text = data.decode()

        method = ""
        path = ""

        # ---- parse request line ----
        lines = request_text.split("\r\n")
        if len(lines) > 0:
            parts = lines[0].split(" ")
            if len(parts) > 1:
                method = parts[0]
                path = parts[1].strip()

        # ---- query parsing ----
        query_params = {}
        if "?" in path:
            parts = path.split("?")
            base_path = parts[0]
            query_string = parts[1]

            for pair in query_string.split("&"):
                if "=" in pair:
                    k, v = pair.split("=")
                    query_params[k] = v
        else:
            base_path = path

        body = ""

        # =========================
        # POST ROUTES
        # =========================

        if method == "POST" and base_path == "/add-to-cart":
            raw_body = request_text.split("\r\n\r\n")[-1]

            form_data = {}
            for pair in raw_body.split("&"):
                if "=" in pair:
                    k, v = pair.split("=")
                    form_data[k] = v

            if "id" in form_data:
                try:
                    pid = int(form_data["id"])
                    for p in products:
                        if p["id"] == pid:
                            cart.append(p)
                            body = f"<h1>Added {p['name']}</h1>"
                            break
                    else:
                        body = "<h1>Invalid Product</h1>"
                except:
                    body = "<h1>Error</h1>"
            else:
                body = "<h1>Invalid Request</h1>"

        elif method == "POST" and base_path == "/confirm-order":
            if len(cart) == 0:
                body = "<h1>Cart is Empty</h1>"
            else:
                total = sum(item["price"] for item in cart)
                cart.clear()
                body = f"<h1>Order Placed</h1><p>Total Paid: {total}</p>"

        # =========================
        # GET ROUTES
        # =========================

        else:
            if base_path == "/":
                body = "<h1>Home</h1><p>Welcome to Store</p>"

            elif base_path == "/products":
                body = "<h1>Products</h1>"
                for p in products:
                    body += f"{p['id']}. {p['name']} - {p['price']}<br>"

            elif base_path == "/cart":
                body = "<h1>Cart</h1>"
                total = 0

                for item in cart:
                    body += f"{item['name']} - {item['price']}<br>"
                    total += item["price"]

                body += f"<br>Total: {total}"

            elif base_path == "/checkout":
                if len(cart) == 0:
                    body = "<h1>Cart Empty</h1>"
                else:
                    total = sum(item["price"] for item in cart)
                    body = "<h1>Checkout</h1>"
                    body += f"Total: {total}"

            else:
                body = "<h1>404 Not Found</h1>"

        # =========================
        # RESPONSE
        # =========================

        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type: text/html\r\n"
        response += "Connection: close\r\n\r\n"
        response += body

        client_socket.send(response.encode())

    client_socket.close()