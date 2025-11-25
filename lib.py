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
    guess = guess.upper()
    word = word.upper()

    # Result starts gray
    result = ["_"] * len(guess)

    # Count letters in the secret word
    counts = {}
    for ch in word:
        counts[ch] = counts.get(ch, 0) + 1

    # ----- FIRST PASS: handle greens -----
    for i in range(len(guess)):
        if guess[i] == word[i]:
            result[i] = "G"
            counts[guess[i]] -= 1  # Reduce available count since it’s used

    # ----- SECOND PASS: handle yellows -----
    for i in range(len(guess)):
        # Skip indexes already green
        if result[i] == "G":
            continue

        letter = guess[i]
        if letter in counts and counts[letter] > 0:
            result[i] = "Y"
            counts[letter] -= 1  # Use one of that letter

    return result
