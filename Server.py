# -*- coding: utf-8 -*-

import socket, BossDragon, Player, random

def messageAll(connected, msg):
    for x in connected:
        x.send(msg.encode())

def updateHealth(players):
    message = ""
    for x in players:
        string = "-" + x.getName() + ": " + x.getHealth() + "\n"
        message += str(string)
        
    return message

def commands (conn):
    commandHelp = "Commands:\n1 = attack\n2 = block"
    conn.send(commandHelp.encode())

def death(player, connections, defense):
    i = 0
    for p in player:
        if(p.getHealth() <= 0):
            p.send("Dead".encode())
            messageAll(connections, p.getName() + " has died")
            del(player[i])
            del(defense[i])
        else:
            i += 1
    
    return player, i

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
    
    amount = 1 #the amount of people that are within the server
    server_socket.listen(amount) #how many people will be connected
    addresses = [] #list of connections
    #names = [] #list of usernames that will correspond to addresses
    players = [] ###Testing
    i = 0 #the counter that will go through the list
    block = []
    
    while(len(addresses) != amount):
        conn, address = server_socket.accept()
        print("Connection from: " + str(address))
        username = conn.recv(1024).decode()
        print(username)
        #names.append(username)
        addresses.append(conn)
        players.append(Player.Player(100, username)) ###Testing
        block.append(False)
        messageAll(addresses, str(len(addresses)) + "/" + str(amount) + " players are connected")
    
    messageAll(addresses, "Welcome to the game!")
    print("Welcome to the game!")
    
    ###Everything below here is a test
    boss = BossDragon.BossDragon(100)
    while(boss.getHealth() > 0): #continues until dragon is defeated
        if(amount == 0): #alternate end, players are defeated
            break
        
        chosen = int(random.random() * amount) # random number from array to attack
        message = players[chosen].getName() + "'s turn"
        print(message)
        addresses[i%amount].send(message.encode())
        
       
        while(True): #this loop continuously receives actions
            action = addresses[i%amount].recv(1024).decode()
            print(action.lower().strip())
            
            if(str(action).lower().strip() == 'attack'):
                print(players[i%amount].attack())
                boss.lossHealth(players[i%amount].attack())
                break
            elif(str(action).lower().strip() == 'block'):
                block[i%amount] = True;
                break
            elif(str(action).lower().strip() == 'health'):
                updateHealth(players)
            else:
                commands(addresses[i%amount])
        
        message = "Boss: " + str(boss.getHealth())
        print(message)
        messageAll(addresses, message)
        if(players[chosen].getHealth() <= 0):
            players, amount = death(players, addresses)
        i += 1
        
        bossAction, damage = boss.dealDamage() # boss deals damage and says what was the attack
        if(block[chosen]):
            messageAll(addresses, "**" + players[chosen].getName() + " has blocked the attack and miligated the damage!")
            damage -= int(random.random()*10)
            block[chosen] = False
        players[chosen].takeDamage(int(damage)) # player now takes damage
        
        message = "The dragon used " + bossAction
        print(message + " on " + players[chosen].getName()) # prints out what the dragon did
        messageAll(addresses, message)
        message = "*" + players[chosen].getName() + ": " + str(players[chosen].getHealth())
        print(message) #prints out the player's new health
        addresses[chosen].send(message.encode())
        
    conn.close()  # close the connection

        
    
"""
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
"""

if __name__ == '__main__':
    server_program()



    