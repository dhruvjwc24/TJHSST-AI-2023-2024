import sys; args = sys.argv[1:]
from time import time
from re import search
# import time, re

CACHEMOVES = {}

def print2D(choicesBoard, spaces=False):
    for i in range(0, 64, 8): print(" ".join(choicesBoard[i:i+8]))
    if spaces: print("\n")

def display(board, validMoves, move=None, token=None):
    choicesBoard = board
    if move != None: choicesBoard = choicesBoard[:move] + token.upper() + choicesBoard[move+1:]
    for choice in validMoves: choicesBoard = choicesBoard[:choice] + '*' + choicesBoard[choice+1:]
    print2D(choicesBoard)
    print(f"{board} {board.count('x')}/{board.count('o')}")

def printPossibleMoves(board, token):
    validMoves = findPossibleMoves(board, token)
    if len(validMoves) == 0:
        validMoves = findPossibleMoves(board, getOppositeToken(token))
        token = getOppositeToken(token)
    print(f"Possible moves for {token}: {', '.join(sorted([str(choice) for choice in validMoves.keys()]))}\n")
    # return token

def idxToPos(idx): return (idx // 8, idx % 8)

def posToIdx(row, col): return row * 8 + col

def convertMoveToIdx(move):
    if move.isdigit(): return int(move)
    if len(move) > 2: return -1
    if "-" in move: return -1
    else:
        col, row = ord(move[0])-65, int(move[1])-1
        if col < 0 or col >= 8 or row < 0 or row >= 8: return -1
        return posToIdx(row, col)

def findPossibleMovesTokenFirst(board, token):
    key = (board, token)
    if key in CACHEMOVES: return CACHEMOVES[key]
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
    CACHEMOVES[key] = validMoves
    return validMoves

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

def findPossibleMoves(board, token): return findPossibleMovesEmptyFirst(board, token) if board.count(".") <= 32 else findPossibleMovesTokenFirst(board, token)

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
        if "-" in move and move[1] != "1": movesStr = movesStr[2:]; continue
        if "_" in move: moves.append(int(move[1]))
        else: moves.append(int(move))
        movesStr = movesStr[2:]
    return moves

def extractFromArgs(args):
    board, token, suppress, moves, holeLimit, verbose, noArgs = '', '', False, [], 0, False, False
    if len(args) == 0: noArgs = True
    for arg in args:
        if len(arg) == 64 and set(arg.lower()) == {'x', 'o', '.'}: board = arg.lower()
        elif "HL" in arg: holeLimit = int(arg[2:])
        elif "v" == arg.lower(): verbose = True
        elif arg.lower() in "xo": token = arg.lower()
        elif arg.lower() == "s": suppress = True
        elif len(arg) <= 2 and (("-" in arg and arg[1] == "1") or arg.isdigit()) : moves.append(int(arg))
        else: moves += condenseMoves(arg.upper())
    if board == '': board = '.'*27+'ox......xo'+'.'*27; board = board.lower()
    if token == '': token = getToken(board)
    return board, token, suppress, moves, holeLimit, verbose, noArgs

def quickMove(brd, tkn):
    global HLLIM
    # if holeLim: HLLIM = holeLim
    # if not tkn: tkn = getToken(brd)
    if not brd: HLLIM = tkn; return 
    if brd.count(".") <= HLLIM: return negamaxAlphaBeta(brd, tkn)[-1]
    else: return ruleOfThumb(brd, tkn)

def checkSafeEdge(pos, line, brd, token):
    oppositeToken = getOppositeToken(token)
    ltStr = "".join([brd[idx] for idx in line[:line.index(pos)]])
    rbStr = "".join([brd[idx] for idx in line[line.index(pos)+1:][::-1]])
    return search(f"^{token}+{oppositeToken}*$", ltStr) or search(f"^{token}+{oppositeToken}*$", rbStr)

def ruleOfThumb(board, token, possibles=None):
    dctCorners = {0:{1,8,9}, 7:{6,14,15}, 56:{48,49,57}, 63:{54,55,62}}
    xSquares = {9, 14, 49, 54}
    cSquares = {1, 6, 8, 15, 48, 55, 57, 62}
    corners = {0, 7, 56, 63}
    top = [0, 1, 2, 3, 4, 5, 6, 7]
    left = [0, 8, 16, 24, 32, 40, 48, 56]
    right = [7, 15, 23, 31, 39, 47, 55, 63]
    bottom = [56, 57, 58, 59, 60, 61, 62, 63]
    walls = {"top": top, "left": left, "right": right, "bottom": bottom}

    if possibles: validMoves = possibles
    else: validMoves = findPossibleMoves(board, token)
    validMovesSet = set(validMoves.keys())

    scores = {}
    if len(validMoves) == 0: return -1

    #Checking for corners
    # if (u:=corners.intersection(validMovesSet)): return u.pop()
    for move in validMoves: 
        if move in corners: return move
    
    #Checking for corners and edges
    for corner in dctCorners:
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
    
    
    # Check mobility and weight
    scores = {}
    maxScore = -9223372036854775807
    optimalMove = None
    for move in sorted(validMovesSet):
        newBrd = makeMove(board, move, validMoves, token)
        oppoTkn = getOppositeToken(token)
        oppoMoves = findPossibleMoves(newBrd, oppoTkn)
        mobility = len(oppoMoves)
        scores[move] = -mobility
        
        if scores[move] >= maxScore: optimalMove = move; maxScore = scores[move]
    return optimalMove

def negamaxAlphaBeta(brd=None, tkn=None, alpha=-1000, beta=1000):
    eTkn = "o" if tkn == "x" else "x"
    possibleMoves = findPossibleMovesEmptyFirst(brd, tkn)
    if not possibleMoves: 
        ePossibleMoves = findPossibleMovesEmptyFirst(brd, eTkn)
        if not ePossibleMoves: return [brd.count(tkn) - brd.count(eTkn)]
        nm = negamaxAlphaBeta(brd, eTkn, -beta, -alpha)
        return [-nm[0]] + nm[1:] + [-1]

    orderedMoves = []
    possibleMovesCopy = possibleMoves.copy()
    while possibleMovesCopy:
        move = ruleOfThumb(brd, tkn, possibleMovesCopy)
        orderedMoves.append(move)
        possibleMovesCopy.pop(move)

    bsf = [alpha]
    for mv in orderedMoves:
        newBrd = makeMove(brd, mv, possibleMoves, tkn)
        nm = negamaxAlphaBeta(newBrd, eTkn, -beta, -alpha)
        score = -nm[0]
        if score >= beta: return [score] + nm[1:] + [mv]
        if score <= alpha: continue
        bsf = [score] + nm[1:] + [mv]
        alpha = score
    return bsf

def checkGameOver(board): return board.count(".") == 0 or not(findPossibleMoves(board, 'x') or findPossibleMoves(board, 'o'))

def main():
    global args, CACHEMOVES, HLLIM
    # if not args: args = ".x.......ox.x....xoxx......oxoo...oxoxox..xoxxox.x.oo.o....oooox".split()
    board, token, suppress, moves, holeLimit, verbose, noArgs = extractFromArgs(args)
    HLLIM = holeLimit

    validMoves = findPossibleMoves(board, token)
    if not validMoves:
        token = getOppositeToken(token)
        validMoves = findPossibleMoves(board, token)
    display(board, validMoves)
    print(f"Possible moves for {token}: {set(validMoves.keys())}\n")

    i = 0
    while i < len(moves):
        moveIdx = moves[i]
        if moveIdx == -1: i += 1; continue
        if len(validMoves) == 0: 
            token = getOppositeToken(token)
            continue
        tokenPlayed = token
        board = makeMove(board, moveIdx, validMoves, token)
        print(f"{token} plays to {moveIdx}\n")
        token = getOppositeToken(token)
        validMoves = findPossibleMoves(board, token)
        if len(validMoves) == 0: 
            token = getOppositeToken(token)
            validMoves = findPossibleMoves(board, token)
        if verbose: 
            display(board, validMoves, moveIdx, tokenPlayed)
            if not validMoves: 
                print("No moves possible")
            else: print(f"Possible moves for {token}: {set(validMoves.keys())}\n")
        elif i == len(moves)-1: 
            display(board, validMoves, moveIdx, tokenPlayed)
            if not validMoves: print("No moves possible")
            else: print(f"Possible moves for {token}: {set(validMoves.keys())}\n")
        i += 1

    if noArgs:
        display(board, validMoves)
        if not validMoves: print("No moves possible")
        else: print(f"Possible moves for {token}: {set(validMoves.keys())}\n")

    if validMoves:
        best = ruleOfThumb(board, token)
        print(f"My preferred move is: {best}")
        if board.count(".") <= HLLIM:
            ab = negamaxAlphaBeta(board, token)
            print(f'Negamax score: {ab[0]}; Move Sequence: {ab[1:]}')

if __name__ == "__main__":
    tStart = time()
    main()
    print(f"Time taken: {(time()-tStart)*1000}")

#Dhruv Chandna 2025 Period 6