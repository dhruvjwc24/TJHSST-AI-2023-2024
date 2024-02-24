import sys; args = sys.argv[1:]
import random, re, time

def print2D(choicesBoard, spaces=False):
    for i in range(0, 64, 8): print(choicesBoard[i:i+8])
    # for i in range(0, 64): 
    #     print(choicesBoard[i], end=" ")
    #     if i % 8 == 0: print("\n")
    if spaces: print("\n")

def idxToPos(idx): return (idx // 8, idx % 8)

def posToIdx(row, col): return row * 8 + col

def getLine(board, r, c, ra, ca):
    line = ""
    rStart, cStart = r+ra, c+ca
    while rStart >= 0 and rStart < 8 and cStart >= 0 and cStart < 8:
        line += board[posToIdx(rStart, cStart)]
        rStart += ra
        cStart += ca
    return line

def findPossibleMovesEmptyFirst(board, token):
    oppositeToken = getOppositeToken(token)
    validMoves = {}
    for idx, cell in enumerate(board):
        if cell == ".":
            r, c = idxToPos(idx)
            for ra in range(-1, 2):
                for ca in range(-1, 2):
                    if ra == 0 and ca == 0: continue
                    if r+ra >= 0 and r+ra < 8 and c+ca >= 0 and c+ca < 8:
                        if re.search(f"^{oppositeToken}+{token}.*", getLine(board, r, c, ra, ca)):
                            # re.search(f"pattern", string)
                            flips = set()
                            rCurr = r + ra
                            cCurr = c + ca
                            while board[posToIdx(rCurr, cCurr)] != token:
                                flips.add(posToIdx(rCurr, cCurr))
                                rCurr += ra
                                cCurr += ca
                            if idx in validMoves: validMoves[idx] |= flips
                            else: validMoves[idx] = flips
                            # while
    return validMoves

def findPossibleMovesTokenFirst(board, token):
    oppositeToken = getOppositeToken(token)
    validMoves = {}
    for idx, cell in enumerate(board):
        if cell == token:
            r, c = idxToPos(idx)
            for ra in range(-1, 2):
                for ca in range(-1, 2):
                    flips = set()
                    if r+ra >= 0 and r+ra < 8 and c+ca >= 0 and c+ca < 8:
                        if board[(tp:=posToIdx(r+ra, c+ca))] == oppositeToken:
                            rStart, cStart = r+ra, c+ca
                            flips.add(posToIdx(rStart, cStart))
                            while rStart+ra >= 0 and rStart+ra < 8 and cStart+ca >= 0 and cStart+ca < 8:
                                if board[(tp:=posToIdx(rStart+ra, cStart+ca))] == ".":
                                    if tp in validMoves: validMoves[tp] |= flips
                                    else: validMoves[tp] = flips
                                    break
                                elif board[tp] == token: break
                                else: flips.add(tp)
                                rStart += ra
                                cStart += ca

    return validMoves

def findPossibleMoves(board, token): 
    return findPossibleMovesEmptyFirst(board, token) if board.count(".") <= -1 else findPossibleMovesTokenFirst(board, token)

def convertMoveToIdx(move):
    if len(move) > 2: return -1
    if "-" in move: return -1
    if move.isdigit(): return int(move)
    col, row = ord(move[0])-65, int(move[1])-1
    if col < 0 or col >= 8 or row < 0 or row >= 8: return -1
    return posToIdx(row, col)

def makeMove(board, move, validMoves, token):
    board = board[:move] + token + board[move+1:]
    for idx in validMoves[move]: board = board[:idx] + token + board[idx+1:]
    return board
        
def getToken(board):
    numTokens = len(board)-board.count(".")
    if numTokens % 2 == 0: return 'x'
    else: return 'o'

def getOppositeToken(token): return 'o' if token == 'x' else 'x'

def extractFromArgs(args):
    board, token, suppress, moves = '', '', False, []
    for arg in args:
        if len(arg) == 64 and set(arg.lower()) == {'x', 'o', '.'}: board = arg.lower()
        elif arg.lower() in "xo": token = arg.lower()
        elif arg.lower() == "s": suppress = True
        elif len(arg) <= 2 and ("-" in arg or arg.isdigit()) : moves.append(int(arg))
        # elif arg.isdigit(): moves.append(int(arg))
        else: moves += condenseMoves(arg.upper())
    if board == '': board = '.'*27+'ox......xo'+'.'*27; board = board.lower()
    if token == '': token = getToken(board)
    return board, token, suppress, moves

def printPossibleMoves(board, token):
    validMoves = findPossibleMoves(board, token)
    if len(validMoves) == 0: validMoves, token = findPossibleMoves(board, getOppositeToken(token)), getOppositeToken(token)
    print(f"Possible moves for {token}: {', '.join(sorted([str(choice) for choice in validMoves.keys()]))}\n")
    return token

def display(board, validMoves):
    choicesBoard = board
    for choice in validMoves: choicesBoard = choicesBoard[:choice] + '*' + choicesBoard[choice+1:]
    print2D(choicesBoard, True)
    print(f"{board} {board.count('x')}/{board.count('o')}")

def checkSafeEdge(pos, line, brd, token):
    oppositeToken = getOppositeToken(token)
    ltStr = "".join([brd[idx] for idx in line[:line.index(pos)]])
    rbStr = "".join([brd[idx] for idx in line[line.index(pos)+1:][::-1]])
    return re.search(f"^{token}+{oppositeToken}*$", ltStr) or re.search(f"^{token}+{oppositeToken}*$", rbStr)

def quickMove(board, token):
    dctCorners = {0:{1,8,9}, 7:{6,14,15}, 56:{48,49,57}, 63:{54,55,62}}
    xSquares = {9, 14, 49, 54}
    cSquares = {1, 6, 8, 15, 48, 55, 57, 62}
    corners = {0, 7, 56, 63}
    top = [0, 1, 2, 3, 4, 5, 6, 7]
    left = [0, 8, 16, 24, 32, 40, 48, 56]
    right = [7, 15, 23, 31, 39, 47, 55, 63]
    bottom = [56, 57, 58, 59, 60, 61, 62, 63]
    inside = {10, 11, 12, 13, 17, 18, 19, 20, 21, 22, 25, 26, 27, 28, 29, 30, 33, 34, 35, 36, 37, 38, 41, 42, 43, 44, 45, 46, 50, 51, 52, 53}
    walls = {"top": top, "left": left, "right": right, "bottom": bottom}
    foursome = {"tl": [0, 1, 8, 9], "tr": [6, 7, 14, 15], "bl": [48, 49, 56, 57], "br": [54, 55, 62, 63]}

    validMoves = findPossibleMoves(board, token)
    validMovesSet = set(validMoves.keys())

    scores = {}
    # for move in validMoves: scores[move] = 0

    # print2D(board)
    # print(); print()
    if len(validMoves) == 0: return -1

    #Checking for corners
    # if (u:=corners.intersection(validMovesSet)): return u.pop()
    
    #Checking for corners and edges
    for corner in dctCorners:
        if corner in validMovesSet: return corner

        if board[corner] == token:
            for wall in walls:
                edge = walls[wall]
                if not corner in edge: continue
                for space in edge: 
                    if space in validMovesSet and checkSafeEdge(space, edge, board, token): return space

    veryBadMovesSet = set()
    badMovesSet = set()
    for move in validMoves:
        if move in xSquares: veryBadMovesSet.add(move); validMovesSet.remove(move)
        elif move in cSquares: badMovesSet.add(move); validMovesSet.remove(move)
    if len(validMovesSet) == 0: validMovesSet = badMovesSet if len(badMovesSet) > 0 else veryBadMovesSet 

    # Check mobility
    numOppoMoves = {}
    for move in validMovesSet:
        newBrd = makeMove(board, move, validMoves, token)
        numOppoMoves[move] = len(findPossibleMoves(newBrd, getOppositeToken(token)))
    minOppoMoves = 100
    optimalMove = None
    for move in numOppoMoves:
        if numOppoMoves[move] < minOppoMoves: optimalMove = move; minOppoMoves = numOppoMoves[move]
    return optimalMove
            # for space in dctCorners[corner]:
            #     if space in validMovesSet and space not in xSquares: return space


    '''
    # for wall in walls:
    #     for edge in walls[wall]:
    #         if edge in validMovesSet: return edge
    #     # if (u:=set(walls[wall]).intersection(validMovesSet)): 
    #     #     #return u.pop()
    #     #     for move in u:
    #     #         if checkSafeEdge(move, walls[wall], board, token): return move
        
    # for i in inside:
    #     if i in validMovesSet: return i

    # for c in cSquares:
    #     if c in validMovesSet: return c
    
    # for x in xSquares:
    #     if x in validMovesSet: return x
    '''

    # for corner in dctCorners:
    #     if board[corner] == token:
    #         cornerCSquares = dctCorners[corner].intersection(cSquares)
    #         while cornerCSquares:
    #             cSquare = cornerCSquares.pop()
    #             if board[cSquare] != token: break
    #         xSquare = (dctCorners[corner] - cornerCSquares).pop()
    #         if xSquare in validMovesSet: return xSquare

    # #Checking for spaces next to corners
    # for move in validMoves:
    #     if move in cSquares:
    #         for corner in xSquares:
    #             if board[corner] == token and (move == corner+1 or move == corner-1 or move == corner+8 or move == corner-8): return move

    #Checking for spaces diagonal to corners
    # for move in validMoves:
    #     for quad in foursome:
    #         four = foursome[quad]
    #         if move in four:
    #             four.remove(move)
    #             for space in four:
    #                 if board[space] != token: break
    #             return move


    # if (u:=cSquares.intersection(validMovesSet)):
    #     for cSquare in u:
    #         for wall in walls:
    #             if cSquare in walls[wall]:
    #                 if checkSafeEdge(cSquare, walls[wall], board, token): return cSquare
    # print("Im here!!!!!\n\n\n\n\n\n\n\n")
    # for move in validMoves:
    #     for wall in walls:
    #         if move in walls[wall]:
    #             if checkSafeEdge(move, walls[wall], board, token): return move



    
    
    return random.choice(sorted(list(validMovesSet)))

# bestMove = random.choice(sorted(list(validMoves.keys())))
    # return validMovesSet.pop()s
    # bestMove = None
    # bestScore = -100
    # for move in validMoves:

    #     newBoard = makeMove(board, move, validMoves, token)
    #     moveScore = originalNumOfOppositeMoves - len(findPossibleMoves(newBoard, getOppositeToken(token)))
    #     if moveScore > bestScore: bestMove, bestScore = move, moveScore
    return bestMove

def checkGameOver(board):
    if board.count('x') == 0 or board.count('o') == 0 or board.count('.') == 0: return True
    return False

def condenseMoves(movesStr):
    moves = []
    while len(movesStr) > 0:
        move = movesStr[:2]
        if "_" in move: moves.append(int(move[1]))
        else: moves.append(int(move))
        movesStr = movesStr[2:]
    return moves

def main():
    global args
    if not args: args = "444537291910304334222113202331181512143846395053545160574258".split()
    board, token, suppress, moves = extractFromArgs(args)
    # quickMove(board, token)
    validMoves = findPossibleMoves(board, token)
    if len(validMoves) == 0:
        validMoves = findPossibleMoves(board, getOppositeToken(token))
        token = getOppositeToken(token)
    display(board, validMoves)
    printPossibleMoves(board, token)

    i = 0
    while i < len(moves):
        validMoves = findPossibleMoves(board, token)
        moveIdx = moves[i]
        if moveIdx == -1 or len(validMoves) == 0: 
            i += 1; token = getOppositeToken(token); continue
        board = makeMove(board, moveIdx, validMoves, token)
        print(f"{token} plays to {moveIdx}")
        if i+1 < len(moves) and moves[i+1] == -1: validMoves = findPossibleMoves(board, token); i+=1
        else: validMoves = findPossibleMoves(board, getOppositeToken(token)); token = getOppositeToken(token)
        if len(validMoves) == 0: 
            token = getOppositeToken(token)
            validMoves = findPossibleMoves(board, token)
        display(board, validMoves)
        token = printPossibleMoves(board, token)
        i += 1

if __name__ == "__main__":
    # tStart = time.time()
    main()
    # print(f"Time taken: {(time.time()-tStart)*2000}")

#Dhruv Chandna 2025 Period 6