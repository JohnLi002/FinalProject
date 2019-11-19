# -*- coding: utf-8 -*-

import socket

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
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024
    # create the socket
    # AF_INET == ipv4         ipv6 == AF_INET6
    # SOCK_STREAM == TCP      SOCK_DGRAM == UDP
    #socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together
    # configure how many client the server can listen simultaneously
    
    amount = 2 #the amount of people that are within the server
    server_socket.listen(amount) #how many people will be connected
    addresses = [] #list of connections
    names = [] #list of usernames that will correspond to addresses
    i = 0 #the counter that will go through the list
    
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
    
    
    
    while amount > 0: #while people are within the server
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
            data = input(' >>>[You]: ')
            addresses[i%amount].send(data.encode())  # send data to the client
            i += 1

    conn.close()  # close the connection

if __name__ == '__main__':
    server_program()



    