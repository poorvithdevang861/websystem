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

cart = []

# ---- HTML wrapper ----
def wrap_html(content):
    html = "<html>"
    html += "<head><title>My Store</title></head>"
    html += "<body>"

    html += '<a href="/">Home</a> | '
    html += '<a href="/products">Products</a> | '
    html += '<a href="/cart">Cart</a> | '
    html += '<a href="/about">About</a>'
    html += "<hr>"

    html += content

    html += "</body></html>"
    return html
# ---- end wrapper ----

while True:
    client_socket, addr = server_socket.accept()
    
    data = client_socket.recv(4096)

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

        # ---- query parsing ----
        query_params = {}

        if "?" in path:
            parts = path.split("?")
            base_path = parts[0].strip()
            query_string = parts[1]

            pairs = query_string.split("&")
            for pair in pairs:
                if "=" in pair:
                    kv = pair.split("=")
                    query_params[kv[0]] = kv[1]
        else:
            base_path = path.strip()

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
                        content = "<h1>Item Added</h1>"
                        content += '<a href="/products">Back to Products</a>'
                    else:
                        content = "<h1>Invalid Product</h1>"

                except:
                    content = "<h1>Invalid Product</h1>"
            else:
                content = "<h1>Invalid Product</h1>"

            body = wrap_html(content)

        # ---- GET routes ----
        else:
            if base_path == "/":
                content = "<h1>Home Page</h1>"
                content += "<p>Welcome to store</p>"

            elif base_path == "/products":
                content = "<h1>Product List</h1><ul>"

                for p in products:
                    content += "<li>"
                    content += p["name"] + " - " + str(p["price"])

                    content += '<form method="POST" action="/add-to-cart">'
                    content += '<input type="hidden" name="id" value="' + str(p["id"]) + '">'
                    content += '<button type="submit">Add to Cart</button>'
                    content += "</form>"

                    content += "</li>"

                content += "</ul>"

            elif base_path == "/about":
                content = "<h1>About Page</h1>"

            elif base_path == "/product":
                if "id" in query_params:
                    try:
                        product_id = int(query_params["id"])
                        found = False

                        for p in products:
                            if p["id"] == product_id:
                                content = "<h1>Product Detail</h1>"
                                content += "<p>Name: " + p["name"] + "</p>"
                                content += "<p>Price: " + str(p["price"]) + "</p>"
                                content += '<a href="/products">Back</a>'
                                found = True
                                break

                        if not found:
                            content = "<h1>Product Not Found</h1>"

                    except:
                        content = "<h1>Product Not Found</h1>"
                else:
                    content = "<h1>Product Not Found</h1>"

            elif base_path == "/cart":
                content = "<h1>Cart</h1><ul>"
                total = 0

                for item in cart:
                    content += "<li>" + item["name"] + " - " + str(item["price"]) + "</li>"
                    total += item["price"]

                content += "</ul>"
                content += "<h2>Total: " + str(total) + "</h2>"

            else:
                content = "<h1>404 Not Found</h1>"

            body = wrap_html(content)

        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type: text/html\r\n"
        response += "Connection: close\r\n"
        response += "\r\n"
        response += body

        client_socket.send(response.encode())

    client_socket.close()