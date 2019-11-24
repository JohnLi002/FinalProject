# -*- coding: utf-8 -*-

import socket

# Start CLient Program
def client_program():
    
    # Initalize Client Socket
    host = socket.gethostname() 
    port = 5000  
    client_socket = socket.socket()
    
    # Connect to Server
    client_socket.connect((host, port))  
   
    # Send Server Name
    message = input("Username: ")  
    client_socket.send(message.encode())
    
    # Print Connection Status
    data = client_socket.recv(1024).decode() 
    print(data)
    
    # Joining message [0] and [2] represent the queue ie 1/3
    # If the same, the queue is full ie 3/3
    # Update status if other players have joined
    while(data[0] != data[2]): 
        data = client_socket.recv(1024).decode() 
        print(data) 
    
    # Receive "Welcome to the game!" message after all players have joined
    data = client_socket.recv(1024).decode() 
    print(data) 
    
    # Receive Dragons Action
    data = client_socket.recv(1024).decode() 
    print(data) 
    
    # Continues until message is "bye" or ?(Healh < 0)
    while message.lower().strip() != 'bye': 
        
        # Client Player Input
        while True:
            message = input(" -> ")  
            client_socket.send(message.encode())
            data = client_socket.recv(1024).decode()
            print(data)
            if(data[0:7] != 'Command'):
                break
        
        # Receives player current health
        while True:
            data = client_socket.recv(1024).decode()  
            print(data)
            if(data[0] == '['):
                break
    
    #client_socket.send(message) #send bye message
    client_socket.close()  
# End Client Program
    
if __name__ == '__main__':
    client_program()