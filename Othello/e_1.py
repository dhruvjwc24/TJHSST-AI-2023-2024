import sys; args = sys.argv[1:]
import random, re, time

CACHE = {}

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
    # oppositeToken = getOppositeToken(token)
    oppositeToken = 'o' if token == 'x' else 'x'
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
    # return findPossibleMovesEmptyFirst(board, token) if board.count(".") <= -1 else findPossibleMovesTokenFirst(board, token)
    return findPossibleMovesTokenFirst(board, token)

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

def negamax(brd=None, tkn=None):
    # if tkn == None: tkn = getToken(brd)
    eTkn = "o" if tkn == "x" else "x"
    # if checkGameOver(brd): return [brd.count(tkn) - brd.count(eTkn)]
     # if tkn can not move, but eTkn can: deal with it
    possibleMoves = findPossibleMovesTokenFirst(brd, tkn)
    if not possibleMoves: 
        ePossibleMoves = findPossibleMovesTokenFirst(brd, eTkn)
        if not ePossibleMoves: return [brd.count(tkn) - brd.count(eTkn)]
        key = (brd, eTkn)
        if key in CACHE: return CACHE[key]
        nm = negamax(brd, eTkn)
        CACHE[key] = nm
        return [-nm[0]] + nm[1:] + [-1]

    bsf = [-65]
    for mv in possibleMoves:
        newBrd = makeMove(brd, mv, possibleMoves, tkn)
        key = (newBrd, eTkn)
        if key in CACHE: nm = CACHE[key]
        else:
            nm = negamax(newBrd, eTkn)
            CACHE[key] = nm
        if -nm[0] > bsf[0]:
            bsf = [-nm[0]] + nm[1:] + [mv]
    return bsf

def checkGameOver(board): return board.count(".") == 0 or not(findPossibleMoves(board, 'x') or findPossibleMoves(board, 'o'))

def main():
    global args, CACHE
    if not args: args = "ooooooo.oooooo.oooooxxo.ooooxxoxoooxoooxooxxxooooooooooo.oxxxo.. x".split()
    board, token, suppress, moves = extractFromArgs(args)

    print2D(board, True)
    print(f"{board} {board.count('x')}/{board.count('o')}")
    print(f"Possible moves for {token}: {set(findPossibleMoves(board, token).keys())}")
        
    best = negamax(board, token)
    print(f'Negamax score: {best[0]}; Move Sequence: {best[1:]}')

if __name__ == "__main__":
    tStart = time.time()
    main()
    print(f"Time taken: {(time.time()-tStart)*1000}")

#Dhruv Chandna 2025 Period 6