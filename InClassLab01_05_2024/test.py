def setGlobals():
    global k, gameOverCount, distinctBoards, tkn, brd, scores
    scores = {"x": -1, "o": 1, "d": 0}
    brd = None
    tkn = None
    distinctBoards = set()
    k = 3
    gameOverCount=0

def makeMove(brd, tkn, mv):
    return brd[:mv] + tkn + brd[mv+1:]

def isGameOver(brd):
    global k
    if len(getPossibleMoves(brd)) == 0: return "d"
    if getTokenCt(brd, "x") > 0: return "x"
    if getTokenCt(brd, "o") > 0: return "o"
    return None
    # return len(getPossibleMoves(brd)) == 0 or getTokenCt(brd, "x") > 0 or getTokenCt(brd, "o") > 0

def getPossibleMoves(brd):
    global k
    return {idx for idx, cell in enumerate(brd) if cell == "."}

def getTokenCt(brd, tkn):
    global k
    rows = 0
    rows = [1 if set(brd[idx:idx+k]) == {tkn} else 0 for idx in range(0, len(brd), k)]
    cols = [1 if set(brd[idx::k]) == {tkn} else 0 for idx in range(k)]
    fwdDiag = ""
    for r, c in zip(list(range(k-1, -1, -1)), list(range(k))):
        fwdDiag += brd[r*k+c]
    fwdDiag = 1 if set(fwdDiag) == {tkn} else 0
    bckDiag = ""
    for r, c in zip(list(range(k)), list(range(k))):
        bckDiag += brd[r*k+c]
    bckDiag = 1 if set(bckDiag) == {tkn} else 0
    return sum(rows) + sum(cols) + fwdDiag + bckDiag

def printBoard(brd, spaces=False):
    global k
    for idx in range(0, len(brd), k):
        print(brd[idx:idx+k])
    if spaces: print("\n\n")    

def negamax(brd=None, tkn=None):
    # print(scores)
    if brd == None: brd = "x...x..oo"
    printBoard(brd, True)
    if tkn == None: tkn = "o" if brd.count("x") > brd.count("o") else "x"
    eTkn = "o" if tkn == "x" else "x"
    if (res:=isGameOver(brd)): return [scores[res]]
    bsf = [-2]
    for mv in getPossibleMoves(brd):
        newBrd = makeMove(brd, tkn, mv)
        nm = negamax(newBrd, eTkn)
        if -nm[0] > bsf[0]:
            bsf = [-nm[0]] + nm[1:] + [mv]
    return bsf
        # if newBrd not in distinctBoards:
        #     distinctBoards.add(newBrd)
        #     score = -negamax(newBrd, eTkn)
        #     if score > bsf[0]: bsf = [score, mv]
        

def main():
    # global tkn, brd
    setGlobals()
    out = negamax()
    print(out)

if __name__ == "__main__": main()


