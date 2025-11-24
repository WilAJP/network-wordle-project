# network-wordle-project

Project Leader - Wilfred Jimenez
Client - Charlen Baloukjy
Server - Wilfred Jimenez
Library - Christopher Frias

Description : A wordle style game using a client-server format in Python. The server provides random festive-themed words to connected clients, and the client allows the user to guess the words. The game gives the letters G or Y in results of guessing the correct or a letter in the word.

How to compile the client and server - No compilation. Project written in Python

How to run server - ?

How to run client - python client.py {hostname} {optional port number}

The type of library - Shared as we wanted the library to be used by both server and client withouth directly being embedded into the code. 

Protocol - TCP as we wanted the client and server to have a solid connection with eachother and there for not to be any data being loss when sent.
Protocol Syntax Messages:
- Client -> Server: READY (Client asks server to send a new secret word) | BYE (Client is done and wants to close the connection)
- Server -> Client: ?

Known Issues - None

Yes we worked as a team  to identify tasks assigned to eachother to be able to efficently complete the project successfully and on time.
