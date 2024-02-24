import sys; args = sys.argv[1:]
import random, re, time
import g_1 as myFile

CACHEMOVES = {}

def main():
    global args, CACHEMOVES
    p = 100
    holeLimit = 12
    for arg in args: 
        if arg.startswith("-p"): p = int(arg[2:])
        elif "HL" in arg: holeLimit = int(arg[2:])
    # if p > 0: totalMyTkn, totalAll = runTournament(p, holeLimit)
    totalMyTkn, totalAll = runTournament(p, holeLimit)
    reportResults(totalMyTkn, totalAll)

def runTournament(gameCt, holeLimit):
    totalMyTkn = 0
    totalAll = 0
    for gameNum in range(0, gameCt):
        myTkn = 'x' if gameNum % 2 == 0 else 'o'
        # oppositeToken = getOppositeToken(myTkn)
        myTknCount, oppTknCount, transcript = runGame(myTkn, holeLimit)
        totalMyTkn += myTknCount
        totalAll += myTknCount + oppTknCount
        print(f"Game {gameNum+1:4}: Current Game: {myTknCount}/{myTknCount+oppTknCount} ({myTknCount/(myTknCount+oppTknCount)*100:.3f}%)\t|\tRunning Total: {totalMyTkn}/{totalAll} ({totalMyTkn/totalAll*100:.3f}%)")
        # break
    return totalMyTkn, totalAll

def reportResults(totalMyTkn, totalAll):
    print(f"Total x: {totalMyTkn}")
    print(f"Total All: {totalAll}")
    print(f"Percentage: {totalMyTkn/totalAll*100}%")

def runGame(myTkn, holeLimit):
    oppositeTkn = getOppositeToken(myTkn)
    brd = '.'*27+'ox......xo'+'.'*27
    tokens = ['x', 'o']
    tknCt = ['x', 'o'].index(myTkn)
    moves = ''
    while not gameOver(brd):
        tkn = tokens[tknCt]
        # Either next or next-next line works
        # if tkn == myTkn: move = quickMove(brd, tkn)
        if tkn == myTkn: move = myFile.quickMove(brd, tkn)
        else: 
            move = randomMove(brd, tkn)
            # move = myFile.quickMove(brd, tkn, holeLimit)
            # if brd.count(".") <= holeLimit: move = move[-1]
        moves += str(move)
        if move == -1: tknCt = (tknCt + 1) % 2; continue
        brd = makeMove(brd, move, findPossibleMoves(brd, tkn), tkn)
        # print(f"{tkn} plays {move}\t|\tMy token: {myTkn}")
        # print2D(brd, spaces=True)
        tknCt = (tknCt + 1) % 2
    return brd.count(myTkn), brd.count(oppositeTkn), moves
    
def print2D(choicesBoard, spaces=False):
    for i in range(0, 64, 8): print(choicesBoard[i:i+8])
    if spaces: print("\n\n")

def gameOver(board): return board.count(".") == 0 or not(findPossibleMoves(board, 'x') or findPossibleMoves(board, 'o'))

def randomMove(board, token):
    validMoves = findPossibleMoves(board, token)
    if len(validMoves) == 0: return -1
    return random.choice(sorted(list(validMoves.keys())))

def makeMove(board, move, validMoves, token):
    board = board[:move] + token + board[move+1:]
    for idx in validMoves[move]: board = board[:idx] + token + board[idx+1:]
    return board

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

def idxToPos(idx): return (idx // 8, idx % 8)

def posToIdx(row, col): return row * 8 + col
    
def getOppositeToken(token): return 'o' if token == 'x' else 'x'

if __name__ == "__main__": main()