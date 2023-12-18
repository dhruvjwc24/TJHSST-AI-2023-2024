import sys; args = sys.argv[1:]

lookupTable = {}
indices = [i for i in range(81)]
blocks = [{0,1,2,9,10,11,18,19,20}, {3,4,5,12,13,14,21,22,23}, {6,7,8,15,16,17,24,25,26}, {27,28,29,36,37,38,45,46,47}, {30,31,32,39,40,41,48,49,50}, {33,34,35,42,43,44,51,52,53}, {54,55,56,63,64,65,72,73,74}, {57,58,59,66,67,68,75,76,77}, {60,61,62,69,70,71,78,79,80}]

def getRowIndices(i):
    return {j for j in range(i//9*9, i//9*9+9) if j != i}

def getColIndices(i):
    return {j for j in range(i%9, 81, 9) if j != i}

def getBlockIndices(i):
    return blocks[i//27*3+i%9//3]

def isSolved(pzl):
    return not("." in pzl)

def isInvalid(pzl):
    solved = True
    visited = None
    for i, c in enumerate(pzl):
        rowCheck = getRowIndices(i)
        colCheck = getColIndices(i)
        blockCheck = getBlockIndices(i)
        if i in blockCheck: blockCheck.remove(i)
        # print(f"Row Check: {rowCheck}\nCol Check: {colCheck}\nBlock Check: {blockCheck}")
        visited = []
        for idx in rowCheck:
            if pzl[idx] in visited and pzl[idx] != ".": return True
            visited.append(pzl[idx])                 
        visited = []
        for idx in colCheck:
            if pzl[idx] in visited and pzl[idx] != ".": return True
            visited.append(pzl[idx])   
        visited = []
        for idx in blockCheck:            
            if pzl[idx] in visited and pzl[idx] != ".": return True
            visited.append(pzl[idx])  
        return False

def bruteForce(pzl):
    if isInvalid(pzl): return ""
    if isSolved(pzl): return pzl
    pos = pzl.find(".")
    choicesSet = [str(i) for i in range(1, 10) if pzl.count(str(i)) < 9]
    for choice in choicesSet:
        subPzl = pzl[:pos] + choice + pzl[pos+1:]
        bf = bruteForce(subPzl)
        if bf: return bf
    return ""

def get2D(pzl):
    return pzl[:9] + "\n" + pzl[9:18]+ "\n" + pzl[18:27]+ "\n"+ pzl[27:36] + "\n" + pzl[36:45]+ "\n" + pzl[45:54]+ "\n"+ pzl[54:63] + "\n" + pzl[63:72]+ "\n" + pzl[72:]

def checkSum(pzl):
    asciList = [ord(c) for c in pzl]
    return sum(asciList)-min(asciList)*len(pzl)


# args = ["Sudoku/puzzles.txt"]
pzls = open(args[0]).read().split("\n")

for i, pzl in enumerate(pzls):
    sol = bruteForce(pzl)
    print(f"{i+1} {pzl}\n   {sol} {checkSum(sol)}")

#Dhruv Chandna Period 6 2025


