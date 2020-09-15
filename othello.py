import random
import sys


def drawBoard(board):
    print('   12345678')
    print('  **********')
    for y in range(8):
        print('%s *' % (y+1), end='')
        for x in range(8):
            print(board[x][y], end='')
        print('*')
    print('  **********')


def resetBoard(board):
   for x in range(8):
       for y in range(8):
           board[x][y] = ' '

   board[3][3] = 'X'
   board[3][4] = 'O'
   board[4][3] = 'O'
   board[4][4] = 'X'


def getNewBoard():
    board = []
    for i in range(8):
        board.append([' '] * 8)
    return board


def isValidMove(board, tile, xstart, ystart):
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False
    board[xstart][ystart] = tile
    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'
    tilesToFlip = []

    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        if isOnBoard(x, y) and board[x][y] == otherTile:
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y):
                    break
            if not isOnBoard(x, y):
                continue
            if board[x][y] == tile:
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])

    board[xstart][ystart] = ' '
    if len(tilesToFlip) == 0:
        return False
    return tilesToFlip


def isOnBoard(x, y):
    return ((x >= 0) and (x <= 7)) and ((y >= 0) and (y <=7))


def getBoardWithValidMoves(board, tile):
    dupeBoard = getBoardCopy(board)
    for x, y in getValidMoves(dupeBoard, tile):
        dupeBoard[x][y] = '.'
    return dupeBoard


def getValidMoves(board, tile):
    validMoves = []
    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves


def getScoreOfBoard(board):
    xscore = 0
    oscore = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'X':
                xscore+=1
            if board[x][y] == 'O':
                oscore+=1
    return {'X': xscore, 'O': oscore}


def enterPlayerTile():
    tile = ''
    while not (tile == 'X' or tile == 'O'):
        print('Do you want to be X or O?')
        tile = input().upper()
    if tile == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']


def makeMove(board, tile, xstart, ystart):
    tilesToFlip = isValidMove(board, tile, xstart, ystart)
    if tilesToFlip == False:
        return False
    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True


def getBoardCopy(board):
    duplicate= getNewBoard()
    for x in range(8):
        for y in range(8):
            duplicate[x][y]=board[x][y]
    return duplicate


def isOnCorner(x, y):
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)


def getPlayerMove(board, playerTile):
    digits = '1 2 3 4 5 6 7 8'.split()
    while True:
        print('Enter your move, or type quit to end the game.')
        move = input().lower()
        if move == 'quit':
            return 'quit'
        if len(move) == 2 and move[0] in digits and move[1] in digits:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isValidMove(board, playerTile, x, y) == False:
                continue
            else:
                break
    return [x, y]


def getComputerMove(board, computerTile):
    possibleMoves = getValidMoves(board, computerTile)
    random.shuffle(possibleMoves)
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]

    bestScore = -100000
    for x, y in possibleMoves:
        dupeBoard = getBoardCopy(board)
        makeMove(dupeBoard, computerTile, x, y)
        score = getScoreOfBoard(dupeBoard)[computerTile]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove


def PlayerStrategy(board, playerTile):
    possibleMoves = getValidMoves(board, playerTile)
    random.shuffle(possibleMoves)
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]

    bestScore =100000
    for x, y in possibleMoves:
        dupeBoard = getBoardCopy(board)
        makeMove(dupeBoard, computerTile, x, y)
        score = getScoreOfBoard(dupeBoard)[computerTile]
        if score < bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove


def minimax(board, depth, computerTile, maximizingPlayer):
    if depth == 1:
        tempx, tempy = getComputerMove(board, computerTile)
    if maximizingPlayer:
        dupeBoard1=getBoardCopy(board)
        for x in range(8):
            for y in range(8):
                tempx, tempy = getComputerMove(board, computerTile)
                makeMove(dupeBoard1, computerTile, tempx, tempy)
    else:
        dupeBoard1 = getBoardCopy(board)
        for x in range(8):
            for y in range(8):
                tempx, tempy = PlayerStrategy(board, playerTile)
                makeMove(dupeBoard1, playerTile, tempx, tempy)

    bestValue = [tempx, tempy]
    return bestValue


def showPoints(playerTile, computerTile):
    scores = getScoreOfBoard(mainBoard)
    print('Player = %s points. \nComputer = %s points.' % (scores[playerTile], scores[computerTile]))


while True:
    mainBoard = getNewBoard()
    resetBoard(mainBoard)
    playerTile, computerTile = enterPlayerTile()
    showHints = False
    turn = 'player'
    print('The ' + turn + ' will go first.')
    print('Please select your level. Press 0 for easy and 1 for hard.')
    a = int(input());
    if a == 0:
        depth = 1
    else:
        depth = 3
    while True:
        if turn == 'player':
            drawBoard(mainBoard)
            showPoints(playerTile, computerTile)
            move = getPlayerMove(mainBoard, playerTile)
            if move == 'quit':
                print('Thanks for playing!')
                sys.exit()
            else:
                makeMove(mainBoard, playerTile, move[0], move[1])

            if getValidMoves(mainBoard, computerTile) == []:
                break
            else:
                turn = 'computer'
        else:
            drawBoard(mainBoard)
            showPoints(playerTile, computerTile)
            input('Press Enter to see the computer\'s move.')
            x, y = minimax(mainBoard, depth, computerTile, True)
            makeMove(mainBoard, computerTile, x, y)

            if getValidMoves(mainBoard, playerTile) == []:
                break
            else:
                turn = 'player'


drawBoard(mainBoard)
scores = getScoreOfBoard(mainBoard)
print('X scored %s points. O scored %s points.' % (scores['X'], scores['O']))
if scores[playerTile] > scores[computerTile]:
    print('You beat the computer by %s points! Congratulations!' % (scores[playerTile] - scores[computerTile]))
elif scores[playerTile] < scores[computerTile]:
    print('You lost. The computer beat you by %s points.' % (scores[computerTile] - scores[playerTile]))
else:
    print('The game was a tie!')

