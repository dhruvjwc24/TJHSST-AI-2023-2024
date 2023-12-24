import sys; args = sys.argv[1:]

def updateStats(funcName):
    if funcName in STATS_COUNTER: STATS_COUNTER[funcName] += 1
    else : STATS_COUNTER[funcName] = 1

def isSolved(pzl): return not("." in pzl)

def makePossibles(pzl):
    possibles = []
    for idx, c in enumerate(pzl):
        if c == ".":
            idxChecks = lenData["idxChecks"][idx]
            values = {pzl[i] for i in idxChecks if pzl[i] != "."}
            possibleValues = lenData["symset"] - values
            possibles.append(possibleValues)
        else: 
            possibles.append(None)
    
    return fwdLooking(pzl, possibles)

def fwdLooking(pzl, possibles):
    for idx, psbls in enumerate(possibles):
        if psbls == None: continue
        if len(psbls) == 0: return "", ""
        if len(psbls) == 1:
            val = psbls.pop()
            subPzl = pzl[:idx] + val + pzl[idx+1:]
            possibles[idx] = None
            for nbrIdx in lenData["idxChecks"][idx]:
                if possibles[nbrIdx] == None: continue
                if val in possibles[nbrIdx]: 
                    possibles[nbrIdx].remove(val)
                    if len(possibles[nbrIdx]) == 0: 
                        return "", ""
            return fwdLooking(subPzl, possibles)
    return pzl, possibles

def findBestPeriod(possibles):
    minLen = 999
    idx = -1
    for i, tup in enumerate(possibles):
        if tup == None: continue
        if len(tup) == 0: return -1
        if (tupLen:=len(tup)) < minLen:
            minLen = tupLen
            idx = i
        if minLen == 1: break
    return idx

def isInvalid(possibles):
    for psblsSet in possibles:
        if psblsSet == None: continue
        if len(psblsSet) == 0: return True
    return False
            
def bruteForce(pzl, myPossibles):
    if isInvalid(myPossibles): return None
    if isSolved(pzl): return pzl
    bestDot = findBestPeriod(myPossibles)
    if bestDot == -1: return ""
    psbls = myPossibles[bestDot]
    
    if len(psbls) == 1: 
        subPzl = pzl[:bestDot] + psbls.pop() + pzl[bestDot+1:]
        myPossibles[bestDot] = None
        for idx in lenData["idxChecks"][bestDot]: 
            if myPossibles[idx] == None: continue
            if psbls in myPossibles[idx]:
                myPossibles[idx] = myPossibles[idx].remove(psbls)
        return bruteForce(subPzl, myPossibles)

    for choice in psbls:
        # shallow copy to test each choice
        myPossiblesCopy = [*myPossibles]
        myPossiblesCopy[bestDot] = None
        # create potential puzzle with possible choice integrated
        subPzl = pzl[:bestDot] + choice + pzl[bestDot+1:]
        # for idx in nbrs check if the potewntial choice is in the possibles set for that choice, then if it is, remove it from the copy
        for idx in lenData["idxChecks"][bestDot]: 
            # if that index alr has a value
            if myPossiblesCopy[idx] == None: continue
            if choice in myPossiblesCopy[idx]:
                myPossiblesCopy[idx] = myPossibles[idx] - {choice}
                if myPossiblesCopy[idx] == None: continue
                if(len(myPossiblesCopy[idx])==0): 
                    return None
        bf = bruteForce(subPzl, myPossiblesCopy)
        if not bf: continue
        return bf
    return ""

def checkSum(pzl):
    asciList = [ord(c) for c in pzl]
    return sum(asciList)-min(asciList)*pzlLen

def makeSymSet(pzl, N):
    currSyms = {c for c in pzl if c != "."}
    spareSyms = {str(i) for i in range(1, N+1)}
    while len(currSyms) < N:
        poss = spareSyms.pop()
        if(poss not in currSyms): currSyms.add(poss)
    return currSyms

def makeLocs(pzlLen):
    N = int(pzlLen**0.5)
    rowIndices = [set(range(i*N, i*N+N)) for i in range(N)]
    colIndices = [set(range(i, pzlLen, N)) for i in range(N)]
    blockIndices = get_sudoku_block_indices_flat(N)
    return rowIndices + colIndices + blockIndices
    
def get_sudoku_block_indices_flat(N):
    # Compute the dimensions of each block
    width, height = getDimensions(N)
    blocks = []
    for block_row in range(N // height):
        for block_col in range(N // width):
            block = set()
            for row in range(height):
                for col in range(width):
                    index = (block_row * height + row) * N + (block_col * width + col)
                    block.add(index)
            blocks.append(block)
    return blocks

def create_idx_checks(locs, pzlLen):
    idx_checks = {}
    for idx in range(pzlLen):
        checks = set()
        for loc in locs:
            if idx in loc:
                checks = checks.union(loc)
        checks.remove(idx)
        idx_checks[idx] = checks
    return idx_checks

def getDimensions(N):
    l = N
    w = int(l**0.5)
    while l % w != 0:
        w+=1
    return (max(t:=(w, l//w)), min(t))

def setGlobals(puzzleLen):
    lenData = {}
    N = int(puzzleLen ** 0.5)
    gw, gh = getDimensions(N)
    SYMSET = makeSymSet(pzl, N)
    LOCS = makeLocs(pzlLen)
    idxChecks = create_idx_checks(LOCS, puzzleLen)
    lenData["pzlLen"], lenData["N"], lenData["gw"], lenData["gh"], lenData["symset"], lenData["locs"], lenData["idxChecks"], lenData["possibles"] = puzzleLen, N, gw, gh, None, LOCS, idxChecks, None
    return lenData

def print2D(pzl):
    N = int(len(pzl)**0.5)
    for i in range(N):
        print(pzl[i*N:i*N+N])

def main():
    global lookupTable, pzlLen, lenData, pzl, STATS_COUNTER
    lookupTable = {}
    args = ["InputFiles/puzzles_8_standard_size_81_and_all_numberspuzzlesAllNumsAndSize81.txt"]
    STATS_COUNTER = {}
    PZLS = open(args[0]).read().split("\n")
    lenData = None
    for idx, pzl in enumerate(PZLS):
        pzlLen = len(pzl)
        if pzlLen in lookupTable: lenData = lookupTable[pzlLen]
        else: lookupTable[pzlLen] = setGlobals(pzlLen); lenData = lookupTable[pzlLen]
        symset = makeSymSet(pzl, lenData["N"])
        lenData["symset"] = symset
        newPzl, lenData["possibles"] = makePossibles(pzl)
        print(f"{idx+1:3}: {pzl}")
        pzl = newPzl
        sol = bruteForce(pzl, lenData["possibles"])
        print(f"{' '*5}{sol} {checkSum(sol)}")

if __name__ == "__main__":
    main()

#Dhruv Chandna Period 6 2025