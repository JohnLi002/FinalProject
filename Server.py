# -*- coding: utf-8 -*-

import socket, BossDragon, Player, random, time

# Message All Connected Players
def messageAll(connected, msg):
    for x in connected:
        x.send(msg.encode())

# Display Current Health of Connected Players
def updateHealth(players):
    message = ""
    for x in players:
        string = "-" + x.getName() + ": " + x.getHealth() + "\n"
        message += str(string)
        
    return message

# Send Back List of Commands if Client Input is not allowed
def commands (conn):
    commandHelp = "Commands:\n1 = attack\n2 = block"
    conn.send(commandHelp.encode())

# Death Message
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


# Start Server Program
def server_program():  
    
    # Initalize Server Socket
    host = socket.gethostname()
    port = 5000  
    server_socket = socket.socket()  
    server_socket.bind((host, port))  
    
    # Max Clients Allowed
    amount = 1 
    
    # Listens and Takes in Client's connection and username
    server_socket.listen(amount) 
    addresses = [] 
    players = [] 
    
    # Counter to loop through connections
    i = 0 
    
    # Boolean Array if player is currently blocking
    block = []
    
    # Receive Connecting Players
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
    
    # Notify all players that game is starting
    messageAll(addresses, "Welcome to the game!")
    print("Welcome to the game!")
    
    ###Everything below here is a test
    
    # Initalize Boss
    boss = BossDragon.BossDragon(100)
    
    # Continue until boss health < 0
    while(boss.getHealth() > 0): 
        
        # Players are defeated, exit
        if(amount == 0): 
            break
        
        # Notify Start of Player's Turn
        chosen = int(random.random() * amount) # random number from array to attack
        time.sleep(1)
        message = players[chosen].getName() + "'s turn"
        print(message)
        addresses[i%amount].send(message.encode())
        
        # Receive Player Input
        while(True): 
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
        
        # Print Current Status of Boss to all players
        message = "Boss: " + str(boss.getHealth())
        print(message)
        messageAll(addresses, message)
        
        # If player dies, print death message to all players
        if(players[chosen].getHealth() <= 0):
            players, amount = death(players, addresses)
        
        # Loops through Connected Players
        i += 1
        
        # Boss Attacks
        bossAction, damage = boss.dealDamage() 
        
        # Player Block Sequence if currently blocking
        if(block[chosen]):
            messageAll(addresses, "**" + players[chosen].getName() + " has blocked the attack and miligated the damage!")
            damage -= int(random.random()*10)
            block[chosen] = False
        players[chosen].takeDamage(int(damage)) # player now takes damage
        
        # Prints Boss Actions to all players and current status of player affected.
        message = "The dragon used " + bossAction
        print(message + " on " + players[chosen].getName()) # prints out what the dragon did
        messageAll(addresses, message)
        
        # Prints Player Current Health and send status
        if players[chosen].getHealth() > 0:
            message = "*" + players[chosen].getName() + ": " + str(players[chosen].getHealth())
            print(message) 
            addresses[chosen].send(message.encode())
        else:
            message = "*" + players[chosen].getName() + ": Died!"
            print(message) 
            addresses[chosen].send(message.encode())
    
    conn.close()  # close the connection
# End Server Program
        
    
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