# -*- coding: utf-8 -*-
"""
@author John Li
"""
import socket, BossDragon, Player, random, time

def messageAll(connected, msg):
    for x in connected:
        x.send(msg.encode())

def updateHealth(players):
    message = ""
    for x in players:
        string = "-" + x.getName() + ": " + str(x.getHealth()) + "\n"
        message += str(string)
        
    return message

def commands (conn):
    commandHelp = "Commands:\n1 = attack\n2 = block"
    conn.send(commandHelp.encode())

def death(player, connections, defense):
    i = 0
    for p in player:
        if(p.getHealth() <= 0):
            connections[i].send("Dead".encode())
            messageAll(connections, p.getName() + " has died")
            del(player[i])
            del(defense[i])
        else:
            i += 1
    
    return player, i, defense

def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000
    server_socket = socket.socket()  # get instance
    server_socket.bind((host, port))  # bind host address and port together
    # configure how many client the server can listen simultaneously
    
    amount = 1 #the amount of people that are within the server
    server_socket.listen(amount) #how many people will be connected at once. This counter closes when a socket closes
    connections = [] #list of connections
    #names = [] #list of usernames that will correspond to addresses
    players = [] ###Testing
    i = 0 #the counter that will go through the list
    block = []
    
    while(len(connections) != amount):
        conn, address = server_socket.accept()
        print("Connection from: " + str(address))
        username = conn.recv(1024).decode()
        print(username)
        #names.append(username)
        connections.append(conn)
        players.append(Player.Player(1, username)) ###Testing
        block.append(False) #question is the block function really a good idea?
        messageAll(connections, str(len(connections)) + "/" + str(amount) + " players are connected")
    
    messageAll(connections, "Welcome to the game!")
    print("Welcome to the game!")
    
    ###Everything below here is a test
    boss = BossDragon.BossDragon(100)
    while(boss.getHealth() > 0): #continues until dragon is defeated
        if(amount == 0): #alternate end, players are defeated
            break
        
        chosen = int(random.random() * amount) # random number from array to attack
        time.sleep(1)
        message = players[chosen].getName() + "'s turn"
        print(message)
        connections[i%amount].send(message.encode())
        
       
        while(True): #this loop continuously receives actions
            action = connections[i%amount].recv(1024).decode()
            print(action.lower().strip())
            
            if(str(action).lower().strip() == 'attack'):
                print(players[i%amount].attack())
                boss.lossHealth(players[i%amount].attack())
                break
            elif(str(action).lower().strip() == 'block'):
                block[i%amount] = True;
                break
            elif(str(action).lower().strip() == 'health'):
                connections[i%amount].send(updateHealth(players).encode())
            else:
                commands(connections[i%amount])
        
        message = "Boss: " + str(boss.getHealth())
        print(message)
        messageAll(connections, message)
        
        
        bossAction, damage = boss.dealDamage() # boss deals damage and says what was the attack
        if(block[chosen]):
            messageAll(connections, "**" + players[chosen].getName() + " has blocked the attack and miligated the damage!")
            damage -= int(random.random()*10)
            block[chosen] = False
        players[chosen].takeDamage(int(damage)) # player now takes damage
        time.sleep(1) #to make sure the client is not overwelmed
        
        message = "The dragon used " + bossAction
        print(message + " on " + players[chosen].getName()) # prints out what the dragon did
        messageAll(connections, message)
        
        time.sleep(1)
        message = "*" + players[chosen].getName() + ": " + str(players[chosen].getHealth())
        print(message) #prints out the player's new health
        
        connections[chosen].send(message.encode())
        if(players[chosen].getHealth() <= 0):
            players, amount, block = death(players, connections, block)
        i += 1
        
    conn.close()  # close the connection

if __name__ == '__main__':
    server_program()



    