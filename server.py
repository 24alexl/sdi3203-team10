import socket
import threading

# Dictionary to store {username: client_socket}
clients = {}

def handle_client(client_socket, address):
    try:
        # Registration loop
        while True:
            username_req = client_socket.recv(1024).decode().strip()
            if username_req.startswith("server:register "):
                username = username_req.split(" ", 1)[1]
                if username not in clients:
                    clients[username] = client_socket
                    client_socket.send("server:registered\n".encode())
                    break
                else:
                    client_socket.send("server:username_taken\n".encode())

        # Message handling loop
        while True:
            msg = client_socket.recv(1024).decode().strip()
            if msg == "server:who":
                active_users = ", ".join(clients.keys())
                client_socket.send(f"Online users: {active_users}\n".encode())

            elif msg == "server:exit":
                client_socket.send("server:goodbye\n".encode())
                break

            elif ":" in msg:
                recipient, message = msg.split(":", 1)
                if recipient in clients:
                    clients[recipient].send(f"{username}: {message}\n".encode())
                else:
                    client_socket.send("server:user_not_found\n".encode())

    except Exception as e:
        print(f"[ERROR] {e}")

    finally:
        # Cleanup on disconnect
        for user, sock in clients.items():
            if sock == client_socket:
                del clients[user]
                break
        client_socket.close()

def start_server(host='0.0.0.0', port=8080):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"[SERVER STARTED] Listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[NEW CONNECTION] {addr}")
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
