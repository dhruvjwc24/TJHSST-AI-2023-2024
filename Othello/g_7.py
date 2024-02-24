import sys; args = sys.argv[1:]
from re import search
# from time import time
CACHEMOVES = {}

def print2D(choicesBoard, spaces=False):
    for i in range(0, 64, 8): print("".join(choicesBoard[i:i+8]))
    print()
    # if spaces: print()

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
    board, token, suppress, moves, holeLimit, verbose, noArgs = '', '', False, [], 12, False, False
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
    # global HLLIM
    hLim = 12
    midLim = 20
    if not brd: hLim = tkn; return 
    if brd.count(".") <= hLim: return terminalAlphaBeta(brd, tkn)[-1]
    if brd.count(".") <= midLim: return midgameAlphaBeta(brd, tkn)[-1]
    return ruleOfThumb(brd, tkn)
    # else: 
    #     return ruleOfThumb(brd, tkn)

def checkSafeEdge(pos, line, brd, token):
    oppositeToken = getOppositeToken(token)
    ltStr = "".join([brd[idx] for idx in line[:line.index(pos)]])
    rbStr = "".join([brd[idx] for idx in line[line.index(pos)+1:][::-1]])
    return search(f"^{token}+{oppositeToken}*$", ltStr) or search(f"^{token}+{oppositeToken}*$", rbStr)

def getNumFrontierDiscs(brd, token):
    frontierDiscs = 0
    for pos in range(64):
        if brd[pos] == token:
            r, c = idxToPos(pos)
            for ri in range(-1, 2):
                for ci in range(-1, 2):
                    if ri == 0 and ci == 0: continue
                    if r+ri >= 0 and r+ri < 8 and c+ci >= 0 and c+ci < 8:
                        if brd[posToIdx(r+ri, c+ci)] == ".": 
                            frontierDiscs += 1
                            break
    return frontierDiscs

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

def getWeightedScore(board, token):
    weights = [100, -20, 10, 5, 5, 10, -20, 100,
               -20, -50, -2, -2, -2, -2, -50, -20,
               10, -2, -1, -1, -1, -1, -2, 10,
               5, -2, -1, -1, -1, -1, -2, 5,
               5, -2, -1, -1 ,-1, -1, -2, 5,
               10, -2, -1, -1, -1, -1, -2, 10,
               -20, -50, -2, -2, -2, -2, -50, -20,
               100, -20, 10, 5, 5, 10, -20, 100]
    eTkn = getOppositeToken(token)
    score = 0
    for pos in range(64):
        if board[pos] == token: score += weights[pos]
        elif board[pos] == eTkn: score -= weights[pos]
    return score

def ruleOfThumbBrdEval(board, token):
    eTkn = getOppositeToken(token)
    ePossibleMoves = findPossibleMoves(board, eTkn)
    if not ePossibleMoves: 
        if not findPossibleMoves(board, token): 
            return (board.count(token) - board.count(eTkn)) * 10000000
        return 1000000

    evaluation = 0
    evaluation += 100 * getNumCorners(board, token) - 100 * getNumCorners(board, eTkn)
    evaluation += 50 * getNumSafeTokens(board, token) - 50 * getNumSafeTokens(board, eTkn)
    evaluation += 10 * len(findPossibleMoves(board, token)) - 10 * len(ePossibleMoves)
    # evaluation -= 20 * getNumFrontierDiscs(board, token) - 20 * getNumFrontierDiscs(board, eTkn)
    # Add more evaluations based on stability, parity, etc.

    return evaluation

def ruleOfThumb(board, token, possibles=None):
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

    for move in validMoves:
        if move in corners: return move

    for side in walls:
        for move in validMoves:
            if move in walls[side]:
                if checkSafeEdge(move, walls[side], board, token): return move

    for move in validMoves:
        if checkSafeToken(move, board, token): return move

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
    for move in validMovesSet:
        newBrd = makeMove(board, move, validMoves, token)
        oppoTkn = getOppositeToken(token)
        oppoMoves = findPossibleMoves(newBrd, oppoTkn)
        mobility = len(oppoMoves)
        scores[move] = -mobility
        scores[move] += getWeightedScore(newBrd, token)*0.2
        
        if scores[move] >= maxScore: 
            optimalMove = move; maxScore = scores[move]
            # print(f"My preferred move is: {optimalMove}")
    return optimalMove

def brdEval(board, token):

    eTkn = getOppositeToken(token)
    # ePossibleMoves = findPossibleMoves(board, eTkn)
    # if not ePossibleMoves: 
    #     if not findPossibleMoves(board, token): return (board.count(token) - board.count(eTkn))*10000000
    #     return 1000000000

    evaluation = 0
    # print(getNumCorners(board, token))
    #1
    evaluation += 4*getNumCorners(board, token)
    # print(getNumSafeTokens(board, token))
    #17
    evaluation += 2*getNumSafeTokens(board, token)
    # print(len(findPossibleMoves(board, token)))
    # evaluation -= len(findPossibleMoves(board, getOppositeToken(token)))**2
    #11
    # evaluation += 2*len(findPossibleMoves(board, token))**2
    # print(board.count(token))
    #17
    evaluation -= 2*len(findPossibleMoves(board, eTkn))
    # evaluation += board.count(token)**1
    return evaluation

