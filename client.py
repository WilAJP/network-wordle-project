#****************************************************************************#
# Name: Charlen Baloukjy                                                     #
# Major: Computer Science                                                    #
# Creation Date: 10/16/2025                                                  #
# Due Date: 11/24/2025                                                       #
# Professor: Riley Walther                                                   #
# File Name: client.py                                                       #
# CPSC 328                                                                   #
# Team Program Application - Wordle                                          #
# Purpose: Interact with the user and perform the Wordle game functionality. #
#****************************************************************************#
import socket
import sys
from lib import send_msg, recv_msg, returnColor

DEFAULT_PORT = 50000

#*******************************************************************#
#                                                                   #
#   Function name:  play_round                                      #
#                                                                   #
#   Description:    Runs one full round of the Wordle game using    #
#                   the secret word provided by the server.         #
#                   Handles user guesses, validates inputs, tracks  #
#                   remaining letters, displays color-coded         #
#                   feedback, and determines win/loss conditions.   #
#                                                                   #
#   Parameters:     secret_word (str) - the word the player must    #
#                   guess.                                          #
#                                                                   #
#   Return Value:   None - controls a single round of gameplay and  #
#                   prints results to the screen.                   #
#                                                                   #
#*******************************************************************#

def play_round(secret_word):
    secret_word = secret_word.upper()   
    word_length = len(secret_word)                          # Store the word length
    attempts = 0                                            # Number of guesses taken
    max_attempts = 6                                        
    remaining_letters = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")   # Track unused letters

    print("\n!Game Started! ")
    print("Guess the {}-letter word!".format(word_length))
    print("You have {} attempts.".format(max_attempts))

    while attempts < max_attempts:
        try:
            guess = input("Guess #{}: ".format(attempts + 1)).strip().upper()
        except KeyboardInterrupt:
            print("\nGame cancelled by user.")          # User pressed Ctrl+C while playing
            return
            
        # Validate guess length and characters
        if len(guess) != word_length or not guess.isalpha():
            print("Please enter a valid {}-letter word.".format(word_length))
            continue

        attempts += 1
        
        # Remove guessed letters from remaining letters
        for char in guess:
            remaining_letters.discard(char)
            
        # Color feedback using library function
        result = returnColor(guess, secret_word)
        
        # Display the guess results
        print("  Your guess:  {}".format(guess))
        print("  Result:      {}".format("".join(result)))
        print("  Remaining Letters:   {}".format("".join(sorted(remaining_letters))))

        # Player winss
        if guess == secret_word:
            print("\nYou guessed the word {} in {} attempts. Great job!".format(secret_word, attempts))
            return
    # Player loses if loop ends
    print("\nOut of attempts! The word was {}.".format(secret_word))

#*******************************************************************#
#                                                                   #
#   Function name:  main                                            #
#                                                                   #
#   Description:    The main client function. Handles command-line  #
#                   argument parsing, validates the hostname/IP,    #
#                   connects to the Wordle server, exchanges the    #
#                   initial greeting, requests secret words,        #
#                   initiates gameplay rounds, and manages user     #
#                   continuation or exit commands.                  #
#                                                                   #
#   Parameters:     None (reads hostname and optional port from     #
#                   sys.argv).                                      #
#                                                                   #
#   Return Value:   None - controls the overall execution flow of   #
#                   the Wordle client.                              #
#                                                                   #
#*******************************************************************#

def main():
    try:

        if len(sys.argv) == 2:
            port = DEFAULT_PORT
        elif len(sys.argv) == 3:
            try:
                port = int(sys.argv[2])
            except ValueError:
                print("Error: port must be an integer.")
                print("Usage: python client.py <hostname> [port]")
                return
        else:
            print("Usage: python client.py <hostname> [port]")
            return

        host = sys.argv[1]

        # Validate host unless it's literally "localhost"
        if host.lower() != "localhost":
            try:
                socket.inet_aton(host)     # Validate it's a proper IPv4 address
            except OSError:
                print("Error: hostname must be 'localhost' or IPv4 address.")
                return


        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(3)      # Timeout to avoid hanging

            print("Connecting to {}:{} ...".format(host, port))
            try:
                sock.connect((host, port))
            except socket.timeout:
                print("Error: connection timed out.")
                return
            except ConnectionRefusedError:
                print("Error: connection refused by server.")
                return

            print("Connected.")

            # Receive server;s Hello
            try:
                hello = recv_msg(sock)
            except:
                return


            print("[SERVER]:", hello)


            while True:
                send_msg(sock, "READY")
                secret_word = recv_msg(sock)    # Get new secret word

                if not secret_word:
                    print("Server closed connection.")
                    break

                play_round(secret_word.strip())

                # Ask user if they want to play again
                try:
                    again = input("\nPlay again? (y/n): ").strip().lower()
                except KeyboardInterrupt:
                    print("\nEnding session.")
                    send_msg(sock, "BYE")
                    break

                if again != "y":
                    send_msg(sock, "BYE")
                    print("Goodbye!")
                    break

                print("\nRequesting another word from server...")
    # If user hits Ctrl+C at any point in main()
    except KeyboardInterrupt:
        print("\nClient terminated by user. Shutting down connection.")
        return


if __name__ == "__main__":
    main()
