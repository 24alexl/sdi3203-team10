# Term Project For SDI 3203 | Team 10
## Connor T. and Alex L.

### How To Run

For the Server, run:<br>
``` python server.py <port number> ```
This will open up a server that listens on your respective IP Address on your desired port.

For the Clients, run:<br>
``` python client.py <IP address> <port number> ```
This will connect the client into the listening server at the port.
You will be asked a name (cannot have duplicates) and you will be granted entry.

To see who's online, run: ``` server:who ```

To message a person, run: ``` <name>:<message> ``` | Example: ```bob: hello!```

To leave, run: ```server:exit```