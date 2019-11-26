# -*- coding: utf-8 -*-

import socket

def client_program():
    
    # Initalize Client Socket
    host = socket.gethostname()  
    port = 5000  
    client_socket = socket.socket() 
    client_socket.connect((host, port))  
    
    # data = server string
    # message = client string
    
    # If player is still in the game
    finished = False
    
    # Choose Username and Send to Server
    username = "[" + input("Username: ") + "]" 
    message = username 
    client_socket.send(message.encode()) 
    
    # Receive Current Queue Status
    data = client_socket.recv(1024).decode() 
    print(data)
    
    # Receive Current Queue Status until Server is Full
    while(data[0] != data[2]): 
        data = client_socket.recv(1024).decode() 
        print(data) 
    
    # Receive Server Welcome Message
    data = client_socket.recv(1024).decode() 
    print(data) 
    
    # Receive Whose Turn it is 
    data = client_socket.recv(1024).decode() 
    print(data) 
    
    # Start Active Game
    while True: 
        
        # Check if player has died, close socket
        if finished: 
            print("The dragon has killed you")
            client_socket.close()
            break
        
        # Server returns whoses turn it is. 
        # If it is current clients turn (matches name), allowed to do some action
        if(data[0:len(username)] == username): 
            while True:
                message = input(" -> ")  
                client_socket.send(message.encode()) 
                data = client_socket.recv(1024).decode()
                print(data)
                
                # If action is illegal, get list of commands
                if(data[0:7] != 'Command' and data[0] != '-'): 
                    break
        
        # While it is not current player's turn, receive game updates
        while True:
            data = client_socket.recv(1024).decode() 
            
            # If player has died and receives death message from server 
            # Begin death sequence: Set finish to true, print death message, exit out of current then larger loop
            if(data == 'Dead'): 
                finished = True 
                data = client_socket.recv(1024).decode() 
                print(data) 
                break
            
            # Print other player's action 
            print(data)
            
            # #The client identifies the '[' to understands if it is the next turn
            if(data[0] == '['): 
                break
#End Client Program
    
if __name__ == '__main__':
    client_program()