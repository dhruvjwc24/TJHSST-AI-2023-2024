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

def checkOnEdge(row, col): return row == 0 or row == 7 or col == 0 or col == 7
def checkFullLine(leftStr, rightStr): return leftStr.count(".") == 0 and rightStr.count(".") == 0
def checkNextToStable(left, right, stables): return left[-1] in stables or right[0] in stables

def horizontalStable(pos, board, stables):
    row, col = idxToPos(pos)
    left = [posToIdx(row, c) for c in range(0, col)]
    leftStr = "".join([board[idx] for idx in left])
    right = [posToIdx(row, c) for c in range(col+1, 8)]
    rightStr = "".join([board[idx] for idx in right])
    return checkFullLine(leftStr, rightStr) or checkOnEdge(row, col) or checkNextToStable(left, right, stables)
def verticalStable(pos, board, stables):
    row, col = idxToPos(pos)
    top = [posToIdx(r, col) for r in range(0, row)]
    topStr = "".join([board[idx] for idx in top])
    bottom = [posToIdx(r, col) for r in range(row+1, 8)]
    bottomStr = "".join([board[idx] for idx in bottom])
    return checkFullLine(topStr, bottomStr) or checkOnEdge(row, col) or checkNextToStable(top, bottom, stables)
def forwardDiagonalStable(pos, board, stables):
    row, col = idxToPos(pos)
    bottomLeft = [posToIdx(r, c) for r, c in zip(range(row+1, 8), range(col-1, -1, -1))][::-1]
    bottomLeftStr = "".join([board[idx] for idx in bottomLeft])
    topRight = [posToIdx(r, c) for r, c in zip(range(row-1, -1, -1), range(col+1, 8))]
    topRightStr = "".join([board[idx] for idx in topRight])
    return checkFullLine(bottomLeftStr, topRightStr) or checkOnEdge(row, col) or checkNextToStable(bottomLeft, topRight, stables)
def backwardDiagonalStable(pos, board, stables):
    row, col = idxToPos(pos)
    topLeft = [posToIdx(r, c) for r, c in zip(range(row-1, -1, -1), range(col-1, -1, -1))][::-1][::-1]
    topLeftStr = "".join([board[idx] for idx in topLeft])
    bottomRight = [posToIdx(r, c) for r, c in zip(range(row+1, 8), range(col+1, 8))]
    bottomRightStr = "".join([board[idx] for idx in bottomRight])
    return checkFullLine(topLeftStr, bottomRightStr) or checkOnEdge(row, col) or checkNextToStable(topLeft, bottomRight, stables)

def checkStability(pos, board, stables):
    print(f"My position: {pos}")
    print2D(board)
    return horizontalStable(pos, board, stables) and verticalStable(pos, board, stables) and forwardDiagonalStable(pos, board, stables) and backwardDiagonalStable(pos, board, stables)

def checkSafeToken(pos, brd, token):
    safeDirs = set()
    eTkn = getOppositeToken(token)
    for rc in range(-1, 2):
        for cc in range(-1, 2):
            if rc == 0 and cc == 0: continue
            r, c = idxToPos(pos)
            while r+rc >= 0 and r+rc < 8 and c+cc >= 0 and c+cc < 8:
                r += rc
                c += cc
                if brd[posToIdx(r, c)] == eTkn or brd[posToIdx(r, c)] == ".": break
        if not (-r, -c) in safeDirs: safeDirs.add((r, c))
        if len(safeDirs) == 4: return True

def getNumSafeTokens(brd, token):
    safeTokens = 0
    for pos in range(64):
        if brd[pos] == token and checkSafeToken(pos, brd, token): safeTokens += 1
    return safeTokens

def getNumCorners(brd, token):
    corners = {0, 7, 56, 63}
    return sum([1 for corner in corners if brd[corner] == token])

def countCorners(brd, tkn):
    corners = {0, 7, 56, 63}
    return sum([1 for corner in corners if brd[corner] == tkn])

def brdEval(board, token):
    eTkn = getOppositeToken(token)
    evaluation = 0
    # print(getNumCorners(board, token))
    #1
    evaluation += 4*getNumCorners(board, token)**4
    # print(getNumSafeTokens(board, token))
    #17
    evaluation += 2*getNumSafeTokens(board, token)**2
    # print(len(findPossibleMoves(board, token)))
    # evaluation -= len(findPossibleMoves(board, getOppositeToken(token)))**2
    #11
    # evaluation += 2*len(findPossibleMoves(board, token))**2
    # print(board.count(token))
    #17
    evaluation -= len(findPossibleMoves(board, eTkn))**1
    # evaluation += board.count(token)**1
    return evaluation

def quickMove(board, token):
    # if possibles: validMoves = possibles
    validMoves = findPossibleMoves(board, token)
    if not validMoves: return -1
    validMovesSet = set(validMoves.keys())

    bestMove = validMovesSet.pop()
    newBrd = makeMove(board, bestMove, validMoves, token)
    bestScore = brdEval(newBrd, token)
    for move in validMoves:
        newBrd = makeMove(board, move, validMoves, token)
        brdScore = brdEval(newBrd, token)
        if brdScore > bestScore: bestScore = brdScore; bestMove = move
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
    # if not args: args = "444537291910304334222113202331181512143846395053545160574258".split()
    myPrefMove = quickMove("..........o.ooxx..ooooxx...oxxxx..xoxoxo...ooxx...oo.xx..o..x...", 'x')
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