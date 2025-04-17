import socket
import threading
import sys

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if msg:
                print(msg)
        except:
            print("Disconnected from server.")
            break

def start_client(host='127.0.0.1', port=8080):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Register username
    while True:
        username = input("Enter your username: ").strip()
        client_socket.send(f"server:register {username}".encode())
        response = client_socket.recv(1024).decode().strip()
        if response == "server:registered":
            print("[INFO] Registered successfully.")
            break
        elif response == "server:username_taken":
            print("[ERROR] Username already taken. Try again.")

    # Start listener thread
    listener_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    listener_thread.daemon = True
    listener_thread.start()

    # Main sending loop
    while True:
        msg = input()
        if msg:
            client_socket.send(msg.encode())
            if msg == "server:exit":
                break

    client_socket.close()

if __name__ == "__main__":
    start_client()
