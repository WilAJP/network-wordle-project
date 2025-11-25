#*****************************************************************************#
# Author:        Wilfred Jimenez                                              #
# Major:         Computer Science                                             #
# Creation Date: Oct 19th, 2025                                               #
# Due Date:      November 27, 2025                                            #
# Course:        CSC 328                                                      #
# Professor:     Riley Walther                                                #
# Assignment:    Wordle Project                                               #
# Filename:      server.py                                                    #
# Purpose:       This program implements a concurrent TCP server that         #
#                sends random 5 letter words to clients. Each client          #
#                connects, receives a greeting, and can request new words     #
#                or disconnect.                                               #
# Language:      Python                                                       #
# How to run:    python server.py <port>                                      #
#                                                                             #
#*****************************************************************************#
import sys
import socket
import threading

from lib import load_words, get_random_word, send_msg, recv_msg

#*******************************************************************#
#                                                                   #
#   Function name:  portValidation                                  #
#   Description:    Validates the optional command line port        #
#                   argument, ensures it is within a valid range,   #
#                   and checks that it is not already in use.       #
#   Parameters:     defaultPort (int) - default port to use when    #
#                   no port is supplied on the command line         #
#   Return Value:   int - the validated port number                 #
#                                                                   #
#*******************************************************************#
def portValidation(defaultPort):
    #validate optional port agument and make sure its usable
    usage = "Usage: python server.py <port>"
    portNumError = "Please keep the port between 1 and 65535, thank you!"
    
    #if no port is given, use default
    if len(sys.argv) == 1:
        return defaultPort
        
    #if port is given, verify its an int
    elif len(sys.argv) == 2:
        try:
            port = int(sys.argv[1])
        except:
            print(usage)
            sys.exit()
            
        #verify port is not more than max port number on a pc
        if not (0 < port <= 65535):
            print(portNumError)
            sys.exit()
            
    else:   #too many arguments
        print(usage)
        sys.exit()
        
    #check if the port is available  and not in use
    testPort = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try: 
        testPort.bind(("0.0.0.0", port))
    except OSError:
        print(f"Port {port} is in use, please use another.")
        sys.exit()
    finally:
        testPort.close()    #close test socket
    return port 
    

#*******************************************************************#
#                                                                   #
#   Function name:  handleClient                                    #
#   Description:    Handles communication with a single client.     #
#                   Sends an initial HELLO message, processes       #
#                   client commands, and sends random words when    #
#                   requested. Closes the connection when the       #
#                   client disconnects or an error occurs.          #
#   Parameters:     connection (socket.socket) - client connection  #
#                   address (tuple) - client (ip, port)             #
#                   wordleWords (list of str) - list of possible    #
#                   words to send to the client                     #
#   Return Value:   None                                            #
#                                                                   #
#*******************************************************************#
def handleClient(connection, address, wordleWords):
    print("Connected by ", address)
    try:
        send_msg(connection, "HELLO") #send hello to client
        
        while True:
            message = recv_msg(connection)  #wait for full message
            if message is None:
                #client closes without sending BYE/QUIT
                print(f"Client {address} disconnected")
                break
            
            #upper case for all cases
            messageUpperCased = message.strip().upper()
            print("From Client: ", messageUpperCased)
            
            #client requests random word
            if messageUpperCased in ("READY", "WORD"):
                pickRandomWord = get_random_word(wordleWords)
                send_msg(connection, pickRandomWord)
                
                
            #client disconnects cleanly 
            elif messageUpperCased in ("BYE", "QUIT"):
                #close connection
                print(f"Client {address} sent {messageUpperCased}, closing connection")
                break
                
                
            else:   #for random messages 
                print(f"Unknown message from {address}: {messageUpperCased}")
                
    except socket.error as e:
        print(f"Socket error with {address}: {e}")
    finally:
        connection.close()      #always and I mean ALWAYS close the connection 
        print("Connection closed for ", address)
    
#*******************************************************************#
#                                                                   #
#   Function name:  main                                            #
#   Description:    Validates the port, loads the word list,        #
#                   creates the listening TCP socket, accepts       #
#                   incoming client connections, and starts a       #
#                   thread for each connected client. Shuts down    #
#                   cleanly on keyboard interrupt.                  #
#   Parameters:     None                                            #
#   Return Value:   None                                            #
#                                                                   #
#*******************************************************************#
def main():
    defaultPort = 50000 #default port 
        
    portNumber = portValidation(defaultPort)    #validate command line arguments 
    
    wordleWords = load_words("words.txt")   #load christmas word list
    
    #le TCP socket
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    #bind to chosen port
    tcpSocket.bind(("0.0.0.0", portNumber))
    tcpSocket.listen(5)
    print("Server is listening...")
    
    try:
        while True:
            connection, address = tcpSocket.accept()
            #thread for each client
            thread = threading.Thread(target = handleClient, args = (connection, address, wordleWords), daemon = True)
            thread.start()
    except KeyboardInterrupt:   #nice message if you control c on server
        print("\nTCP Server Shutting Down")
    finally: 
        tcpSocket.close()   #ALWAYS close main socket
        
if __name__ == "__main__":
    main()