def checkSafeToken(pos, brd, token):
    safeDirs = set()
    eTkn = getOppositeToken(token)
    for rc in range(-1, 2):
        for cc in range(-1, 2):
            safe = True
            if rc == 0 and cc == 0: continue
            r, c = idxToPos(pos)
            while r+rc >= 0 and r+rc < 8 and c+cc >= 0 and c+cc < 8:
                r += rc
                c += cc
                if brd[posToIdx(r, c)] == eTkn or brd[posToIdx(r, c)] == ".": 
                    safe = False
                    break
            if safe and not (-rc, -cc) in safeDirs: safeDirs.add((rc, cc))
            if len(safeDirs) == 4: return True

def midgameAlphaBeta(brd=None, tkn=None, alpha=-1000, beta=1000, level=2, grader=False):
    eTkn = "o" if tkn == "x" else "x"
    possibleMoves = findPossibleMoves(brd, tkn)

    if not possibleMoves: 
        ePossibleMoves = findPossibleMoves(brd, eTkn)
        if not ePossibleMoves: 
            return [(brd.count(tkn) - brd.count(eTkn))*100000]
        nm = midgameAlphaBeta(brd, eTkn, -beta, -alpha, level-1)
        return [-nm[0]] + nm[1:] + [-1]

    if level == 0: return [brdEval(brd, tkn)-brdEval(brd, eTkn)]

    # orderedMoves = []
    # possibleMovesCopy = possibleMoves.copy()
    # while possibleMovesCopy:
    #     move = ruleOfThumb(brd, tkn, possibleMovesCopy)
    #     orderedMoves.append(move)
    #     possibleMovesCopy.pop(move)

    bsf = [alpha]
    for mv in possibleMoves:
        newBrd = makeMove(brd, mv, possibleMoves, tkn)
        nm = midgameAlphaBeta(newBrd, eTkn, -beta, -alpha, level-1)
        score = -nm[0]
        if score >= beta: return [score] + nm[1:] + [mv]
        if score <= alpha: continue
        bsf = [score] + nm[1:] + [mv]
        if level == 2 and grader: print(f'Negamax score: {bsf[0]}; Move Sequence: {bsf[1:]}')
        alpha = score
    return bsf

def terminalAlphaBeta(brd=None, tkn=None, alpha=-1000, beta=1000, level=0, grader=False):
    eTkn = "o" if tkn == "x" else "x"
    possibleMoves = findPossibleMovesEmptyFirst(brd, tkn)

    if not possibleMoves: 
        ePossibleMoves = findPossibleMovesEmptyFirst(brd, eTkn)
        if not ePossibleMoves: return [brd.count(tkn) - brd.count(eTkn)]
        nm = terminalAlphaBeta(brd, eTkn, -beta, -alpha, level+1)
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
        nm = terminalAlphaBeta(newBrd, eTkn, -beta, -alpha, level+1)
        score = -nm[0]
        if score >= beta: return [score] + nm[1:] + [mv]
        if score <= alpha: continue
        bsf = [score] + nm[1:] + [mv]
        if level == 0 and grader: print(f'Negamax score: {bsf[0]}; Move Sequence: {bsf[1:]}')
        alpha = score
    return bsf

def checkGameOver(board): return board.count(".") == 0 or not(findPossibleMoves(board, 'x') or findPossibleMoves(board, 'o'))

def main():
    global args, CACHEMOVES, HLLIM
    # if not args: args = "...........................ox......xo........................... x".split()
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

        #Pass
        if moveIdx == -1: i += 1; continue
        validMoves = findPossibleMoves(board, token)

        #Self has no moves
        if not validMoves: token = getOppositeToken(token); continue 
        
        tokenPlayed = token
        board = makeMove(board, moveIdx, validMoves, token)
        if verbose or i == len(moves)-1: print(f"{token} plays to {moveIdx}\n")
        token = getOppositeToken(token)
        validMoves = findPossibleMoves(board, token)
        if len(validMoves) == 0: 
            token = getOppositeToken(token)
            validMoves = findPossibleMoves(board, token)
        if verbose or i == len(moves)-1: 
            display(board, validMoves, moveIdx, tokenPlayed)
            if not validMoves: print("No moves possible")
            else: print(f"Possible moves for {token}: {set(validMoves.keys())}\n")
        i += 1

    # if noArgs:
    #     display(board, validMoves)
    #     if not validMoves: print("No moves possible")
    #     else: print(f"Possible moves for {token}: {set(validMoves.keys())}\n")

    if validMoves:
        best = ruleOfThumb(board, token)
        print(f"My preferred move is: {best}")
        
        if board.count(".") <= HLLIM:
            ab = terminalAlphaBeta(board, token, grader=True)
            print(f'Negamax score: {ab[0]}; Move Sequence: {ab[1:]}')
        elif board.count(".") <= 30:
            # intially 56
            ab = midgameAlphaBeta(board, token, grader=True)
            print(f'Negamax score: {ab[0]}; Move Sequence: {ab[1:]}')

if __name__ == "__main__": main()

#Dhruv Chandna 2025 Period 6