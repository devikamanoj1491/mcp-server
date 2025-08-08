import socket
import threading
import json

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 8080       # Or whatever port you're using

def handle_client(client_socket, address):
    print(f"[CONNECTED] {address} connected.")

    try:
        data = client_socket.recv(1024).decode()

        # Separate headers and body
        if "\r\n\r\n" not in data:
            raise ValueError("Invalid HTTP request format")
        headers, body = data.split("\r\n\r\n", 1)

        print(f"[HEADERS] {headers}")
        print(f"[BODY] {body}")

        # Try decoding JSON
        try:
            raw_json = json.loads(body)
            if isinstance(raw_json, str):
                request = json.loads(raw_json)
            else:
                request = raw_json
            print(f"[REQUEST] {request}")
        except Exception as e:
            print(f"[ERROR] Invalid JSON: {e}")
            client_socket.close()
            return

        # Handle JSON-RPC methods
        if request.get("method") == "ping":
            response = {
                "jsonrpc": "2.0",
                "result": "pong",
                "id": request.get("id")
            }
        else:
            response = {
                "jsonrpc": "2.0",
                "error": {"code": -32601, "message": "Method not found"},
                "id": request.get("id")
            }

        response_data = json.dumps(response)
        http_response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: application/json\r\n"
            f"Content-Length: {len(response_data)}\r\n"
            "Connection: close\r\n"
            "\r\n"
            f"{response_data}"
        )

        client_socket.sendall(http_response.encode())

    except Exception as e:
        print(f"[ERROR] {e}")

    finally:
        client_socket.close()
        print(f"[DISCONNECTED] {address} disconnected.")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[STARTED] MCP server listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        client_handler = threading.Thread(
            target=handle_client,
            args=(client_socket, addr)
        )
        client_handler.start()

if __name__ == "__main__":
    start_server()
