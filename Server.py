# -*- coding: utf-8 -*-

import socket
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
    server_socket.listen(2)
    addresses = []
    i = 0
    
    while True:
        conn, address = server_socket.accept()  # accept new connection
        print("Connection from: " + str(address))
        if(i < 2):
            addresses.append(conn)
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = addresses[i%2].recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
        data = input(' -> ')
        addresses[i%2].send(data.encode())  # send data to the client
        i += 1        


    conn.close()  # close the connection

if __name__ == '__main__':
    server_program()
