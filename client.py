import socket

# Define the server's IP address and port
HOST = '10.24.2.13'  # The server's hostname or IP address
PORT = 50001        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Connect to the server
    s.connect((HOST, PORT))
    print(f"Connected to {HOST}:{PORT}")

    # Send data to the server
    message = "Hello, server!"
    s.sendall(message.encode('utf-8'))
    print(f"Sent: {message}")

    # Receive data from the server
    data = s.recv(1024)  # Receive up to 1024 bytes
    print(f"Received: {data.decode('utf-8')}")
