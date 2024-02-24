def setGlobals():
    global k, gameOverCount, distinctBoards
    distinctBoards = set()
    k = 3
    gameOverCount=0

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

def getPossibleMoves(brd):
    global k
    return {idx for idx, cell in enumerate(brd) if cell == "."}

def makeMove(brd, tkn, mv):
    return brd[:mv] + tkn + brd[mv+1:]

def isGameOver(brd):
    global k
    if len(getPossibleMoves(brd)) == 0 or getTokenCt(brd, "x") > 0 or getTokenCt(brd, "o") > 0: return True

def getNumberDifferentBoards(tkn = "x", distinctBoards = set(), brd = None):
    global gameOverCount, k
    # if starting board
    if not brd: brd = "." * k * k
    # This checks how many diff board configs
    distinctBoards.add(brd)
    
    if isGameOver(brd): 
        gameOverCount += 1
        # This checks how many diff ending configs
        distinctBoards.add(brd)
        return
    
    moves = getPossibleMoves(brd)

    next_tkn = "o" if tkn == "x" else "x"
    for move in moves:
        newBrd = makeMove(brd, tkn, move)
        getNumberDifferentBoards(next_tkn, distinctBoards, newBrd)
            
def main():
    setGlobals()
    getNumberDifferentBoards(distinctBoards=distinctBoards)
    print(len(distinctBoards))
    print(gameOverCount)

if __name__ == "__main__": main()

# Dhruv Chandna Period 6 2025
