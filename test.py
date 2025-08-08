import socket

HOST = 'localhost'
PORT = 8080

try:
    print(f"🔄 Connecting to {HOST}:{PORT}...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("✅ Connected")
        data = s.recv(1024)
        print("📩 Received:", data.decode())
except Exception as e:
    print("❌ Error:", e)
