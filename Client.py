import socket

def client_program():#'10.220.112.48'
    host = socket.gethostname()  # get IP address of server
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    # data = server string
    # message = client string
    
    finished = False
    username = "[" + input("Username: ") + "]" # take input which will be the username associated with the host
    message = username #the username is now the input
    client_socket.send(message.encode()) #sends server the message
    
    data = client_socket.recv(1024).decode() #after join, there is an initial message of how you just joined
    print(data)
    
    while(data[0] != data[2]): #Within the joining message the 1st and 3rd parts there are numbers 
                               #that represent the queue. If the numbers are the same, the queue is filled
        data = client_socket.recv(1024).decode()  # receive any othere joining messages which appear every time someone joings
        print(data) #prints out said message
    
    data = client_socket.recv(1024).decode() #the game will send message "Welcome to the game!"
    print(data) #prints out previously said message
    
    
    data = client_socket.recv(1024).decode() #receives whose turn it is initially
    print(data) #prints said mmessage
    
    while True: #This loop continues the game
        if finished: #checks to see if you are dead, if you are the loop ends and the socket is closed
            print("The dragon has killed you")
            client_socket.close()
            break
        #At the very start the server returns whose turn it is. The client identifies if it is
        #their turn by checking if the first part of the message is their name. If it is their
        #name then then they are allowed actions
        if(data[0:len(username)] == username): 
            while True:
                message = input(" -> ")  # take input that the player says for the action
                client_socket.send(message.encode()) # sends the input
                data = client_socket.recv(1024).decode()
                print(data)
                if(data[0:7] != 'Command' and data[0] != '-'): #If there is a return that isn't a command or given health, break loop
                    break
        
        while True:
            data = client_socket.recv(1024).decode()  #messages and continues until the next turn is identified
            
            if(data == 'Dead'): #If the player is attacked and dies, the client picks up this special message
                finished = True #Makes this boolean true
                data = client_socket.recv(1024).decode() #prints next message
                print(data) 
                break #ends this loop to restart the bigger while loop
            
            print(data)
            if(data[0] == '['): #The client identifies the '[' to understands if it is the next turn
                break
    
    #client_socket.send(message) #send bye message
    #client_socket.close()  # close the connection
    
if __name__ == '__main__':
    client_program()
