# -*- coding: utf-8 -*-

import socket, BossDragon, Player, random, time

# Message Something to All Players 
def messageAll(connected, msg):
    for x in connected:
        x.send(msg.encode())

# Update Players Health
def updateHealth(players):
    message = ""
    for x in players:
        string = "-" + x.getName() + ": " + str(x.getHealth()) + "\n"
        message += str(string)
    return message

# If action illegal, send list of commands
def commands (conn): 
    commandHelp = "Commands:\n1 = attack\n2 = block\n3 = check health"
    conn.send(commandHelp.encode())

# Close player connection and notify Player's Death to all
def death(player, connections, defense):
    i = 0
    for p in player:
        if(p.getHealth() <= 0):
            connections[i].send("Dead".encode())
            messageAll(connections,"#" + p.getName() + " has died")
            del(player[i])
            del(defense[i])
            del(connections[i])
        else:
            i += 1
    return player, defense, connections

# Start Server Program
def server_program():
    
    # Initalize Server Socket
    host = socket.gethostname()
    port = 5000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    server_socket.bind((host, port))  #
    
    # Configure max allowed connections
    amount = int(input("How many players allowed? ")) 
    print("Waiting for connections...\n")
    server_socket.listen(amount) 
    
    # Counter to loop through connections
    i = 0 
    
    # Boolean Array if Player is currently blocking
    block = []
    
    # Initalize connections and player usernames
    connections = []
    players = []
    while(len(connections) != amount):
        
        # Get Connection and Username 
        conn, address = server_socket.accept()
        print("Connection from: " + str(address))
        username = conn.recv(1024).decode()
        print(username)
        connections.append(conn)
        
        ### Testing
        # Create Player Objects
        players.append(Player.Player(1, username)) 
        
        #Question: is the block function really a good idea?
        block.append(False) 
        
        # Message all players someone connected
        messageAll(connections, str(len(connections)) + "/" + str(amount) + " players are connected")
    
    # Message all players start of game
    messageAll(connections, "Welcome to the game!")
    print("Welcome to the game!")
    
    # Initalize Boss Object
    boss = BossDragon.BossDragon(100)
    
    # Continue until Boss Health is less than 0
    while(boss.getHealth() > 0):
        
        # Alternate end: Players are defeated, exit 
        if(amount == 0):
            break
        
        # Notify all clients whose turn it is
        time.sleep(1)
        message = players[i%amount].getName() + "'s turn"
        print(message)
        messageAll(connections,message)
        
        # Receive Player Action
        while True: 
            
            action = connections[i%amount].recv(1024).decode()
            print(action.lower().strip())
            
            if(str(action).lower().strip() == '1'):
                print(players[i%amount].attack())
                boss.lossHealth(players[i%amount].attack())
                break
            elif(str(action).lower().strip() == '2'):
                block[i%amount] = True;
                break
            elif(str(action).lower().strip() == '3'):
                connections[i%amount].send(updateHealth(players).encode())
            else:
                commands(connections[i%amount])
        
        # Notify all Boss Status
        time.sleep(1)
        message = "Boss: " + str(boss.getHealth())
        print(message)
        messageAll(connections, message)
        
        # Boss Action
        bossAction, damage = boss.dealDamage() 
        
        # Choose random player to attack
        chosen = int(random.random() * amount) 
        
        # If player is currently blocking, reduce damage
        if(block[chosen]):
            messageAll(connections, "**" + players[chosen].getName() + " has blocked the attack and miligated the damage!")
            damage -= int(random.random()*10)
            block[chosen] = False
        players[chosen].takeDamage(int(damage)) 
        
        # Make sure client is not overwhelmed 
        time.sleep(1)
        
        # Notify all Boss Action
        message = "The dragon used " + bossAction
        print(message + " on " + players[chosen].getName()) 
        messageAll(connections, message)
        
        # Make sure client is not overwhelmed 
        time.sleep(1)
        
        # Update Current Player's Status
        message = "*" + players[chosen].getName() + ": " + str(players[chosen].getHealth())
        print(message) 
        connections[chosen].send(message.encode())
        
        # Death Sequence if Player dies
        if(players[chosen].getHealth() <= 0):
            players, block, connections = death(players, connections, block)
            amount = len(connections)
        
        # Move on to Next Player
        i += 1
        
    # Close Connection
    conn.close()  
# End Server Program

if __name__ == '__main__':
    server_program()
