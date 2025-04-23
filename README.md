# Term Project For SDI 3203 | Team 10

## Authors
Connor T. and Alex L.

## Introduction
This is a basic multi-client chat application developed for the SDI 3203 course. It allows multiple users to connect to a server, register with a unique username, view online users, send private messages to specific users, and exit the chat.

## How To Run

### Server

1.  Open your terminal or command prompt.
2.  Navigate to the directory containing the `server.py` file.
3.  Run the server using the following command, replacing `<port number>` with your desired port (e.g., 8080):

    ```bash
    python server.py <port number>
    ```

    This will start the server, listening for incoming connections on your machine's IP address and the specified port.

### Client

1.  Open a new terminal or command prompt for each client you want to run.
2.  Navigate to the directory containing the `client.py` file.
3.  Run the client using the following command, replacing `<IP address>` with the IP address of the server and `<port number>` with the port the server is listening on (the same port you used when starting the server):

    ```bash
    python client.py <IP address> <port number>
    ```

    * You will be prompted to enter a username.
    * Usernames must be unique; if a username is already taken, you will be asked to choose another one.
    * Once a unique username is entered, you will be granted entry to the chat.

## User Commands

Once connected to the server, you can use the following commands within the client terminal:

* **See Online Users:** To view a list of currently online users, type and send:
    ```
    server:who
    ```

* **Send a Private Message:** To send a message to a specific user, use the following format:
    ```
    <username>:<your message>
    ```
    **Example:**
    ```
    bob: hello!
    ```
    This will send the message "hello!" to the user with the username "bob".

* **Leave the Chat:** To disconnect from the server and exit the chat application, type and send:
    ```
    server:exit
    ```

## Notes
* Ensure that the server is running before attempting to connect with any clients.
* The server's IP address can be `127.0.0.1` or `localhost` if the server and clients are running on the same machine. Otherwise, use the actual IP address of the machine hosting the server.
* Choose a port number that is not already in use by other applications on your system.