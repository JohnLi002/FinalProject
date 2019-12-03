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


def death(player, connections):
    i = 0
    for p in player:
        if(p.getHealth() <= 0):
            connections[i].send("Dead".encode())
            messageAll(connections,"#" + p.getName() + " has died")
            del(player[i])
            del(connections[i])
        else:
            i += 1
    
    return player, connections

def playerActions(connections, Players, num, attdebuff, attTimer, defdebuff, defTimer, taunt):
    damage = 0
    message = ''
    num = num%len(connections)
    job = Players[num].getClass().lower().strip()

    while(True):
        action = connections[num].recv(1024).decode()

        if(job == 'ranger'):
            if(action.lower().strip() == '1'): #sharp shot
                damage = Players[num].sharpShot()
                message = Players[num].getName() + " used [Sharp Shot]!"
                print('Sharp Shot')
                break
            elif(action.lower().strip() == '2'): #crippling shot
                message = Players[num].getName() + " used [Crippling Shot]! \nBoss's attack decreased!"
                damage = Players[num].cripplingShot()
                attdebuff.append(3)
                attTimer.append(0)
                print('Crippling Shot')
                break
            elif(action.lower().strip() == '3'): #collapsing shot
                message = Players[num].getName() + " used [Collapsing Shot]! \nBoss's defense decreased!"
                damage = Players[num].collapsingShot()
                defdebuff.append(3)
                defTimer.append(0)
                print('collapsing shot')
                break
            else:
                connections[num].send(Players[num].getSkillList().encode())
        elif(job == 'thief'):
            if(action.lower().strip() == '1'): #poison coat
                message = (Players[num].getName() + " used [Poison Coat]! \nHe prepares his next attack!")
                print('Poison Coat')
                break
            elif(action.lower().strip() == '2'): #swift strike
                message = Players[num].getName() + " used [Swift Strike]!"
                damage = Players[num].swiftStrike()
                print('Swift Strike')
                break
            elif(action.lower().strip() == '3'): #smoke bomb
                attdebuff.append(-5)
                attTimer.append(0)
                message = Players[num].getName() + " used [Smoke Bomb]! \nThe bosses attack has weakened!"
                print('Smoke Bomb')
                break
            else:
                connections[num].send(Players[num].getSkillList().encode())
        elif(job == 'guardian'):
            if(action.lower().strip() == '1'): #taunt
                taunt = num
                message = Players[num].getName() + " used [Taunt]! \nThe boss is now focused on him!"
                print('Taunt')
                break
            elif(action.lower().strip() == '2'): #shield bash
                damage = Players[num].shieldBash()
                message = Players[num].getName() + " used [Shield Bash]!"
                print('Shield Bash')
                break
            elif(action.lower().strip() == '3'): #protection
                Players[num].protection()
                message = Players[num].getName() + " used Protection! \nThey prepare themselves for the enxt blow"
                print('Protection')
                break
            else:
                connections[num].send(Players[num].getSkillList().encode())
        else: #The remaining class must be priest
            if(action.lower().strip() == '1'): #heal
                print('Heal')
                connections[num].send('Who do you want to heal?'.encode())
                while(True):
                    person = connections[num].recv(1024).decode().lower().strip()
                    for x in Players:
                        if(person == x.getName()):
                            x = Players[num].statBoost(x)
                            message = 'healed'
                            break
                    if(message == 'healed'):
                        message = Players[num].getName() + " has healed " + person + "!"
                        break
                    else:
                        message = "Choose valid players:"
                        for x in Players:
                            message += "\n" + x.getName()
                        connections[num].send(message.encode())
                
                break
            elif(action.lower().strip() == '2'): #holy glade
                damage = Players[num].holyGlader()
                message = Players[num].getName() + " used [Holy Glade]!"
                print('Holy Glader')
                break
            elif(action.lower().strip() == '3'): #stat boost
                print('Stat Boost')
                connections[num].send('Who do you want to buff?'.encode())
                while(True):
                    person = connections[num].recv(1024).decode().lower().strip()
                    for x in Players:
                        if(person == x.getName()):
                            x = Players[num].statBoost(x)
                            message = 'buffed'
                            break
                    if(message == 'buffed'):
                        message = Players[num].getName() + " has buffed " + person + "!"
                        break
                    else:
                        message = "Choose valid players:"
                        for x in Players:
                            message += "\n" + x.getName()
                        connections[num].send(message.encode())
                break
            else:
                connections[num].send(Players[num].getSkillList().encode())
    
    messageAll(connections, message)
    return Players, attdebuff, attTimer, defdebuff, defTimer, damage, taunt

