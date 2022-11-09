import numpy as np
import cv2
import regions
import tictactoe
import time
import socket 
VIDEPORT = 0
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "192.168.12.67"
port = 2222
client.connect((host, port))
def findCircles(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.blur(gray,(5,5))
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 30, param1= 100, param2=60, minRadius= 60, maxRadius=65)
    return circles

def drawCircles(image, x , y, r):
    cv2.circle(image, (x, y), r, (0, 255, 0), 4)
    cv2.rectangle(image, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

def findMove(image, circles):
    circles = np.round(circles[0, :]).astype("int")
    opponentMove = 0
    for (x, y, r) in circles:

        isMoved = True
        if((x >= regions.minX) and (x <= regions.maxX)) and ((y >= regions.minY) and (y <= regions.maxY)):
            region = regions.checkRegion(x,y)
        else:
            break

        for move in board.availableMoves():
            if move + 1  == region:
                isMoved = False
                break
            else:
                pass

        if not isMoved:
            opponentMove = region - 1
            isMoved = True
            return opponentMove

def nextMove(opponentMove):

    player = 'X'
    board.makeMove(opponentMove, player)
    print("Opponent Move: ", opponentMove + 1)
    board.show()

    player = tictactoe.getEnemy(player)
    computerMove = tictactoe.determine(board, player)
    if not board.complete():
        data = str(computerMove + 1)
        client.send(bytes(data, "utf-8"))
    board.makeMove(computerMove, player)
    print("Computer Move: ", computerMove + 1)
    board.show()
    return computerMove + 1
def drawRegions(image):

    fontIndex = 0
    for i in range(regions.totalYintercepts-1):
        for ii in range(regions.totalXintercepts-1):
            x1 = regions.xIntercepts()[ii]
            x2 = regions.xIntercepts()[ii + 1]
            y1 = regions.yIntercepts()[i]
            y2 = regions.yIntercepts()[i+1]
            cv2.rectangle(image,(int(x1),int(y1)),(int(x2),int(y2)),(0,255,0),2)
            fontIndex = fontIndex + 1
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(image,str(fontIndex),(int(x1) +5,int(y1)+25), font, 0.7,(255,255,255),2)

def drawOpponentMoves(image):
    for move in board.getSquares('X'):
        x = regions.center()[move][0]
        y = regions.center()[move][1]
        cv2.circle(image, (int(x), int(y)), 40, (0, 0, 255), 10)

def drawComputerMoves(image):
    for move in board.getSquares('O'):
        x = regions.center()[move][0]
        y = regions.center()[move][1]
        cv2.rectangle(image, (int(x) - 40, int(y) - 40), (int(x) + 40, int(y) + 40), (255, 0, 0), 10)

def main():
    turn = 0
    while not board.complete():
        ret, image = videoCapture.read()
        circles = findCircles(image)

        if circles is not None:
            opponentMove = findMove(image, circles)
            if not opponentMove in board.availableMoves():
                continue
            computerMove = nextMove(opponentMove)
            if board.complete():
                break
        drawOpponentMoves(image)
        drawRegions(image)
        cv2.imshow('TICTACTOE',image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print("winner is", board.winner())
    time.sleep(1)
    videoCapture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":

    regions = regions.Regions(300, 800, 750, 300,3,3)
    videoCapture = cv2.VideoCapture(VIDEPORT)
    videoCapture.set(3, 1000)
    videoCapture.set(4, 1000)
    board = tictactoe.Tic()
    image = None
    main()