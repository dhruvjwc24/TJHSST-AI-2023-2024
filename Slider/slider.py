import sys; args = sys.argv[1:]

import time, math, random, re

def BFS(w, h, start, goal=None):
    icStart = inversionCount(start)
    icGoal = inversionCount(goal)
    startTime = time.process_time()
    if icStart%2!=icGoal%2 and w%2==1: return(f"{getBand(start, w, h)}\nSteps: -1\nTime: {str(float('%.3g' % (time.process_time()-startTime)))}s") 

    if goal == "": goal = "".join(sorted(start))
    if start == goal: 
        band = getBand(start, w, h)
        return(f"{band}\nSteps: 0\nTime: {str(float('%.3g' % (time.process_time()-startTime)))}s")
    parseMe = [start]
    dctSeen = {start: ""} #list of parents visited
    while parseMe:
        node = parseMe.pop(0)
        for nbr in neighbors(node, w, h):
            if nbr == goal:
                path = (dctSeen[node] + " " + node + " " + nbr).strip()
                pathLength = len(path.split(" "))-1

                band = getBand(path, w, h)
                return(f"{band}\nSteps: {pathLength}\nTime: {str(float('%.3g' % (time.process_time()-startTime)))}s")
                
            if nbr not in dctSeen:
                dctSeen[nbr] = dctSeen[node] + " " + node
                parseMe.append(nbr)

def getDimensions(start):
    #return (width, height)
    l = len(start)
    w = int(l**0.5)
    while l % w != 0:
        w+=1
    return (max(t:=(w, l//w)), min(t))

def getBand(path, w, h, bandMaxLength=12):
    pathList = path.split(" ")
    bandList = []
    for i in range(0, len(pathList), bandMaxLength):
        pathListBand = pathList[i:i+bandMaxLength]
        twoDList = []
        band = ""
        for state in pathListBand:
            twoDList.append(create2D(state, w, h))
        zipped = list(zip(*twoDList))
        for i, tup in enumerate(zipped):
            band += " ".join(tup) + "\n"
        bandList.append(band)
    return "\n".join(bandList)


def neighbors(puzzle, w, h):
    undInd = puzzle.index('_')
    col, row = undInd % w, undInd // w
    neighbors = []

    def is_valid(x, y):
        return 0 <= x < w and 0 <= y < h

    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_col, new_row = col + dx, row + dy
        if is_valid(new_col, new_row):
            new_undInd = new_row * w + new_col
            new_puzzle = list(puzzle)
            new_puzzle[undInd], new_puzzle[new_undInd] = new_puzzle[new_undInd], new_puzzle[undInd]
            neighbors.append(''.join(new_puzzle))

    return neighbors


def neighbors_helper(puzzle, neighborNums):
    neighbors = []
    for num in neighborNums:
        #print(puzzle)
        numInd = puzzle.index(num)
        undInd = puzzle.index('_')
        temp = [*puzzle]
        temp[undInd] = num
        temp[numInd] = '_'
        neighbors.append("".join(temp))
    return neighbors

def inversionCount(puzzle):
    count = 0
    for i in range((l:=len(puzzle))):
        for j in range(i+1, l):
            if puzzle[i] != '_' and puzzle[j] != '_' and puzzle[i] > puzzle[j]:
                count += 1
    return count

def create2D(state, w, h):
    return [state[w*i:w*(i+1)] for i in range(h)]


# puzzleStart = args[0]
# try:
#     puzzleGoal = args[1]
# except:
#     puzzleGoal = ""
# input = "_12475863" + " "
input = "RMCfDe5HajV8F42G0I6EQkdi_9XbcSTN7Y13AJghZPLlBOKWUDHEUATA RMCfDe5HajV8F42G0I6EQkdi9_XbcSTN7Y13AJghZPLlBOKWUDHEUATA" + " "
puzzleStart, puzzleGoal = input.split(" ")[0], input.split(" ")[1]

w, h = getDimensions(puzzleStart)
output = BFS(w, h, puzzleStart, puzzleGoal)
print(output)

#Dhruv Chandna Period 6 2025
