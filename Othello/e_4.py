import sys; args = sys.argv[1:]
import time

CACHE = {}

def print2D(choicesBoard, spaces=False):
    for i in range(0, 64, 8): print(choicesBoard[i:i+8])
    if spaces: print("\n")

def idxToPos(idx): return (idx // 8, idx % 8)

def posToIdx(row, col): return row * 8 + col

def findPossibleMovesEmptyFirst(board, token):
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
    return validMoves           

def findPossibleMoves(board, token): return findPossibleMovesEmptyFirst(board, token)

def makeMove(board, move, validMoves, token):
    board = board[:move] + token + board[move+1:]
    for idx in validMoves[move]: board = board[:idx] + token + board[idx+1:]
    return board
         
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

def negamax(brd=None, tkn=None):
    key = (brd, tkn)
    if key in CACHE: return CACHE[key]
    eTkn = "o" if tkn == "x" else "x"
    possibleMoves = findPossibleMovesEmptyFirst(brd, tkn)
    if not possibleMoves: 
        ePossibleMoves = findPossibleMovesEmptyFirst(brd, eTkn)
        if not ePossibleMoves: 
            CACHE[key] = [brd.count(tkn) - brd.count(eTkn)]
            return [brd.count(tkn) - brd.count(eTkn)]
        nm = negamax(brd, eTkn)
        CACHE[key] = [-nm[0]] + nm[1:] + [-1]
        return [-nm[0]] + nm[1:] + [-1]

    bsf = [-65]
    for mv in possibleMoves:
        newBrd = makeMove(brd, mv, possibleMoves, tkn)
        nm = negamax(newBrd, eTkn)
        if -nm[0] > bsf[0]:
            bsf = [-nm[0]] + nm[1:] + [mv]
    CACHE[key] = bsf
    return bsf

def checkGameOver(board): return board.count(".") == 0 or not(findPossibleMoves(board, 'x') or findPossibleMoves(board, 'o'))

def main():
    global args, CACHE
    # if not args: args = "ooooooo.oooooo.oooooxxo.ooooxxoxoooxoooxooxxxooooooooooo.oxxxo.. x".split()
    if not args: args = "xxxxxo.xxxxxooooxxxxooooxxxoxoooxoxxoxoooxxo.xx...oxxxxx.o.xo... x".split()
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