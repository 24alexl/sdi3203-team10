#!/usr/bin/env python3
# coding=utf-8
"""Module for client creation and connecting to designated server with username"""

import socket   # Network Communication
import threading    # Concurrent Tasks like receiving messages
import sys  # For system-specific params and funcs

def receive_messages(sock):
    """
    Listens continuously for messages on server given socket.
    
    Args: 
        sock (socket.socket): The socket connected to the server
    """
    while True:
        try:
            msg = sock.recv(1024).decode()  # Receive 1024 bytes (max) and decode to string
            if msg: # Message Receive Check
                print(msg)  # Prints message to console
        except:
            print("Disconnected from server.")  # Disconnect message if errors
            break # Exit loop

def start_client(host='127.0.0.1', port=8080):
    """
    Initialize client, connect to server, does username registration, 
    opens thread for receiving message, manages sending messages.

    Args:
        host (str, optional): Hostname or IP Addr. of server.
                              Defaults to '127.0.0.1' (localhost)
        port (int, optional): Port number of server to connect.
                              Defaults to 8080.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # TCP/IP socket created
    client_socket.connect((host, port)) # Connect to server at specific host and port

    # Register username
    while True:
        username = input("Enter your username: ").strip()   # Username prompt
        client_socket.send(f"server:register {username}".encode())  # Send registration request to server with encode to bytes
        response = client_socket.recv(1024).decode().strip()    # Receive server response and decode
        if response == "server:registered":
            print("[INFO] Registered successfully.")
            break   # Exit username registration loop
        elif response == "server:username_taken":
            print("[ERROR] Username already taken. Try again.")

    # Start listener thread
    listener_thread = threading.Thread(target=receive_messages, args=(client_socket,))  # Thread creation to handle incoming messages
    listener_thread.daemon = True   # Make thread daemon so upon exit, main thread exits
    listener_thread.start() # Start message receiving thread

    # Main sending loop
    while True:
        msg = input()   # Prompt user for input to send message
        if msg: # Message check
            client_socket.send(msg.encode())    # Send message to server (encoded as bytes)
            if msg == "server:exit":    # Exit condition
                break   # Exit loop

    client_socket.close()   # Closes server connection

if __name__ == "__main__":
    start_client()  # Runs the client function
