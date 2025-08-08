# mcp_server.py

import socket
import threading

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 8080       # MCP server port

def handle_client(conn, addr):
    print(f"[CONNECTED] {addr} connected.")
    conn.sendall(b"MCP SERVER READY\n")

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break

            command = data.decode().strip().upper()
            print(f"[COMMAND] {addr} sent: {command}")

            if command == "HELLO":
                conn.sendall(b"Hello from MCP Server!\n")
            elif command == "PING":
                conn.sendall(b"PONG\n")
            elif command.startswith("DATA"):
                conn.sendall(b"Data received successfully.\n")
            elif command == "EXIT":
                conn.sendall(b"Goodbye.\n")
                break
            else:
                conn.sendall(b"Unknown command.\n")
        except:
            break

    conn.close()
    print(f"[DISCONNECTED] {addr} disconnected.")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[STARTED] MCP Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
