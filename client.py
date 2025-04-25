#!/usr/bin/env python3
# coding=utf-8
"""Module for client creation and connecting to designated server with username"""

import socket
import threading
import sys

# ANSI escape codes for colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
RESET = '\033[0m'

def receive_messages(sock, username):
    """
    Listens continuously for messages on server given socket and formats received messages with colors.

    Args:
        sock (socket.socket): The socket connected to the server
        username (str): The username of the current client
    """
    while True:
        try:
            msg = sock.recv(1024).decode()
            if msg:
                if msg.startswith("server:") and msg.split(":")[1] == "goodbye":
                    print(f"{YELLOW}{msg}{RESET}")
                    break
                elif ":" in msg:
                    sender, message = msg.split(":", 1)
                    print(f"[{GREEN}{sender}{RESET}->{BLUE}YOU{RESET}]: {message.strip()}")
                else:
                    print(f"{YELLOW}{msg}{RESET}") # Color other server messages
        except:
            print(f"{RED}[ERROR] Disconnected from server.{RESET}")
            break

def start_client(host, port):
    """
    Initialize client, connect to server, does username registration,
    opens thread for receiving message, manages sending messages with colored output.

    Args:
        host (str, optional): Hostname or IP Addr. of server.
                                Defaults to '127.0.0.1' (localhost)
        port (int, optional): Port number of server to connect.
                                Defaults to 8080.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    username = ""
    # Register username
    while True:
        username = input(f"Enter your {MAGENTA}username{RESET}: ").strip()
        client_socket.send(f"server:register {username}".encode())
        response = client_socket.recv(1024).decode().strip()
        if response == "server:registered":
            print(f"{GREEN}[INFO] Registered successfully as {CYAN}{username}{RESET}.")
            print(f"{YELLOW}[COMMANDS] {CYAN}recipient: message{YELLOW}', '{CYAN}server:who{YELLOW}', or '{CYAN}server:exit{YELLOW}'.{RESET} ")
            break
        elif response == "server:username_taken":
            print(f"{RED}[ERROR] Username already taken. Try again.{RESET}")

    # Start listener thread with username
    listener_thread = threading.Thread(target=receive_messages, args=(client_socket, username))
    listener_thread.daemon = True
    listener_thread.start()

    # Main sending loop
    while True:
        msg = input()
        if msg:
            if ":" in msg:
                recipient, content = msg.split(":", 1)
                print(f"[{BLUE}{username}{RESET}->{GREEN}{recipient.strip()}{RESET}]: {content.strip()}")
                client_socket.send(msg.encode())
            elif msg == "server:who":
                client_socket.send(msg.encode())
            elif msg == "server:exit":
                client_socket.send(msg.encode())
                break
            else:
                print(f"{YELLOW}[INFO] Invalid command or message format. Use '{CYAN}recipient: message{YELLOW}', '{CYAN}server:who{YELLOW}', or '{CYAN}server:exit{YELLOW}'.{RESET}")
        if msg == "server:exit":
            print(f"{RED}[EXITING SERVER]")
            break

    client_socket.close()

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 8080
    if len(sys.argv) == 3:
        host = sys.argv[1]  # '192.168.1.1'
        try:
            port = int(sys.argv[2]) # 9090
        except ValueError:
            print(f"{RED}[ERROR] Invalid port number. Using default port 8080.{RESET}")
    elif len(sys.argv) > 3:
        print(f"{YELLOW}[USAGE] python client.py <ip> <port>{RESET}")
        sys.exit(1)

    start_client(host, port)
