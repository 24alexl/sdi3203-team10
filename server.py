#!/usr/bin/env python3
# coding=utf-8
"""Basic multi-client chat server"""

import socket   # Network Communication
import threading    #   Concurrent Tasks

clients = {}    # Dictionary to store {username: client_socket}

def handle_client(client_socket, address):
    """
    Handles communication with single client.

    Args:
        client_socket: Socket object for connected client.
        address: Address (IP and Port) of connected client.
    """
    try:
        # Registration loop
        while True:
            username_req = client_socket.recv(1024).decode().strip()    # Takes username from client and strips
            if username_req.startswith("server:register "):
                username = username_req.split(" ", 1)[1]
                if username not in clients: # If username doesn't match any other registered members, create
                    clients[username] = client_socket
                    client_socket.send("server:registered\n".encode())  # Sends message to client to ensure they're in
                    break
                else:
                    client_socket.send("server:username_taken\n".encode())  # Sends message to know username is taken

        # Message handling loop
        while True:
            msg = client_socket.recv(1024).decode().strip() # Takes any msg and strips it at server
            if msg == "server:who": # server:who command
                active_users = ", ".join(clients.keys())
                client_socket.send(f"Online users: {active_users}\n".encode())  # Sends out online users

            elif msg == "server:exit":  # Exit Condition
                client_socket.send("server:goodbye\n".encode())
                break

            elif ":" in msg:    # Messaging system to individual users
                recipient, message = msg.split(":", 1)  # Text formatting
                if recipient in clients:
                    clients[recipient].send(f"{username}: {message}\n".encode())    # Sends message to other user
                else:
                    client_socket.send("server:user_not_found\n".encode())  # If user not found, send error

    except Exception as e:
        print(f"[ERROR] {e}")   # Other error catch

    finally:
        # Cleanup on disconnect
        for user, sock in clients.items():  # Every user disconnect when socket is shut down
            if sock == client_socket:
                del clients[user]
                break
        client_socket.close()

def start_server(host='127.0.0.1', port=8080):
    """
    Starts chat server and listens for incoming connections.

    Args:
        host: IP address that server should listen on.
              Defaults to 127.0.0.1 (localhost)
        port: Port number that server should listen on.
              Defaults to port 8080.
    """

    # Socket establishment
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"[SERVER STARTED] Listening on {host}:{port}")

    # Continuous checking and receiving of connections to server
    while True:
        client_socket, addr = server_socket.accept()
        print(f"[NEW CONNECTION] {addr}")
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    start_server()  # Main script to start server
