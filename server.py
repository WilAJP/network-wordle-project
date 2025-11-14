#Simple TCP server
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bind to local host
server.bind(("127.0.0.1", 5000))
#to connect from the same network, put the ip and the port
#server.bind(("192.168.1.14", 5000))

#Listen to incoming connections.
server.listen(1)
print("Server is listening...")

#accept a connection
connection, address = server.accept()
print(f"Connect by {address}")

#Receive data up to 1024 bytes
data = connection.recv(1024).decode()
print("Client says:", data)

#send a response
connection.sendall(b"Server says hello")

connection.close()
