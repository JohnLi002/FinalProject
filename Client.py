"""
@author: John Li, John Khuc, Tony Lei
"""

import socket

def client_program():
    host = socket.gethostname()  # get IP address of server
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    # data = server string
    # message = client string
    
    loss = False #represents boss victory
    victory = False #represent player victory
    #create and send server the username based on user input
    username = "[" + input("Username: ") + "]"
    message = username 
    client_socket.send(message.encode()) #sends server the message
    
    data = client_socket.recv(1024).decode() #after join, there is an initial message of how you just joined
    print(data)
    
    #############################
    
    while True:
        job = input("Choose your job: ")
        client_socket.send(job.encode())
        
        data = client_socket.recv(1024).decode()
        if(data == "received"):
            break
        
    ######################
    #waits until the server is finished filling up with players
    while(data[0] != data[2]):
        data = client_socket.recv(1024).decode() 
        print(data)
    
    #receive and print welcome message
    data = client_socket.recv(1024).decode() 
    print(data)
    
    #receives and prints out whose initial turn initial turn
    data = client_socket.recv(1024).decode() 
    print(data) 
    
    while True: #This loop continues the game
        if loss: #checks to see if you are dead, if you are the loop ends and the socket is closed
            print("The dragon has killed you")
            client_socket.close()
            break
        elif victory:
            client_socket.close()
            break
        
        #Checks to see if it is the clients turn. If it is, they will have the ability to chose their actions
        if(data[0:len(username)] == username): 
            while True:
                message = input(" -> ")  # take input that the player says for the action
                client_socket.send(message.encode()) # sends the input
                data = client_socket.recv(1024).decode()
                print(data)
                
                #If there is a return that isn't a command or given health, break loop
                if(data[0:6] != 'Skills' and data[0] != '-' and data[0:6] != 'Choose' and data[0:3] != 'Who'): 
                    break
        
        #continuously loops until there is a message about another person's turn
        while True:
            data = client_socket.recv(1024).decode()
            
            #If the user gets a special message telling the client that they are dead
            if(data == 'Dead'): 
                loss = True #Makes this boolean true
                data = client_socket.recv(1024).decode() #prints next message
                print(data) 
                break #breaks this loop
            elif (data == 'You have won!'):
                victory = True
                print(data)
                break
            
            print(data)
            if(data[0] == '['): #checks to see if message is a net turn message by identifying the '['
                break
    
    
if __name__ == '__main__':
    client_program()
