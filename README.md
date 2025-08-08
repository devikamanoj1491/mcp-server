# 🛰️ MCP Server – Hackathon Submission

This is a simple MCP (Minimal Control Protocol) server created for the hackathon. It handles basic text-based client commands over TCP.

## 💡 Features

- Accepts TCP client connections
- Handles commands:
  - `HELLO` → returns greeting
  - `PING` → returns `PONG`
  - `DATA <payload>` → acknowledges data
  - `EXIT` → closes connection
- Multi-client support using threads

## ⚙️ How to Run

### 🐍 Requirements
- Python 3.x

### ▶️ Run the server

```bash
python mcp_server.py
