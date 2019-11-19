import socket

def client_program():
    # Client Socket
    host = socket.gethostname()  
    port = 5000  
    client_socket = socket.socket()  
    client_socket.connect((host, port))  

    # Enter the game
    message = input("Username: ")  
    client_socket.send(message.encode())
    
    
    
    data = client_socket.recv(1024).decode()  # receive response
    print(data)
    
    #
    while(data[0] != data[2]):
        data = client_socket.recv(1024).decode()  
        print(data)
    
    
    while message.lower().strip() != 'bye':
        data = client_socket.recv(1024).decode()  # receive response
        
        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input
        client_socket.send(message.encode())

    client_socket.close()  


if __name__ == '__main__':
    client_program()
