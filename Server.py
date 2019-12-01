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

def playerActions(connections, Players, num, attdebuff, defdebuff):
    job = Players[num].getClass().lower().strip()
    damage = 0
    message = ''
    
    while(True):
        action = connections[num].recv(1024).decode()

        if(job == 'ranger'):
            if(action.lower().strip() == '1'): #sharp shot
                damage = Players[num].sharpShot()
                message = Players[num].getName() + " used [Sharp Shot]!"
                break
            elif(action.lower().strip() == '2'): #crippling shot
                message = Players[num].getName() + " used [Collapsing Shot]! \nBoss's attack decreased!"
                damage = Players[num].cripplingShot()
                attdebuff.append(3)
                break
            elif(action.lower().strip == '3'): #collapsing shot
                message = Players[num].getName() + " used [Collapsing Shot]! \nBoss's defense decreased!"
                damage = Players[num].collapsingShot()
                defdebuff.append(3)
                break
            else:
                connections[num].send(Players[num].getSkillList().encode())
        elif(job == 'thief'):
            if(action.lower().strip() == '1'): #poison coat
                message = (Players[num].getName() + " used [Poison Coat]! \nHe prepares his next attack")
                break
            elif(action.lower().strip() == '2'): #swift strike
                print('Swift Strike')
                break
            elif(action.lower().strip == '3'): #smoke bomb
                print('Smoke Bomb')
                break
            else:
                connections[num].send(Players[num].getSkillList().encode())
        elif(job == 'guardian'):
            if(action.lower().strip() == '1'): #taunt
                print('Taunt')
                break
            elif(action.lower().strip() == '2'): #shield bash
                print('Shield Bash')
                break
            elif(action.lower().strip == '3'): #protection
                print('Protection')
                break
            else:
                connections[num].send(Players[num].getSkillList().encode())
        else: #The remaining class must be priest
            if(action.lower().strip() == '1'): #heal
                print('Heal')
                break
            elif(action.lower().strip() == '2'): #holy glade
                print('Holy Glader')
                break
            elif(action.lower().strip == '3'): #stat boost
                print('Stat Boost')
                break
            else:
                connections[num].send(Players[num].getSkillList().encode())
    
    messageAll(connections, message)
    return Players, attdebuff, defdebuff, damage

def newDamage(damage, debuffs):
    for x in debuffs:
        damage -= x
    
    return damage

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
    attDebuff = []
    defDebuff = []
    
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
    if(i%amount == 0):
            attDebuff.clear()
            defDebuff.clear()
    while(boss.getHealth() > 0): #continues until dragon is defeated
        if(amount == 0): #alternate end, no players left
            print("All players defeated")
            break
        
        #prints out whose turn it is
        time.sleep(1)
        message = players[i%amount].getName() + "'s turn"
        print(message)
        messageAll(connections,message)
        
        
        #this loop continuously receives actions
        players, attDebuff, defDebuff, damage = playerActions(connections, players, i%amount, attDebuff, defDebuff)
        boss.lossHealth(damage)
            
        time.sleep(1)
        message = "Boss: " + str(boss.getHealth())
        print(message)
        messageAll(connections, message)
        
        
        bossAction, damage = boss.dealDamage() # boss deals damage and says what was the attack
        
        #random number to chose Boss's target
        chosen = int(random.random() * amount) 

        #deals damage to player
        players[chosen].takeDamage(newDamage(damage, attDebuff)) # player now takes damage
        time.sleep(1) #to make sure the client is not overwelmed
        
        #prints out bosses actions and results
        message = "The dragon used " + bossAction
        print(message + " on " + players[chosen].getName()) # prints out what the dragon did
        messageAll(connections, message)
        time.sleep(1)
        message = "*" + players[chosen].getName() + ": " + str(players[chosen].getHealth())
        print(message) #prints out the player's new health
        messageAll(connections, message)
        
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