def newDamage(damage, debuffs):
    for x in debuffs:
        damage -= x
        
    if damage < 0:
        damage = 0
    
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
    
    #debuffs
    attDebuff = []
    attTimer = []
    defDebuff = []
    defTimer = []
    taunt = -1
    
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
        time.sleep(1)
        messageAll(connections, username + " the " + players[len(players) - 1].getClass() + " has joined!")
        time.sleep(1)
        messageAll(connections, str(len(connections)) + "/" + str(amount) + " players are connected")
        time.sleep(1)
        
    
    #Welcome message sent to all players
    messageAll(connections, "Welcome to the game!")
    print("Welcome to the game!")
    
    #initialize the boss/enemy/Boss Object
    boss = BossDragon.BossDragon(100)
    while(boss.getHealth() > 0): #continues until dragon is defeated
        if(amount == 0): #alternate end, no players left
            print("All players defeated")
            break
        
        #calculates duration of debuffs
        if(i%amount == 0):
            ### Attack Debuffs
            place = 0
            
            while place < len(attTimer):
                attTimer[place] += 1
                place += 1
            
            # Delete expired attack debuff
            place = 0
            while True:
                if(place == len(attTimer)):
                    break
                if(attTimer[place] == 3):
                    del(attTimer[place])
                else:
                    place += 1
                
            ## Printing out attack Debuffs
            place = 0
            while place < len(attTimer):
                print(str(attTimer[place]) + "/2 turns | " + str(attDebuff[place]) + " decrease to att")
                place += 1
            
            
            ### Defense Debuffs
            place = 0
            while place < len(defTimer):
                defTimer[place] += 1
                place += 1
                
            place = 0
            while True:
                if(place == len(defTimer)):
                    break
                if(defTimer[place] == 3):
                    del(defTimer[place])
                else:
                    place += 1
            
            
            place = 0
            while place < len(defTimer):
                print(str(defTimer[place]) + "/2 turns | " + str(defDebuff[place]) + " decrease to att")
                place += 1
            

                    
        #prints out whose turn it is
        time.sleep(1)
        message = players[i%amount].getName() + "'s turn"
        print(message)
        messageAll(connections,message)
        
        
        #this loop continuously receives actions
        players, attDebuff, attTimer, defDebuff, defTimer, damage, taunt = playerActions(connections, players, i, attDebuff, attTimer, defDebuff, defTimer, taunt)
        boss.lossHealth(damage)
        
        
        time.sleep(1)
        message = "Boss: " + str(boss.getHealth())
        print(message)
        messageAll(connections, message)
        
        if(boss.getHealth() <= 0):
            break
        
        #extra damage from debuffs
        for x in defDebuff:
            damage += x
        
        bossAction, damage = boss.dealDamage() # boss deals damage and says what was the attack
        
        #random number to chose Boss's target
        chosen = int(random.random() * amount) 
        
        #taunt changes target
        if(taunt != -1):
            chosen = taunt
            if(i%amount == 0):
                taunt = -1
       
        time.sleep(1) #to make sure the client is not overwelmed
        
        #prints out bosses actions and results
        message = "The dragon used " + bossAction
        print(message + " on " + players[chosen].getName()) # prints out what the dragon did
        messageAll(connections, message)
        time.sleep(1)
        
         
        #deals damage to player
        damage = newDamage(damage, attDebuff)
        
        #New damage with guardian class
        if(players[chosen].getClass() == 'guardian'):
            damage -= players[chosen].defending()
            messageAll(connections, "- " + players[chosen].getName() + " has mitigated the damage")
            if(damage < 0):
                damage = 0
            time.sleep(1)
        
        players[chosen].takeDamage(damage) # player now takes damage
        
        message = "*" + players[chosen].getName() + ": " + str(players[chosen].getHealth())
        print(message) #prints out the player's new health
        messageAll(connections, message)
        
        #checks for death
        if(players[chosen].getHealth() <= 0):
            players, connections = death(players, connections)
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



    