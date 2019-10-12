import PIL,time,webbrowser,winsound,random,sys,math
from PIL import ImageGrab
from PIL import Image
import pyautogui



def makeMove(first,second): # expected format is [1,3] [3,3]
    pyautogui.click(383+32+first[0]*64,-64+149+512-first[1]*64)
    time.sleep(0.2)
    pyautogui.click(383+32+second[0]*64,-64+149+512-second[1]*64)
    time.sleep(0.2)
    pyautogui.click(100,600)

def analysePosition(move,grid):
    temp = grid[move[0][0]][move[0][1]] 
    grid[move[0][0]][move[0][1]] = " "
    grid[move[1][0]][move[1][1]] = temp
    pointValue = 0
    pieceList = [" ","p","P","h","H","b","B","r","R","q","Q","k","K"]
    pieceValue =[ 0 , 1 ,-1 ,2.9,-2.9,3 ,-3 , 5 ,-5 , 9 ,-9 , 0 , 0]
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pointValue += pieceValue[pieceList.index(grid[y][x])]
            #print(pointValue)            
    return pointValue

def checkPiecesTaken(grid,oldGrid):
    whitePointAdv = 0
    blackPointAdv = 0
    return whitePointAdv,blackPointAdv

def checkInCheck(grid):
    inCheck = False
    return inCheck

def piecesBeingAttacked(grid):
    attacks = []
    return attacks

#----------------------------------

# Valid Moves

#----------------------------------
def createAllValidMoves(grid):
    moves = []
    for x in range (len(board)):
        for y in range(len(board[x])):
            if board[x][y] not in contactList:
                if board[x][y].lower() == "p":
                    moves.append(pawnMoves(grid,x,y))
                if board[x][y].lower() == "h":
                    moves.append(knightMoves(grid,x,y))
                if board[x][y].lower() == "b":
                    moves.append(bishopMoves(grid,x,y))
                if board[x][y].lower() == "r":
                    moves.append(rookMoves(grid,x,y))
                if board[x][y].lower() == "q":         # queen is basically a rook and a bishop, so saves some space, ~ Your Welcome
                    moves.append(rookMoves(grid,x,y))
                    moves.append(bishopMoves(grid,x,y))
                if board[x][y].lower() == "k":
                    moves.append(kingMoves(grid,x,y))
    return moves

def pawnMoves(grid,x,y): # checks a move, or an attacking move diagonally
    moves = []
    if (7-x)+1 < 8:
        if grid[x-1][y] == " ":
            moves.append([[y,7-x],[y,(7-x)+1]]) # move forward
    if y-1 > -1 and (7-x)+1 < 8:
        if grid[x-1][y-1] in contactList[1:]:
            moves.append([[y,7-x],[y-1,7-(x-1)]]) # attack diagonal left
    if y+1 < 8 and (7-x)+1 < 8:
        if grid[x-1][y+1] in contactList[1:]:
            moves.append([[y,7-x],[y+1,7-(x-1)]]) # attack diagonal right
    return moves

def knightMoves(grid,x,y): # checks all night moves
    moves = []
    possibleMoves = [[1,2],[1,-2],[-1,2],[-1,-2],[2,1],[2,-1],[-2,1],[-2,-1]] # 8 possible knight moves
    for i in possibleMoves:
        if x+i[0] > -1 and x+i[0] < 8 and y+i[1] > -1 and y+i[1] < 8 and grid[x+i[0]][y+i[1]] in contactList:
            moves.append([[y,7-x],[y+i[1],7-(x+i[0])]]) # add start and end
    return moves

def bishopMoves(grid,x,y):
    moves = []
    diag = [[1,1],[1,-1],[-1,1],[-1,-1]]
    for i in range(len(diag)):
            while x+diag[i][0] > -1 and x+diag[i][0] < 8 and y+diag[i][1]>-1 and y+diag[i][1]<8 and grid[x+diag[i][0]][y+diag[i][1]] in contactList:
                    moves.append([[y,7-x],[y+diag[i][1],7-(x+diag[i][0])]])
                    for j in range(len(diag[i])):
                        if diag[i][j] > 0:
                            diag[i][j] += 1
                        else:
                            diag[i][j] -= 1     # so the next diagonal can be checked
                    if x+diag[i][0] > -1 and x+diag[i][0] < 8 and y+diag[i][1]>-1 and y+diag[i][1]<8:
                        if grid[x+diag[i][0]][y+diag[i][1]] in contactList[1:]: # after taking enemy piece cannot continue moving
                            break
                    else:
                        break
    return moves

