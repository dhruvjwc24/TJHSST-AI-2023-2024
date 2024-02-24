import sys; args = sys.argv[1:]
import random, re, time

CACHE = {}

def print2D(choicesBoard, spaces=False):
    for i in range(0, 64, 8): print(choicesBoard[i:i+8])
    if spaces: print("\n")

def idxToPos(idx): return (idx // 8, idx % 8)

def posToIdx(row, col): return row * 8 + col

def findPossibleMovesTokenFirst(board, token):
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

def makeMove(board, move, validMoves, token):
    board = board[:move] + token + board[move+1:]
    for idx in validMoves[move]: board = board[:idx] + token + board[idx+1:]
    return board

def extractFromArgs(args):
    board, token, suppress, moves = '', '', False, []
    for arg in args:
        if len(arg) == 64 and set(arg.lower()) == {'x', 'o', '.'}: board = arg.lower()
        elif arg.lower() in "xo": token = arg.lower()
        elif arg.lower() == "s": suppress = True
        elif len(arg) <= 2 and ("-" in arg or arg.isdigit()) : moves.append(int(arg))
        else: moves += condenseMoves(arg.upper())
    if board == '': board = '.'*27+'ox......xo'+'.'*27; board = board.lower()
    if token == '': token = "x" if (len(board)-board.count("."))%2 == 0 else "o"
    return board, token, suppress, moves

def negamax(brd=None, tkn=None):
    eTkn = "o" if tkn == "x" else "x"
    possibleMoves = findPossibleMovesTokenFirst(brd, tkn)
    if not possibleMoves: 
        ePossibleMoves = findPossibleMovesTokenFirst(brd, eTkn)
        if not ePossibleMoves: return [brd.count(tkn) - brd.count(eTkn)]
        # key = (brd, eTkn)
        # if key in CACHE: return CACHE[key]
        nm = negamax(brd, eTkn)
        # CACHE[key] = nm
        return [-nm[0]] + nm[1:] + [-1]

    bsf = [-65]
    for mv in possibleMoves:
        newBrd = makeMove(brd, mv, possibleMoves, tkn)
        # key = (newBrd, eTkn)
        # if key in CACHE: nm = CACHE[key]
        # else:
        #     nm = negamax(newBrd, eTkn)
        #     CACHE[key] = nm
        nm = negamax(newBrd, eTkn)
        if -nm[0] > bsf[0]:
            bsf = [-nm[0]] + nm[1:] + [mv]
    return bsf

def checkGameOver(board): return board.count(".") == 0 or not(findPossibleMoves(board, 'x') or findPossibleMoves(board, 'o'))

def condenseMoves(movesStr):
    moves = []
    while len(movesStr) > 0:
        move = movesStr[:2]
        if "_" in move: moves.append(int(move[1]))
        else: moves.append(int(move))
        movesStr = movesStr[2:]
    return moves

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
    # tStart = time.time()
    main()
    # print(f"Time taken: {(time.time()-tStart)*2000}")

#Dhruv Chandna 2025 Period 6