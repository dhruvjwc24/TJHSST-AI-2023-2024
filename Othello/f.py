import sys; args = sys.argv[1:]
import time

CACHE = {}
CACHEMOVES = {}

def print2D(choicesBoard, spaces=False):
    for i in range(0, 64, 8): print(choicesBoard[i:i+8])
    if spaces: print("\n")

def idxToPos(idx): return (idx // 8, idx % 8)

def posToIdx(row, col): return row * 8 + col

def findPossibleMovesEmptyFirst(board, token):
    key = (board, token)
    if key in CACHEMOVES: return CACHEMOVES[key]
    eTkn = getOppositeToken(token)
    validMoves = {}
    for idx, cell in enumerate(board):
        if cell == ".":
            r, c = idxToPos(idx)
            for ri in range(-1, 2):
                for ci in range(-1, 2):
                    if ri == 0 and ci == 0: continue
                    if r+ri >= 0 and r+ri < 8 and c+ci >= 0 and c+ci < 8:
                        currR, currC = r+ri, c+ci
                        flips = set()
                        if board[posToIdx(currR, currC)] == eTkn:
                            flips.add(posToIdx(currR, currC))
                            while currR+ri >= 0 and currR+ri < 8 and currC+ci >= 0 and currC+ci < 8:
                                if board[posToIdx(currR+ri, currC+ci)] == eTkn:
                                    flips.add(posToIdx(currR+ri, currC+ci))
                                    currR += ri
                                    currC += ci
                                elif board[posToIdx(currR+ri, currC+ci)] == token:
                                    if idx in validMoves: validMoves[idx] = validMoves[idx] | flips
                                    else: validMoves[idx] = flips
                                    break
                                else: break
    CACHEMOVES[key] = validMoves
    return validMoves           

def findPossibleMoves(board, token): return findPossibleMovesEmptyFirst(board, token)

def makeMove(board, move, validMoves, token):
    boardList = list(board)
    boardList[move] = token
    for idx in validMoves[move]: boardList[idx] = token
    return "".join(boardList)
         
def getToken(board):
    numTokens = len(board)-board.count(".")
    if numTokens % 2 == 0: return 'x'
    else: return 'o'

def getOppositeToken(token): return 'o' if token == 'x' else 'x'

def condenseMoves(movesStr):
    moves = []
    while len(movesStr) > 0:
        move = movesStr[:2]
        if "_" in move: moves.append(int(move[1]))
        else: moves.append(int(move))
        movesStr = movesStr[2:]
    return moves

def extractFromArgs(args):
    board, token, suppress, moves = '', '', False, []
    for arg in args:
        if len(arg) == 64 and set(arg.lower()) == {'x', 'o', '.'}: board = arg.lower()
        elif arg.lower() in "xo": token = arg.lower()
        elif arg.lower() == "s": suppress = True
        elif len(arg) <= 2 and ("-" in arg or arg.isdigit()) : moves.append(int(arg))
        else: moves += condenseMoves(arg.upper())
    if board == '': board = '.'*27+'ox......xo'+'.'*27; board = board.lower()
    if token == '': token = getToken(board)
    return board, token, suppress, moves

def quickMove(board, token):
    dctCorners = {0:{1,8,9}, 7:{6,14,15}, 56:{48,49,57}, 63:{54,55,62}}
    xSquares = {9, 14, 49, 54}
    cSquares = {1, 6, 8, 15, 48, 55, 57, 62}
    corners = {0, 7, 56, 63}
    top = [0, 1, 2, 3, 4, 5, 6, 7]
    left = [0, 8, 16, 24, 32, 40, 48, 56]
    right = [7, 15, 23, 31, 39, 47, 55, 63]
    bottom = [56, 57, 58, 59, 60, 61, 62, 63]
    walls = {"top": top, "left": left, "right": right, "bottom": bottom}

    validMoves = findPossibleMoves(board, token)
    validMovesSet = set(validMoves.keys())

    scores = {}
    # for move in validMoves: scores[move] = 0

    # print2D(board)
    # print(); print()
    if len(validMoves) == 0: return -1

    #Checking for corners
    # if (u:=corners.intersection(validMovesSet)): return u.pop()
    for move in validMoves:
        if move in corners: return move

        
    
    #Checking for corners and edges
    for corner in dctCorners:
        if corner in validMovesSet: return corner

        if board[corner] == token:
            for wall in walls:
                edge = walls[wall]
                if not corner in edge: continue
                for space in edge: 
                    if space in validMovesSet and checkSafeEdge(space, edge, board, token): return space
    
    # stables = set()
    # for pos in range(64):
    #     if checkStability(pos, board, stables): stables.add(pos)

    veryBadMovesSet = set()
    badMovesSet = set()
    for move in validMoves:
        if move in xSquares: veryBadMovesSet.add(move); validMovesSet.remove(move)
        elif move in cSquares: badMovesSet.add(move); validMovesSet.remove(move)
    if len(validMovesSet) == 0: validMovesSet = badMovesSet if len(badMovesSet) > 0 else veryBadMovesSet 
    
    
    # Check mobility and weight
    scores = {}
    # maxScore = -sys.maxsize
    maxScore = -9223372036854775807
    optimalMove = None
    for move in sorted(validMovesSet):
        newBrd = makeMove(board, move, validMoves, token)
        # print2D(newBrd)
        oppoTkn = getOppositeToken(token)
        oppoMoves = findPossibleMoves(newBrd, oppoTkn)
        # oppoMovesSet = set(oppoMoves.keys())
        # if len(oppoMoves) == 1 and corners.intersection(set(findPossibleMoves(makeMove(newBrd, oppoMovesSet.pop(), oppoMoves, oppoTkn), token))): return move
        mobility = len(oppoMoves)
        scores[move] = -mobility
        # weight = weightedMatrix[move]
        # scores[move] = -100*mobility + weight
        
        if scores[move] >= maxScore: optimalMove = move; maxScore = scores[move]
    return optimalMove

def terminalAlphaBeta(brd=None, tkn=None, alpha=-1000, beta=1000):
    key = (brd, tkn)
    if key in CACHE: return CACHE[key]
    eTkn = "o" if tkn == "x" else "x"
    possibleMoves = findPossibleMovesEmptyFirst(brd, tkn)
    #Move ordering, call quickMove maybe --> Implement later
    if not possibleMoves: 
        ePossibleMoves = findPossibleMovesEmptyFirst(brd, eTkn)
        if not ePossibleMoves: 
            CACHE[key] = [brd.count(tkn) - brd.count(eTkn)]
            return [brd.count(tkn) - brd.count(eTkn)]
        nm = terminalAlphaBeta(brd, eTkn, -beta, -alpha)
        CACHE[key] = [-nm[0]] + nm[1:] + [-1]
        return [-nm[0]] + nm[1:] + [-1]

    bsf = [-65]
    for mv in possibleMoves:
        newBrd = makeMove(brd, mv, possibleMoves, tkn)
        nm = terminalAlphaBeta(newBrd, eTkn, -beta, -alpha)
        if -nm[0] > bsf[0]:
            bsf = [-nm[0]] + nm[1:] + [mv]
        # CACHE[key] = bsf
        if bsf[0] > alpha: alpha = bsf[0]
        if alpha >= beta: break
    return bsf

def checkGameOver(board): return board.count(".") == 0 or not(findPossibleMoves(board, 'x') or findPossibleMoves(board, 'o'))

def main():
    global args, CACHE, CACHEMOVES
    # if not args: args = "ooooooo.oooooo.oooooxxo.ooooxxoxoooxoooxooxxxooooooooooo.oxxxo.. x".split()
    if not args: args = "xxxxxo.xxxxxooooxxxxooooxxxoxoooxoxxoxoooxxo.xx...oxxxxx.o.xo... x".split()
    board, token, suppress, moves = extractFromArgs(args)

    print2D(board, True)
    print(f"{board} {board.count('x')}/{board.count('o')}")
    print(f"Possible moves for {token}: {set(findPossibleMoves(board, token).keys())}")
        
    best = terminalAlphaBeta(board, token)
    print(f'Negamax score: {best[0]}; Move Sequence: {best[1:]}')

if __name__ == "__main__":
    tStart = time.time()
    main()
    print(f"Time taken: {(time.time()-tStart)*1000}")

#Dhruv Chandna 2025 Period 6