import socket, random

def messageAll(connected, msg):
    for x in connected:
        x.send(msg.encode())

def check(connected, check):
    for x in connected:
        if x is check:
            return True
    print("something")
    return False

def server_program():
    # Server Socket
    host = socket.gethostname()
    port = 5000  
    server_socket = socket.socket()  
    server_socket.bind((host, port))  
    
    amount = int(input("How many people allowed: ")) 
    server_socket.listen(amount) 
    
    addresses = [] #list of connections
    names = [] #list of usernames that will correspond to addresses
    
    i = 0 #the counter that will go through the list
       
    # Receives all players
    while(len(addresses) != amount):
        conn, address = server_socket.accept()
        print("Connection from: " + str(address))
        username = conn.recv(1024).decode()
        print(username)
        names.append(username)
        addresses.append(conn)
        messageAll(addresses, str(len(addresses)) + "/" + str(amount) + " people are connected")
    
    messageAll(addresses, "Welcome to the game!")
    print("Welcome to the game!")
   
    
    # While players are still in game
    while amount > 0: 
        
        data = addresses[i%amount].recv(1024).decode()
        if not data:
            # if data is not received break
            break
        if data == 'bye': #if a user leaves
            globalMsg = "[" + names[i%amount] + "] has left the server"
            print(globalMsg)
            del(names[i%amount])
            del(addresses[i%amount])
            amount -= 1
            messageAll(addresses, globalMsg)
        else:
            print("from [" + names[i%amount] + "]: " + str(data))
            data = input(' >>>>>> ')
            addresses[i%amount].send(data.encode())  # send data to the client
            i += 1

    conn.close()  # close the connection

if __name__ == '__main__':
    server_program()



    