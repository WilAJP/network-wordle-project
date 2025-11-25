# ************************************************************
# Author: Christopher Frias
# Major: Computer Science
# Creation Date: October 19, 2025
# Due Date: November 24, 2025
# Course: CPSC 328 020
# Professor: Professor Walther
# Assignment: Wordle Project
# Filename: lib.py
# Purpose: provides functions for loading words, messaging,
#          and returning color results for server and client
# Language: Python ^.^
# ************************************************************

import random

# ************************************************************
# Function name: load_words
# Description: loads a list of words from a text file
# Parameters:
#       filename - a file containing words
# Return: list of words
# ************************************************************
def load_words(filename="words.txt"):
    try:
        with open(filename, "r") as f:
            return [w.strip() for w in f if w.strip()]
    except FileNotFoundError:
        print(f"{filename} not accessible")
        return []

# ************************************************************
# Function name: get_random_word
# Description: returns a random word from the list
# Parameters:
#       words - list of possible words
# Return: a random 5 letter word
# ************************************************************
def get_random_word(words):
    return random.choice(words)

# ************************************************************
# Function name: send_msg
# Description: sends a message through a connection
# Parameters:
#       conn - socket connection
#       msg  - message to send
# Return: None
# ************************************************************
def send_msg(conn, msg):
    conn.sendall((msg + "\n").encode())

# ************************************************************
# Function name: recv_msg
# Description: receives a message from connection
# Parameters:
#       conn - socket connection
# Return: received message or None
# ************************************************************
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

# ************************************************************
# Function name: returnColor
# Description: compare the words and check if letters correlate
# Parameters:
#       guess - guessed word
#       word  - correct word
# Return: list (color of each letter)
# ************************************************************
def returnColor(guess, word):
    # makes both words uppercase
    guess = guess.upper()
    word = word.upper()

    # result starts gray (underscore)
    result = ["_"] * len(guess)

    # counts amount of letters in the word
    counts = {}
    for ch in word:
        counts[ch] = counts.get(ch, 0) + 1

    # checks for green and yellow
    for i in range(len(guess)):
        if guess[i] == word[i]:
            result[i] = "G"
            counts[guess[i]] -= 1
        else:
            letter = guess[i]
            if letter in counts and counts[letter] > 0:
                result[i] = "Y"
                counts[letter] -= 1

    return result
