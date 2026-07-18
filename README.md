# Python TCP Client-Server Wordle

A Wordle style game built in Python using a TCP client-server architecture. The server manages game sessions and sends random five-letter words to connected clients over a TCP connection.

## Team

This project was completed as a team for a university networking course.

| Team Member         | Responsibility                   |
| ------------------- | -------------------------------- |
| **Wilfred Jimenez** | Project Lead, Server Development |
| Charlen Baloukjy    | Client Development               |
| Christopher Frias   | Shared Library                   |

## My Contributions

As Project Lead, I was responsible for the server-side implementation of the project. My work included:

* Developing the TCP server using Python sockets
* Handling client connections and communication
* Implementing the server-side game logic
* Sending random words from the shared word list
* Assisting with integration, testing, and debugging

## Technologies

* Python
* TCP Sockets
* Client-Server Architecture
* Shared Python Library

## Networking Concepts

* TCP socket communication
* Client-server architecture
* Custom client/server messaging
* Persistent connections
* Network application testing

## Running the Project

Start the server:

```bash
python server.py
```

Start the client:

```bash
python client.py <hostname>
```

An optional port number can be provided when starting either the server or client.

## Protocol

**Client → Server**

* `READY` – Request a new word
* `BYE` – Close the connection

**Server → Client**

* `HELLO` – Sent when a client connects
* `<word>` – Random five-letter word sent after receiving `READY`

## Notes

The project uses a shared Python library and a text file containing the available five-letter words. The repository remains in its original team format to accurately represent each member's contributions.
