# interface.py

import socket
import tkinter as tk

HOST = "localhost"
PORT = 8080


def send_request(request):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    client.send(request.encode())

    response = client.recv(4096).decode()
    client.close()

    return response


def get_body(response):
    return response.split("\r\n\r\n", 1)[-1]


def update_text(content):
    text.delete(1.0, tk.END)
    text.insert(tk.END, content)


# ---- actions ----

def home():
    res = send_request("GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
    update_text(get_body(res))


def products():
    res = send_request("GET /products HTTP/1.1\r\nHost: localhost\r\n\r\n")
    update_text(get_body(res))


def cart():
    res = send_request("GET /cart HTTP/1.1\r\nHost: localhost\r\n\r\n")
    update_text(get_body(res))


def checkout():
    res = send_request("GET /checkout HTTP/1.1\r\nHost: localhost\r\n\r\n")
    update_text(get_body(res))


def add_shirt():
    body = "id=1"
    req = f"POST /add-to-cart HTTP/1.1\r\nHost: localhost\r\nContent-Length: {len(body)}\r\n\r\n{body}"
    res = send_request(req)
    update_text(get_body(res))


def add_shoes():
    body = "id=2"
    req = f"POST /add-to-cart HTTP/1.1\r\nHost: localhost\r\nContent-Length: {len(body)}\r\n\r\n{body}"
    res = send_request(req)
    update_text(get_body(res))


def confirm():
    req = "POST /confirm-order HTTP/1.1\r\nHost: localhost\r\n\r\n"
    res = send_request(req)
    update_text(get_body(res))


# ---- UI ----

root = tk.Tk()
root.title("Store Client")

frame = tk.Frame(root)
frame.pack()

tk.Button(frame, text="Home", command=home).grid(row=0, column=0)
tk.Button(frame, text="Products", command=products).grid(row=0, column=1)
tk.Button(frame, text="Cart", command=cart).grid(row=0, column=2)
tk.Button(frame, text="Checkout", command=checkout).grid(row=0, column=3)

tk.Button(frame, text="Add Shirt", command=add_shirt).grid(row=1, column=0)
tk.Button(frame, text="Add Shoes", command=add_shoes).grid(row=1, column=1)
tk.Button(frame, text="Confirm Order", command=confirm).grid(row=1, column=2)

text = tk.Text(root, height=20, width=60)
text.pack()

root.mainloop()