import sys; args = sys.argv[1:]
import random, re, time

def print2D(choicesBoard, spaces=False):
    for i in range(0, 64, 8): print(choicesBoard[i:i+8])
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
        if len(arg) == 64: board = arg.lower()
        elif arg.lower() in "xo": token = arg.lower()
        elif arg.lower() == "s": suppress = True
        elif len(arg) == 2 and "-" in arg: moves.append(int(arg))
        elif arg.isdigit(): moves.append(int(arg))
        else: moves = condenseMoves(arg.upper())
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

def quickMove(board, token):
    validMoves = findPossibleMoves(board, token)
    if len(validMoves) == 0: return -1
    return random.choice(sorted(list(validMoves.keys())))

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
    if not args: args = "3745263433292221204353152313_61850_5_4414919105714613844311711_2_9_0_8395125625842_352601663484047_154122432595630_7-155-146".split()
    board, token, suppress, moves = extractFromArgs(args)
    quickMove(board, token)
    validMoves = findPossibleMoves(board, token)
    if len(validMoves) == 0:
        validMoves = findPossibleMoves(board, getOppositeToken(token))
        token = getOppositeToken(token)
    display(board, validMoves)
    printPossibleMoves(board, token)

    i = 0
    while i < len(moves):
        moveIdx = moves[i]
        if moveIdx == -1: i += 1; continue
        if len(validMoves) == 0: 
            token = getOppositeToken(token)
            continue
        board = makeMove(board, moveIdx, validMoves, token)
        print(f"{token} plays to {moveIdx}")
        validMoves = findPossibleMoves(board, getOppositeToken(token))
        if len(validMoves) == 0: 
            token = getOppositeToken(token)
            validMoves = findPossibleMoves(board, token)
        display(board, validMoves)
        token = printPossibleMoves(board, getOppositeToken(token))
        validMoves = findPossibleMoves(board, token)
        i += 1

if __name__ == "__main__":
    tStart = time.time()
    main()
    print(f"Time taken: {(time.time()-tStart)*2000}")

#Dhruv Chandna 2025 Period 6