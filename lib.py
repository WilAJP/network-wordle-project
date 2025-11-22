import random

# loads the list of words from the text file
def load_words(filename="words.txt"):
    with open(filename, "r") as f:
        words = [w.strip() for w in f.readlines() if w.strip()]
    return words

# returns a random word from the list
def get_random_word(words):
    return random.choice(words)

# sends a message across the socket
def send_msg(conn, msg):
    conn.sendall((msg + "\n").encode())

# receives a message from the socket
def recv_msg(conn):
    data = conn.recv(1024).decode().strip()
    return data
