from re import search

CACHEMOVES = {}

def idxToPos(idx): return (idx // 8, idx % 8)

def posToIdx(row, col): return row * 8 + col

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

def checkSafeEdge(pos, line, brd, token):
    oppositeToken = getOppositeToken(token)
    ltStr = "".join([brd[idx] for idx in line[:line.index(pos)]])
    rbStr = "".join([brd[idx] for idx in line[line.index(pos)+1:][::-1]])
    return search(f"^{token}+{oppositeToken}*$", ltStr) or search(f"^{token}+{oppositeToken}*$", rbStr)

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
                if brd[posToIdx(r, c)] == eTkn or brd[posToIdx(r, c)] == ".": continue
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
    evaluation = 0
    # print(getNumCorners(board, token))
    #1
    evaluation += getNumCorners(board, token)**4
    # print(getNumSafeTokens(board, token))
    #17
    evaluation += getNumSafeTokens(board, token)**2
    # print(len(findPossibleMoves(board, token)))
    # evaluation -= len(findPossibleMoves(board, getOppositeToken(token)))**2
    #11
    evaluation += len(findPossibleMoves(board, token))**2
    # print(board.count(token))
    #17
    evaluation += board.count(token)**1

    return evaluation

def main():
    print(brdEval(".......................x...xx.xo...xxxxo..xxxxoo..oooooo.ooooooo", "o"))

if __name__ == "__main__": main()

#Dhruv Chandna 2025 Period 6