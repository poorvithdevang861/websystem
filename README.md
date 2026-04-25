# WebSystem

This project is a step-by-step low-level web server built with Python sockets.
Each folder (`Stage 1` to `Stage final`) adds one feature, starting from raw TCP and ending with a minimal e-commerce flow (products, cart, checkout, and UI).

## Prerequisites

- Python 3.8+ (recommended: Python 3.10 or newer)
- `curl` (for endpoint testing in terminal)
- Tkinter (only for `Stage 11 (tkinter UI)`, usually bundled with Python on macOS)

## Project Stages

- `Stage 1 (Raw TCP)`: Accept socket connection and respond.
- `Stage 2 (echo get)`: Basic GET request handling.
- `Stage 3 (request parsing)`: Parse HTTP request line.
- `Stage 4 (routing )`: Route by request path.
- `Stage 5 (html routing)`: Return HTML for routes.
- `Stage 6 (product routing`: Product-related route handling.
- `Stage 7 (data parsing)`: Query parameter parsing.
- `Stage 8 (Post Request Add-to-cart)`: Handle POST form data.
- `Stage 9 (Cart sytem)`: Cart flow improvements.
- `Stage 10 (checkout)`: Checkout endpoint/flow.
- `Stage 11 (tkinter UI)`: Local desktop client for the server.
- `Stage final (minimal HTML UI)`: Combined minimal e-commerce HTTP UI.

## Quick Start

From the repo root:

```bash
cd "Stage final (minimal HTML UI)"
python3 server.py
```

Server runs on:

- Host: `localhost`
- Port: `8080`

Open in browser:

- [http://localhost:8080/](http://localhost:8080/)

## Test with curl

Use another terminal while the server is running:

```bash
curl http://localhost:8080/
curl http://localhost:8080/products
curl "http://localhost:8080/product?id=1"
curl -X POST "http://localhost:8080/add-to-cart" -d "id=1"
curl http://localhost:8080/cart
curl http://localhost:8080/about
curl http://localhost:8080/xyz
```

## Run Any Stage

Each stage has its own `server.py` (except `Stage 11` also has `interface.py`).

Example:

```bash
cd "Stage 8 (Post Request Add-to-cart)"
python3 server.py
```

## Stage 11 (Tkinter UI)

Run server first:

```bash
cd "Stage 11 (tkinter UI)"
python3 server.py
```

Then run UI client in another terminal:

```bash
cd "Stage 11 (tkinter UI)"
python3 interface.py
```

This opens a desktop UI with buttons for Home, Products, Cart, Checkout, and Add-to-Cart actions.

## Notes

- Most stages bind to `localhost:8080`, so run only one stage at a time.
- If you get an "Address already in use" error, stop the currently running server and retry.
- Some folder names intentionally include spaces and symbols; always wrap paths in quotes in terminal commands.
