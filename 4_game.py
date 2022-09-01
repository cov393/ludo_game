from termcolor import colored
from tabulate import tabulate
import random

safespots = [3, 11, 23, 15]


class player:
    def __init__(self, player, pos, goal, color, move):
        self.counters = [pos] * 4  # Each of players four counters
        self.pos = pos  # Initial position of player

        self.goal = goal  # goal value for player till he can spiral inwards
        self.kills = 0  # number of kills that the player has
        self.player = player  # number of player e.g. (1)
        self.count = color  # counter ascii code
        self.path = move  # path for player
        self.available_pieces = [True, True, True, True]  # availability value for each counter
        self.won = [False, False, False, False]  # store the winning value for each counter

    def getcount(self):  # get counter value
        return self.count

    def setWon(self, index):  # if goal is reached we call this function
        self.won[index] = True
        self.available_pieces[index] = False
        self.counters[index] = 99
        print(colored("you took a counter To the goal!!", "blue"))
        if (self.getWins() == 4):
            return True
        else:
            return False

    def getWins(self):  # get wins of current player
        count = 0
        for x in self.won:
            if x == True:
                count = count + 1
        return count

    def move(self, index):  # called every time a player needs to move

        counter = self.counters[index]
        if counter == self.goal and self.kills == 0:
            print("You Have no kills so you cannot move this piece any further")
            self.available_pieces[index] = False
            return -1
        else:
            pathIndex = self.path.index(counter)
            self.counters[index] = self.path[(pathIndex + 1)]
            if self.counters[index] == 13:
                all_completed = self.setWon(index)
                if all_completed:
                    return 99
                else:
                    return 100

    def setkills(self, n):  # update the kills of player
        self.kills += n

    def getplayers(self):
        pass

    def setallavailable(self):  # once the player has gotten a kill we can set all counters back
        for i in range(4):
            self.available_pieces[i] = True

    def getCoutners(self):  # returns the counters array
        return self.counters

    def checkStart(self):  # check how many counters are on the board at the moment
        count = 0
        for x in self.counters:
            if x == self.pos:
                count = count + 1
        return count
        pass

    def getNextAvailable(self):  # gets the next available counter that can be moved otherwise returns 0
        for i in range(4):
            if self.available_pieces[i] == True and self.won[i] == False:
                return i
        else:
            return -1
        pass


global board  # global list board
board = list(range(26))
players = []

c1 = colored("i", "red")  # counters for each player
c2 = colored("i", "green")
c3 = colored("i", "yellow")
c4 = colored("i", "blue")

P1 = player(1, 3, 4, c1, [3, 2, 1, 6, 11, 16, 21, 22, 23, 24, 25, 20, 15, 10, 5, 4, 9, 14, 19, 18, 17, 12, 7, 8, 13])
P2 = player(2, 11, 6, c2, [11, 16, 21, 22, 23, 24, 25, 20, 15, 10, 5, 4, 3, 2, 1, 6, 7, 8, 9, 14, 19, 18, 17, 12, 13])
P3 = player(3, 23, 22, c3, [23, 24, 25, 20, 15, 10, 5, 4, 3, 2, 1, 6, 11, 16, 21, 22, 17, 12, 7, 8, 9, 14, 19, 18, 13])
P4 = player(4, 15, 20, c4, [15, 10, 5, 4, 3, 2, 1, 6, 11, 16, 21, 22, 23, 24, 25, 20, 19, 18, 17, 12, 7, 8, 9, 14, 13])
players.append(P1)
players.append(P2)
players.append(P3)
players.append(P4)

counters = []

winners = []


def print_board():
    table = []
    temp = []
    for i in range(1, len(board)):
        temp.append(board[i])
        if ((i) % 5 == 0):
            table.append(temp)
            temp = []
    print(tabulate(table, tablefmt="pretty"))


def resetboard():
    for i in range(len(board)):
        board[i] = i


def addpiece(pos, count):
    if (pos > 98):
        return
    string = board[pos]
    string = str(string) + str(count)
    board[pos] = string


def updatepoistions():
    resetboard()
    for i in range(4):
        count = players[i - 1].getcount()
        pos = players[i - 1].getCoutners()
        # end of turn
        for x in pos:
            addpiece(int(x), count)

def checkKill(p, pieceToMove):
    person = players[p - 1]
    kill = False
    for x in players:
        if x.player == person.player:
            pass
        else:
            other_pos = x.getCoutners()
            for i in range(len(other_pos)):
                if person.counters[pieceToMove] == other_pos[i] and (
                        person.counters[pieceToMove] not in safespots) and \
                        person.counters[pieceToMove] != 99:
                    person.setkills(1)
                    person.setallavailable()
                    x.counters[i] = x.pos
                    print(colored("You have killed one of player {}'s counters!!".format(x.player), "red"))
                    kill = True
    return kill


def playTurn(p):
    person = players[p - 1]
    completed = person.getWins()
    if completed != 4:
        count = person.getcount()
        print("Hello, Player ", p, " :", count)
        atStart = person.checkStart()
        print("----------------------------------------------")
        print("Goals: {} | {} counters at home ('{}') | Kills: {} ".format(completed, atStart, (person.pos),
                                                                           person.kills))
        print("----------------------------------------------")

        input("Press Enter to roll: ")
        roll = random.randint(1, 4)
        output = colored(("You Rolled: {} ".format(roll)), "green")
        print(output)
        input("Press Enter to Resume...")
        # gets the next availible peice to move if others are currently stuck
        pieceToMove = person.getNextAvailable()
        if pieceToMove != -1:
            for i in range(roll):
                returnMsg = person.move(pieceToMove)
                if returnMsg == -1:
                    break
                if returnMsg == 99:
                    winners.append(p)
                    print(colored("WELL DONE PLAYER {} YOU HAVE FINISHED!!".format(p), "yellow"))
                    break
                if returnMsg == 100:
                    break
            kill = checkKill(p, pieceToMove)
        else:
            print("You cannot Currently Move Any Pieces!!")
        updatepoistions()
        if kill == True or roll == 4:
            print_board()
            print(colored("ROLL AGAIN ", "blue"))
            playTurn(p)
    else:
        print("Player: ", p, " You has already Finished!!")
    pass


def game():
    updatepoistions()

    print_board()
    allWon = False
    turn = 0
    while not allWon:
        if turn % 4 == 0:
            playTurn(1)
        elif turn % 4 == 1:
            playTurn(2)
        elif turn % 4 == 2:
            playTurn(3)
        else:
            playTurn(4)
        print_board()
        print(" ")
        turn = turn + 1
        if len(winners) == 4:
            allWon = True
    print(winners)


game()