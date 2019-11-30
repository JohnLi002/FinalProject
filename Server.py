# -*- coding: utf-8 -*-
"""
@author John Li
"""
import socket, BossDragon, random, time, Guardian, Ranger, Priest, Thief



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
    commandHelp = "Commands:\n1 = attack\n2 = block\n3 = check health"
    conn.send(commandHelp.encode())

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

def playerActions(connections, Players, num, debuffs):
    job = Players[num].getClass()
    damage = 0
    while(True):
        action = connections[num].recv(1024).decode()

        if(job == 'ranger'):
            if(action.lower().strip() == '1'):
                print('Sharp Shot')
                break
            elif(action.lower().strip() == '2'):
                print('crippling shot')
                break
            elif(action.lower().strip == '3'):
                print('collapsing shot')
                break
            else:
                connections[num].send(Players[num].getSkillList().encode())
        elif(job == 'thief'):
            if(action.lower().strip() == '1'):
                print('Poison Coat')
                break
            elif(action.lower().strip() == '2'):
                print('Swift Strike')
                break
            elif(action.lower().strip == '3'):
                print('Smoke Bomb')
                break
            else:
                connections[num].send(Players[num].getSkillList().encode())
        elif(job == 'guardian'):
            if(action.lower().strip() == '1'):
                print('Taunt')
                break
            elif(action.lower().strip() == '2'):
                print('Shield Bash')
                break
            elif(action.lower().strip == '3'):
                print('Protection')
                break
            else:
                connections[num].send(Players[num].getSkillList().encode())
        else: #The remaining class must be priest
            if(action.lower().strip() == '1'):
                print('Heal')
                break
            elif(action.lower().strip() == '2'):
                print('Holy Glader')
                break
            elif(action.lower().strip == '3'):
                print('Stat Boost')
                break
            else:
                connections[num].send(Players[num].getSkillList().encode())
    
    return Players, debuffs, damage

def server_program():
    # Server Socket
    host = socket.gethostname()
    port = 5000
    server_socket = socket.socket()  # get instance
    server_socket.bind((host, port))  # bind host address and port together
    
     # Configure max allowed connections
    amount = int(input("How many players allowed? ")) 
    print("Waiting for connections...\n")
    server_socket.listen(amount) 
    
    #the counter that will go through the list
    i = 0
    
    #boolean to see if player is currenlty blocking
    block = []
    bossDebuffAtk = [] #decreases the boss's attack
    bossDebuffDef = [] #decreases the boss's defense
    
    #Initialize connections
    connections = []
    players = []
    while(len(connections) != amount):
        conn, address = server_socket.accept()
        print("Connection from: " + str(address))
        username = conn.recv(1024).decode()
        print(username)
        
        #configure arrays to adjust to new players
        connections.append(conn)
        while True:
            connections[len(connections) - 1].send("Chose between these classes: Thief, Ranger, Guardian, Priest".encode())
            message = connections[len(connections)-1].recv(1024).decode()
            if(message.lower().strip() == 'thief'):
                players.append(Thief.Thief(100, username))
                break
            elif(message.lower().strip() == 'ranger'):
                players.append(Ranger.Ranger(100, username))
                break
            elif(message.lower().strip() == 'guardian'):
                players.append(Guardian.Guardian(100, username))
                break
            elif(message.lower().strip() == 'priest'):
                players.append(Priest.Priest(100, username))
                break
        
        connections[len(connections) -1].send("received".encode())
        block.append(False)
        messageAll(connections, str(len(connections)) + "/" + str(amount) + " players are connected")
        
    time.sleep(1)
    
    #Welcome message sent to all players
    messageAll(connections, "Welcome to the game!")
    print("Welcome to the game!")
    
    #initialize the boss/enemy/Boss Object
    boss = BossDragon.BossDragon(100)
    while(boss.getHealth() > 0): #continues until dragon is defeated
        if(i%amount == 0):
            bossDebuffAtk.clear()
            bossDebuffDef.clear()
        if(amount == 0): #alternate end, no players left
            print("All players defeated")
            break
        
        #prints out whose turn it is
        time.sleep(1)
        message = players[i%amount].getName() + "'s turn"
        print(message)
        messageAll(connections,message)
        
        
        while(True): #this loop continuously receives actions
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
        
        time.sleep(1)
        message = "Boss: " + str(boss.getHealth())
        print(message)
        messageAll(connections, message)
        
        
        bossAction, damage = boss.dealDamage() # boss deals damage and says what was the attack
        
        #random number to chose Boss's target
        chosen = int(random.random() * amount) 

        #check if targeted player is blocking
        if(block[chosen]):
            messageAll(connections, "**" + players[chosen].getName() + " has blocked the attack and miligated the damage!")
            damage -= int(random.random()*10)
            block[chosen] = False
            
        #deals damage to player
        players[chosen].takeDamage(int(damage)) # player now takes damage
        time.sleep(1) #to make sure the client is not overwelmed
        
        #prints out bosses actions and results
        message = "The dragon used " + bossAction
        print(message + " on " + players[chosen].getName()) # prints out what the dragon did
        messageAll(connections, message)
        time.sleep(1)
        message = "*" + players[chosen].getName() + ": " + str(players[chosen].getHealth())
        print(message) #prints out the player's new health
        messageAll(connections, message)
        #connections[chosen].send(message.encode())
        
        #checks for death
        if(players[chosen].getHealth() <= 0):
            players, block, connections = death(players, connections, block)
            amount = len(connections)
        else:
            i += 1
        
    #message if players have won
    if(amount != 0):
        print("Players have won!")
        messageAll(connections, "You have won!")
    
    conn.close()  # close the connection

if __name__ == '__main__':
    server_program()



    