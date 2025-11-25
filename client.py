import socket
import sys
from lib import send_msg, recv_msg, returnColor

DEFAULT_PORT = 50000

def play_round(secret_word):
    secret_word = secret_word.upper()
    word_length = len(secret_word)
    attempts = 0                       # How many guesses the player has used
    max_attempts = 6                   # Total allowed attempts
    remaining_letters = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")  # Track unused letters

    print("\n!Game Started! ")
    print("Guess the {}-letter word!".format(word_length))
    print("You have {} attempts.".format(max_attempts))

    # Loop until player runs out of attempts
    while attempts < max_attempts:
        guess = input("Guess #{}: ".format(attempts + 1)).strip().upper()  # Read guess

        # Ensure guess is correct size and valid letters
        if len(guess) != word_length or not guess.isalpha():
            print("Please enter a valid {}-letter word.".format(word_length))
            continue

        attempts += 1

        # Remove guessed letters from the remaining alphabet
        for char in guess:
            remaining_letters.discard(char)

        # Call library function to get green/yellow/gray result
        result = returnColor(guess, secret_word)

        # Print results for the player
        print("  Your guess:  {}".format(guess))
        print("  Result:      {}".format("".join(result)))
        print("  Remaining Letters:   {}".format("".join(sorted(remaining_letters))))

        # If correct guess, end the round early
        if guess == secret_word:
            print("\n You guessed the word {} in {} attempts. Great Job!".format(secret_word, attempts))
            return

    # If loop ends with no correct guess
    print("\nOut of attempts! The word was {}.".format(secret_word))


def main():
    # Check if hostname was provided
    if len(sys.argv) < 2:
        print("Usage: python client.py <hostname> [port]")
        sys.exit(1)

    host = sys.argv[1]  # Hostname or IP given by user

    # Read port argument if provided; otherwise use default
    if len(sys.argv) >= 3:
        try:
            port = int(sys.argv[2])  # Convert user port to integer
        except ValueError:
            port = DEFAULT_PORT      # If invalid port, use default
    else:
        port = DEFAULT_PORT

    # Create TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        print("Connecting to {}:{} ...".format(host, port))
        sock.connect((host, port))     # Connect to the server
        print("Connected.")

        hello = recv_msg(sock)         # Wait for server's "Hello"
        if not hello:
            print("Server closed connection.")
            return

        print("[SERVER]:", hello)

        # Game loop
        while True:
            send_msg(sock, "READY")    # Tell server client is ready
            secret_word = recv_msg(sock)  # Receive secret word

            if not secret_word:
                print("Server closed connection.")
                break

            secret_word = secret_word.strip()  # Remove newline received value
            play_round(secret_word)            # Start a game round

            # Ask user if they want to play again
            again = input("\nPlay again? (y/n): ").strip().lower()
            if again != "y":
                send_msg(sock, "BYE")  # Tell server client is disconnecting
                print("Goodbye!")
                break
            else:
                print("\nRequesting another word from server...")


main()
