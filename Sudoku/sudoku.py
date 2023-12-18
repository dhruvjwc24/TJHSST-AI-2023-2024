import sys; args = sys.argv[1:]
import time

def updateStats(funcName):
    if funcName in STATS_COUNTER: STATS_COUNTER[funcName] += 1
    else : STATS_COUNTER[funcName] = 1

def getDimensions(pzlLen):
    l = pzlLen
    w = int(l**0.5)
    while l % w != 0:
        w+=1
    return (max(t:=(w, l//w)), min(t))

def isSolved(pzl):
    # updateStats("isSolved")
    return not("." in pzl)

def isInvalid(pzl):
    # updateStats("isInvalid")
    for cs in lenData["locs"]:
        if len((ls:=[pzl[i] for i in cs if pzl[i]!='.']))!=len({*ls}):
            return True
    return False

def findBestPeriod(pzl):
    # updateStats("findBestPeriod")
    vals = []
    for idx, c in enumerate(pzl):
        if c == ".":
            idxChecks = lenData["idxChecks"][idx]
            values = {pzl[i] for i in idxChecks if pzl[i] != "."}
            possibleValues = lenData["symset"] - values
            if(len(possibleValues) == 1):
                return idx, possibleValues
            vals.append((len(possibleValues), idx, possibleValues))
    return min(vals)[1:]
            #print(idx, possibleValues)
            

def bruteForce(pzl):
    # updateStats("bruteForce")
    # if isInvalid(pzl): return ""
    if isSolved(pzl): return pzl
    bestIdxAndVal = findBestPeriod(pzl)
    pos = bestIdxAndVal[0]
    choicesSet = bestIdxAndVal[1]
    #pos = pzl.find(".")
    N = lenData["N"]
    # choicesSet = [str(i+1) for i in range(N)]
    for choice in choicesSet:
        subPzl = pzl[:pos] + choice + pzl[pos+1:]
        bf = bruteForce(subPzl)
        if bf: return bf
    return ""

# def get2D(pzl):
#     N = lenData["N"]
#     return [pzl[idx:idx+N] for idx in range(0, pzlLen, N)].split("\n")

def checkSum(pzl):
    asciList = [ord(c) for c in pzl]
    return sum(asciList)-min(asciList)*pzlLen

def getBlocks(pzlLen):
    return [{0,1,2,9,10,11,18,19,20}, {3,4,5,12,13,14,21,22,23}, {6,7,8,15,16,17,24,25,26}, {27,28,29,36,37,38,45,46,47}, {30,31,32,39,40,41,48,49,50}, {33,34,35,42,43,44,51,52,53}, {54,55,56,63,64,65,72,73,74}, {57,58,59,66,67,68,75,76,77}, {60,61,62,69,70,71,78,79,80}]

def setGlobals(puzzleLen):
    # updateStats("setGlobals")
    lenData = {}
    N = int(puzzleLen**0.5)
    gw, gh = getDimensions(N)
    SYMSET = {str(i) for i in range(1, N+1)}
    indices = [ i for i in range(puzzleLen)]
    # LOCS = setLocs(indices, N)
    LOCS = [{0,1,2,3,4,5,6,7,8},{9,10,11,12,13,14,15,16,17},{18,19,20,21,22,23,24,25,26},{27,28,29,30,31,32,33,34,35},{36,37,38,39,40,41,42,43,44},{45,46,47,48,49,50,51,52,53},{54,55,56,57,58,59,60,61,62},{63,64,65,66,67,68,69,70,71},{72,73,74,75,76,77,78,79,80},{0,9,18,27,36,45,54,63,72},{1,10,19,28,37,46,55,64,73},{2,11,20,29,38,47,56,65,74},{3,12,21,30,39,48,57,66,75},{4,13,22,31,40,49,58,67,76},{5,14,23,32,41,50,59,68,77},{6,15,24,33,42,51,60,69,78},{7,16,25,34,43,52,61,70,79},{8,17,26,35,44,53,62,71,80},{0,1,2,9,10,11,18,19,20},{3,4,5,12,13,14,21,22,23},{6,7,8,15,16,17,24,25,26},{27,28,29,36,37,38,45,46,47},{30,31,32,39,40,41,48,49,50},{33,34,35,42,43,44,51,52,53},{54,55,56,63,64,65,72,73,74},{57,58,59,66,67,68,75,76,77},{60,61,62,69,70,71,78,79,80}]
    idxChecks = {0:{0,1,2,3,4,5,6,7,8,72,9,10,11,18,19,20,27,36,45,54,63},1:{0,1,2,3,4,5,6,7,8,64,73,10,9,11,18,19,20,28,37,46,55},2:{0,1,2,3,4,5,6,7,8,9,10,11,65,74,18,19,20,29,38,47,56},3:{0,1,2,3,4,5,6,7,8,66,75,12,13,14,21,22,23,30,39,48,57},4:{0,1,2,3,4,5,6,7,8,67,12,13,14,76,21,22,23,31,40,49,58},5:{0,1,2,3,4,5,6,7,8,68,12,13,14,77,21,22,23,32,41,50,59},6:{0,1,2,3,4,5,6,7,8,69,78,15,16,17,24,25,26,33,42,51,60},7:{0,1,2,3,4,5,6,7,8,70,79,16,15,17,24,25,26,34,43,52,61},8:{0,1,2,3,4,5,6,7,8,71,15,80,17,16,24,25,26,35,44,53,62},9:{0,1,2,72,9,10,11,12,13,14,15,16,17,18,19,20,27,36,45,54,63},10:{64,1,0,2,9,10,11,12,13,14,15,16,17,73,19,18,20,28,37,46,55},11:{0,1,2,65,9,10,11,12,13,14,15,16,17,18,19,20,29,38,47,74,56},12:{66,3,4,5,9,10,11,12,13,14,15,16,17,75,21,22,23,30,39,48,57},13:{3,4,5,67,9,10,11,12,13,14,15,16,17,76,21,22,23,31,40,49,58},14:{3,4,5,68,9,10,11,12,13,14,15,16,17,77,21,22,23,32,41,50,59},15:{69,6,7,8,9,10,11,12,13,14,15,16,17,78,24,25,26,33,42,51,60},16:{70,7,6,9,10,11,12,13,14,79,16,15,17,24,25,26,34,8,43,52,61},17:{6,7,8,9,10,11,12,13,14,15,16,17,80,24,25,26,35,71,44,53,62},18:{0,1,2,72,9,10,11,18,19,20,21,22,23,24,25,26,27,36,45,54,63},19:{64,1,0,2,73,10,9,11,18,19,20,21,22,23,24,25,26,28,37,46,55},20:{0,65,2,1,9,74,11,10,18,19,20,21,22,23,24,25,26,29,38,47,56},21:{66,3,4,5,75,12,13,14,18,19,20,21,22,23,24,25,26,30,39,48,57},22:{3,4,5,67,12,13,14,76,18,19,20,21,22,23,24,25,26,31,40,49,58},23:{3,4,5,68,12,13,14,77,18,19,20,21,22,23,24,25,26,32,41,50,59},24:{69,6,7,8,78,15,16,17,18,19,20,21,22,23,24,25,26,33,42,51,60},25:{70,7,6,8,79,16,15,18,19,20,21,22,23,24,25,26,17,34,43,52,61},26:{6,71,8,7,15,80,17,18,19,20,21,22,23,24,25,26,16,35,44,53,62},27:{0,72,9,18,27,28,29,30,31,32,33,34,35,36,37,38,45,46,47,54,63},28:{64,1,73,10,19,27,28,29,30,31,32,33,34,35,36,37,38,45,46,47,55},29:{65,2,74,11,20,27,28,29,30,31,32,33,34,35,36,37,38,45,46,47,56},30:{66,3,75,12,21,27,28,29,30,31,32,33,34,35,39,40,41,48,49,50,57},31:{67,4,76,13,22,27,28,29,30,31,32,33,34,35,39,40,41,48,49,50,58},32:{68,5,77,14,23,27,28,29,30,31,32,33,34,35,39,40,41,48,49,50,59},33:{69,6,78,15,24,27,28,29,30,31,32,33,34,35,42,43,44,51,52,53,60},34:{70,7,79,16,25,27,28,29,30,31,32,33,34,35,42,43,44,51,52,53,61},35:{71,8,80,17,26,27,28,29,30,31,32,33,34,35,42,43,44,51,52,53,62},36:{0,72,9,18,27,28,29,36,37,38,39,40,41,42,43,44,45,46,47,54,63},37:{64,1,73,10,19,27,28,29,36,37,38,39,40,41,42,43,44,45,46,47,55},38:{65,2,74,11,20,27,28,29,36,37,38,39,40,41,42,43,44,45,46,47,56},39:{66,3,75,12,21,30,31,32,36,37,38,39,40,41,42,43,44,48,49,50,57},40:{67,4,76,13,22,30,31,32,36,37,38,39,40,41,42,43,44,48,49,50,58},41:{68,5,77,14,23,30,31,32,36,37,38,39,40,41,42,43,44,48,49,50,59},42:{69,6,78,15,24,33,34,35,36,37,38,39,40,41,42,43,44,51,52,53,60},43:{70,7,79,16,25,33,34,35,36,37,38,39,40,41,42,43,44,51,52,53,61},44:{71,8,80,17,26,33,34,35,36,37,38,39,40,41,42,43,44,51,52,53,62},45:{0,72,9,18,27,28,29,36,37,38,45,46,47,48,49,50,51,52,53,54,63},46:{64,1,73,10,19,27,28,29,36,37,38,45,46,47,48,49,50,51,52,53,55},47:{65,2,74,11,20,27,28,29,36,37,38,45,46,47,48,49,50,51,52,53,56},48:{66,3,75,12,21,30,31,32,39,40,41,45,46,47,48,49,50,51,52,53,57},49:{67,4,76,13,22,30,31,32,39,40,41,45,46,47,48,49,50,51,52,53,58},50:{68,5,77,14,23,30,31,32,39,40,41,45,46,47,48,49,50,51,52,53,59},51:{69,6,78,15,24,33,34,35,42,43,44,45,46,47,48,49,50,51,52,53,60},52:{70,7,79,16,25,33,34,35,42,43,44,45,46,47,48,49,50,51,52,53,61},53:{71,8,80,17,26,33,34,35,42,43,44,45,46,47,48,49,50,51,52,53,62},54:{64,65,0,72,73,74,9,18,27,36,45,54,55,56,57,58,59,60,61,62,63},55:{64,65,1,72,73,74,10,19,28,37,46,54,55,56,57,58,59,60,61,62,63},56:{64,65,2,72,73,74,11,20,29,38,47,54,55,56,57,58,59,60,61,62,63},57:{66,67,68,3,75,76,77,12,21,30,39,48,54,55,56,57,58,59,60,61,62},58:{66,67,68,4,75,76,77,13,22,31,40,49,54,55,56,57,58,59,60,61,62},59:{66,67,68,5,75,76,77,14,23,32,41,50,54,55,56,57,58,59,60,61,62},60:{69,70,71,6,78,79,80,15,24,33,42,51,54,55,56,57,58,59,60,61,62},61:{69,70,7,71,78,79,16,80,25,34,43,52,54,55,56,57,58,59,60,61,62},62:{69,70,71,8,78,79,80,17,26,35,44,53,54,55,56,57,58,59,60,61,62},63:{64,65,0,66,67,68,69,70,72,73,74,9,71,18,27,36,45,54,55,56,63},64:{64,65,1,66,67,68,69,70,72,73,74,10,71,19,28,37,46,54,55,56,63},65:{64,65,2,66,67,68,69,70,72,73,74,11,71,20,29,38,47,54,55,56,63},66:{64,65,66,67,68,3,69,70,71,75,76,77,12,21,30,39,48,57,58,59,63},67:{64,65,66,67,68,4,69,70,71,75,76,77,13,22,31,40,49,57,58,59,63},68:{64,65,66,67,68,5,69,70,71,75,76,77,14,23,32,41,50,57,58,59,63},69:{64,65,66,67,68,69,70,71,6,78,79,80,15,24,33,42,51,60,61,62,63},70:{64,65,66,67,68,69,70,7,71,78,79,16,80,25,34,43,52,60,61,62,63},71:{64,65,66,67,68,69,70,71,8,78,79,80,17,26,35,44,53,60,61,62,63},72:{0,64,65,72,73,74,75,76,77,78,79,80,9,18,27,36,45,54,55,56,63},73:{64,65,1,72,73,74,75,76,77,78,79,80,10,19,28,37,46,54,55,56,63},74:{64,65,2,72,73,74,75,76,77,78,79,80,11,20,29,38,47,54,55,56,63},75:{66,67,68,3,72,73,74,75,76,77,78,79,80,12,21,30,39,48,57,58,59},76:{66,67,68,4,72,73,74,75,76,77,78,79,80,13,22,31,40,49,57,58,59},77:{66,67,68,5,72,73,74,75,76,77,78,79,80,14,23,32,41,50,57,58,59},78:{69,70,71,72,73,74,75,76,77,78,79,80,15,24,6,33,42,51,60,61,62},79:{69,70,7,72,73,74,75,76,77,78,79,80,16,25,34,71,43,52,60,61,62},80:{69,70,71,72,73,74,75,76,77,78,79,80,8,17,26,35,44,53,60,61,62}} 
    lenData["pzlLen"], lenData["N"], lenData["gw"], lenData["gh"], lenData["symset"], lenData["indices"], lenData["locs"], lenData["idxChecks"] = puzzleLen, N, gw, gh, SYMSET, indices, LOCS, idxChecks
    return lenData

# def setLocs(indices, N):
#     locs = []
#     for i in indices:
#         locs.append(getRowIndices(i, N))
#         locs.append(getColIndices(i, N))
#         locs.append(getBlockIndices(i))
#     return locs

# def getRowIndices(i, N):
#     return {j for j in range(i//N*N, i//N*N+N) if j != i}

# def getColIndices(i, N):
#     return {j for j in range(i%N, pzlLen, N) if j != i}

# def getBlockIndices(i):
#     return getBlocks(pzlLen)[i//27*3+i%9//3]

def main():
    # print((s:=time.time()))
    global lookupTable, pzlLen, lenData, STATS_COUNTER
    lookupTable = {}
    # STATS_COUNTER = {}
    # args = ["Sudoku Files/puzzles_1_standard_easy.txt"]
    # args = ["puzzles.txt"]
    PZLS = open(args[0]).read().split("\n")
    # setGlobals()
    for idx, pzl in enumerate(PZLS):
        pzlLen = len(pzl)
        if pzlLen not in lookupTable:
            # print(pzlLen)
            lookupTable[pzlLen] = setGlobals(pzlLen)
        lenData = lookupTable[pzlLen]
        # print(lenData["locs"])
        # break
        print(f"{idx+1:3}: {pzl}")
        sol = bruteForce(pzl)
        print(f"{' '*5}{sol} {checkSum(sol)}")
        # print(f"{' '*5}{sol} 324")
        # print(f"STATS: {STATS_COUNTER}")
        # print(f"Time: {time.time()-s} s\n")
# args = ["Sudoku/puzzles.txt"]
if __name__ == "__main__":
    main()

#Dhruv Chandna Period 6 2025