def rookMoves(grid,x,y): # quite the Rookie
    moves = []
    dirctn = [[1,0],[-1,0],[0,1],[0,-1]]
    for i in range(len(dirctn)):
            while x+dirctn[i][0] > -1 and x+dirctn[i][0] < 8 and y+dirctn[i][1]>-1 and y+dirctn[i][1]<8 and grid[x+dirctn[i][0]][y+dirctn[i][1]] in contactList:
                moves.append([[y,7-x],[y+dirctn[i][1],7-(x+dirctn[i][0])]])
                for j in range(len(dirctn[i])):
                    if dirctn[i][j] > 0:
                        dirctn[i][j] += 1
                    if dirctn[i][j] < 0:
                        dirctn[i][j] -= 1     # so the next square can be checked
                if x+dirctn[i][0] > -1 and x+dirctn[i][0] < 8 and y+dirctn[i][1]>-1 and y+dirctn[i][1]<8:
                    if grid[x+dirctn[i][0]][y+dirctn[i][1]] in contactList[1:]: # after taking enemy piece cannot continue moving
                        break
                else:
                    break
    return moves



def kingMoves(grid,x,y): # The king is the main guy
    moves = []
    dirctn = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]
    for i in range(len(dirctn)):
            if x+dirctn[i][0] > -1 and x+dirctn[i][0] < 8 and y+dirctn[i][1]>-1 and y+dirctn[i][1]<8 and grid[x+dirctn[i][0]][y+dirctn[i][1]] in contactList:
                moves.append([[y,7-x],[y+dirctn[i][1],7-(x+dirctn[i][0])]])
    return moves



printout = False

beeps = True
if beeps == True:
    time.sleep(0.3)
    winsound.Beep(100,400)

xStart = 383
yStart = 149



#-------------------------------------

# Take Picture Of The Board

#-------------------------------------

takeScreenShot = True
side = False
contactList = [" ","R","H","B","Q","K","P"]#contactList = [" ","r","h","b","q","k","p"]

while True:
    if takeScreenShot == True:
        img = ImageGrab.grab(bbox=(xStart,yStart,xStart+512,yStart+512))
        board = [[0 for i in range (8)] for b in  range(8)]
        for y in range(512):
            for x in range(512):
                if img.getpixel((x,y)) == (0,0,0):
                    try:
                        board[((y//64))][int((x//64))]  += 1
                    except:
                        pass
        pieceBVal =  [945,1238,1240,836,837,840,838,844,1025,779,778,942,941,940,939,938,937,935, 0  ,194,193,192,191,190,399,253,247,330,332,572,575,576,331]
        pieceIndex = ["R","H" ,"H" ,"B","B","B","B","B","Q" ,"K","K","P","P","P","P","P","P","P", " ","p","p","p","p","p","r","h","h","b","b","q","q","q","k"]
        for x in range (len(board)):
            for y in range(len(board[x])):
                if board[x][y] in pieceBVal:
                    board[x][y] = pieceIndex[pieceBVal.index(board[x][y])]
                else:
                    winsound.Beep(500,500)
                    print("Error: Grid Square ",str(7-x),":",str(y)," is not defined.")
                    [print(board[i]) for i in range(8)]
    if side == False:
        if board[0][0] == "R":
            side = "White"
            contactList = [" ","R","H","B","Q","K","P"]
            
            
        else:
            side = "Black"
            contactList = [" ","r","h","b","q","k","p"]
        side = False
           
                
    moves = createAllValidMoves(board)
    setOfMovesValue = []
    #print("-------")
    for move in moves:
        for subMove in move:
            #print(subMove)
            setOfMovesValue.append([analysePosition(subMove,board),subMove])
    #print(setOfMovesValue)
    setOfMovesValue = sorted(setOfMovesValue,key=lambda x: int(x[0]))
    #print(setOfMovesValue)
    print(setOfMovesValue)
    move = setOfMovesValue[0][1]
    print(move)
    makeMove(move[0],move[1])
    time.sleep(2)
#makeMove([4,1],[4,3])
















#---------------------------

# TO DO

#---------------------------

# Make a function to Check if in check

# Make a function to flip the board

# 



"""
~~~~~~~~~~
RECYCLE
~~~~~~~~~~
#[print(board[i]) for i in range(8)]
"""
