#A game of yahtzee
import random

class Player:
    def __init__(self, name):
        self.name = name 
        self.scoreCard = {"Ones":None,"Twos":None,"Threes":None,"Fours":None,"Fives":None,"Sixes":None,"3 of a Kind":None,"4 of a Kind":None,"Full house":None,"SM Straight":None,"LG Straight":None,"Yahtzee":None,"Chance":None,"Yahtzee Bonus":0}
    
    def rollDice(self):
        dice=[random.randint(1,6),random.randint(1,6),random.randint(1,6),random.randint(1,6),random.randint(1,6)] #random roll
        i = 0
        while i < 2: #Allows you to re-roll twice
            print("DICE ROLL #"+str(i+1))
            print("==================")
            print(dice)
            print("What would you like to do?\n1. Re-roll All\n2. Re-roll Some\n3. Keep All\n4. Sort Dice\n5. See Scorecard")
            choice = ""
            while not choice.isnumeric() or int(choice)>3 or int(choice)<1: ##makes sure input is valid
                choice = input()
                if choice == "4":
                    dice.sort()
                    print(dice)
                    print("What would you like to do?\n1. Re-roll All\n2. Re-roll Some\n3. Keep All\n4. Sort Dice\n5. See Scorecard")
                if choice == "5": ##displays scorecard without interatiting rolls
                    self.displayScoreCard()
                    print("What would you like to do?\n1. Re-roll All\n2. Re-roll Some\n3. Keep All\n4. Sort Dice\n5. See Scorecard")
            if choice=="1":
                dice=[random.randint(1,6),random.randint(1,6),random.randint(1,6),random.randint(1,6),random.randint(1,6)] #New Roll
            elif choice =="2":
                print("Enter the value of the dice you want to re-roll. Enter -1 to re-roll")
                print(dice)
                choice = ""
                while choice != "-1":
                    choice=input()
                    if choice.isnumeric() and int(choice) in dice: #has user remove dice they don't want
                        dice.remove(int(choice))
                        print(dice)
                        
                while len(dice)<5:
                    dice.append(random.randint(1,6)) #adds new dice
                    
            elif choice == "3": #exits the reroll loop and goes straight to options
                break
            i+=1
        print("\nFINAL DICE ROLL")
        print("==================")
        print(dice)
        self.getOptions(dice)
    

    def getOptions(self, dice):
        options = []
        upper = ["Ones","Twos","Threes","Fours","Fives","Sixes"] #keys to iterate with
        threeOfKind = False #had to use variables so i wouldn't have to recheck later
        fourOfKind = False #this is more efficient because variable changes are O(1)
        yahtzee = False 
        fullHouse = False
        sum = 0 
        trueOption = 0
        for i in range (1,len(upper)+1): #interates through 1-6 getting the count
            numCount = dice.count(i)     #finds the count of each number
            sum += numCount*i            #also finds the sum
            if numCount != 0:
                trueOption+=1
            if (not self.scoreCard[upper[i-1]]) and numCount!= 0 and not self.scoreCard[upper[i-1]] == 0:  #is this O(n^2)?
                options.append([upper[i-1],i*numCount])   #if it's not 0 then it adds it as an option
            if numCount == 5: yahtzee = True              #vv just so we don't have to make extra calls we test for everything
            if numCount >= 4: fourOfKind = True
            if numCount == 3: threeOfKind = True
        if trueOption == 2 and threeOfKind:             #if len is two and there is a three of a kidn then there is a pair
            fullHouse = True
        if (threeOfKind or fourOfKind) and not self.scoreCard['3 of a Kind'] and not self.scoreCard['3 of a Kind'] == 0: options.append(["3 of a Kind",sum])
        if fourOfKind and not self.scoreCard['4 of a Kind'] and not self.scoreCard['4 of a Kind'] == 0: options.append(["4 of a Kind",sum])
        if fullHouse and not self.scoreCard['Full house'] and not self.scoreCard['Full house'] == 0: options.append(["Full house",25])
        if not threeOfKind:                               #will optomize by preventing unecessary O(n) (although it's not that important)
            dice = set(dice) #removes dupes cause not needed for straight
            diceStr = ''.join([str(elem) for elem in dice])
            if ('1234'in diceStr or '2345' in diceStr or '3456' in diceStr) and not self.scoreCard['SM Straight'] and not self.scoreCard['SM Straight'] == 0:
                options.append(["SM Straight",30]) #looks for all instaces of a small straight^
            if ('12345'in diceStr or '23456' in diceStr) and not self.scoreCard['LG Straight'] and not self.scoreCard['LG Straight'] == 0:
                options.append(["LG Straight",40]) #all instances of a large straight ^^
        if yahtzee and not self.scoreCard['Yahtzee'] == 0: #The 3 checks it goes through are 1.is it valid 2. has it been done 3. has it been scratched
            if not self.scoreCard['Yahtzee']:
                options.append(["Yahtzee",50])
            else: 
                options.append(["Yahtzee Bonus",100]) 
        if not self.scoreCard['Chance'] and not self.scoreCard['Chance'] == 0:
            options.append(["Chance",sum])
        options.append(['Scratch',0])
        self.displayOptions(options)

    def displayOptions(self,options):
       
        print("What do you want to do?")
        for i in range(1,len(options)+1):
            print(f'{str(i)+": "+options[i-1][0]:15} ==> {options[i-1][1]:3} points') #adds all the options starting from 1 because it looks better
        choice = ""
        while(not choice.isnumeric()) or (int(choice)<1 or int(choice)>=len(options)+1):
            choice = input() #valid input
        choice = int(choice)-1
        print('\n')
        if(options[choice][0]=='Scratch'):
            options = []
            count = 1
            print("What do you want to Scratch?")
            for option in self.scoreCard:
                if not self.scoreCard[option] and not self.scoreCard[option]==0 and not option == "Yahtzee Bonus":
                    print(str(count)+": "+ option) #displaying options
                    options.append(option)
                    count +=1
            choice = ""
            while(not choice.isnumeric()) or (int(choice)<1 or int(choice)>len(options)):
                choice = input()
            choice = int(choice)-1 #shifting choice by 1 to react
            self.scoreCard[options[choice]] = 0
            print('\n')
        elif options[choice][0]=='Yahtzee Bonus':
             self.scoreCard["Yahtzee Bonus"]+=100
        else:
            self.scoreCard[options[choice][0]]=options[choice][1]
        self.displayScoreCard()
        

    def displayScoreCard(self):
        print(" "+self.name)
        for key in self.scoreCard:
            print(f'{"|"+key:14}| {"" if (not self.scoreCard[key]) and not self.scoreCard[key]==0 else self.scoreCard[key]:3} |')
        print('\n')
    
    def canPlay(self):
        return None in self.scoreCard.values()

    
    def calculateScore(self):
        upper = ["Ones","Twos","Threes","Fours","Fives","Sixes"]
        lower = ["3 of a Kind", "4 of a Kind", "Full house", "SM Straight", "LG Straight","Yahtzee","Chance","Yahtzee Bonus"]
        upperTotal = 0
        lowerTotal = 0
        for key in upper: upperTotal += self.scoreCard[key] if self.scoreCard[key] else 0
        for key in lower: lowerTotal += self.scoreCard[key] if self.scoreCard[key] else 0
        upperBonus = 35 if upperTotal >= 63 else 0
        print(self.name+"'s Score")
        print("Upper score: "+str(upperTotal))
        print("Bonus: "+str(upperBonus))
        print("Upper Total: "+str(upperBonus+upperTotal))
        print("Lower Total: "+str(lowerTotal))
        print("Total: "+str(upperBonus+upperTotal+lowerTotal))
        return(upperBonus+upperTotal+lowerTotal)

playerNum = ""
while not playerNum.isnumeric() or not int(playerNum)>0:
    playerNum=input("Enter the number of players: ")

players = []
while len(players)<(int(playerNum)):
    name = input("Enter a name for Player " + str(len(players)+1)+": ")
    players.append(Player(name))

playablePlayers = int(playerNum)
while playablePlayers != 0:
    playablePlayers = int(playerNum)
    for player in players:
        if player.canPlay():
            choice = ""
            while choice != "1":
                print("\nIt is now "+player.name+"'s turn. What do you want to do?")
                print("1. Roll Dice\n2. See Scorecard\n3. Calculate Current Score")
                choice = input()
                print("\n")
                if choice == "2":
                    player.displayScoreCard()
                elif choice == "3":
                    player.calculateScore()
            player.rollDice()
        else:
            playablePlayers -= 1

print("Final Scores")
highestScore = ["",0]
for player in players:
    print("\n")
    score = player.calculateScore()
    if score>highestScore[1]:
        highestScore[0] = player.name
        highestScore[1] = score
    elif score == highestScore[1]:
        highestScore[0] += " & "+player.name
        print("\n")
print("\n"+highestScore[0]+" won with a final score of "+str(highestScore[1])+"!")
