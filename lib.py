import random

# loads the list of words from the text file
def load_words(filename="words.txt"):
    with open(filename, "r") as f:
        words = [w.strip() for w in f.readlines() if w.strip()]
    return words

# returns a random word from the list
def get_random_word(words):
    return random.choice(words)

# sends a msg
def send_msg(conn, msg):
    conn.sendall((msg + "\n").encode())

# receives a msg 
def recv_msg(conn):
    incomingData = b""
    while True:
        chunk = conn.recv(1024)
        if not chunk:
            if not incomingData:
                return None
            break
        incomingData += chunk
        if b"\n" in chunk:
            break
        
    message = incomingData.decode("utf-8")
    return message

def returnColor(guess, word):
    # default color grey
    result = ["_"] * len(guess)

    # count letters in word
    counts = {}
    for ch in word:
        counts[ch] = counts.get(ch, 0) + 1

    # loop through check either green or yellow
    for i in range(len(guess)):
        if guess[i] == word[i]:
            result[i] = "G"
            counts[guess[i]] -= 1
        else:
            # yellow if in dict 
            if guess[i] in counts and counts[guess[i]] > 0:
                result[i] = "Y"
                counts[guess[i]] -= 1

    return result

