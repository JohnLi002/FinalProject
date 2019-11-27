import socket

def client_program():#'10.220.112.48'
    host = socket.gethostname()  # get IP address of server
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    # data = server string
    # message = client string
    
    finished = False #represents if player if done
    
    #create and send server the username based on user input
    username = "[" + input("Username: ") + "]"
    message = username 
    client_socket.send(message.encode()) #sends server the message
    
    data = client_socket.recv(1024).decode() #after join, there is an initial message of how you just joined
    print(data)
    
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
