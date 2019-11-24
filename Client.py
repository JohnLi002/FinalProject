# -*- coding: utf-8 -*-

import socket
def client_program():#'10.220.112.48'
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    # data = server string
    # message = client string
    
    message = input("Username: ")  # take input which will be the username associated with the host
    client_socket.send(message.encode()) #sends server the message
    
    data = client_socket.recv(1024).decode() #after join, there is an initial message of how you just joined
    print(data)
    
    while(data[0] != data[2]): #Within the joining message the 1st and 3rd parts there are numbers 
                               #that represent the queue. If the numbers are the same, the queue is filled
        data = client_socket.recv(1024).decode()  # receive any othere joining messages which appear every time someone joings
        print(data) #prints out said message
    
    data = client_socket.recv(1024).decode() #the game will send message "Welcome to the game!"
    print(data) #prints out previously said message
    
    
    data = client_socket.recv(1024).decode() #receives dragons actions
    print(data) #prints said mmessage
    
    while message.lower().strip() != 'bye': #user can type until user says goodbye
        while True:
            message = input(" -> ")  # take input that the player says for the action
            client_socket.send(message.encode()) # sends the input
            data = client_socket.recv(1024).decode()
            print(data)
            if(data[0:7] != 'Command'):
                break
        
        while True:
            data = client_socket.recv(1024).decode()  # receive player's current health
            print(data)
            if(data[0] == '['):
                break
    
    #client_socket.send(message) #send bye message
    client_socket.close()  # close the connection
if __name__ == '__main__':
    client_program()