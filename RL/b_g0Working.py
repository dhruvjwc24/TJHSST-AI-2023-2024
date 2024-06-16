import sys; args = sys.argv[1:]
import re

def print2D(myStr, width):
    for i in range(0, len(myStr), width):
        print(myStr[i:i+width])

def getDimensions(numNodes):
    numNodes
    width = int(numNodes**0.5)
    while numNodes % width != 0:
        width+=1
    return (max(dims:=(width, numNodes//width)), min(dims))

def getPosFromIdx(idx, width):
    return idx//width, idx%width

def getIdxFromPos(pos, w):
    return pos[0]*w+pos[1]

def getCardinalNbrs(idx, width, height):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    pos = getPosFromIdx(idx, width)
    edges = set()
    for direction in directions:
        newPos = (pos[0]+direction[0], pos[1]+direction[1])
        if newPos[0] >= 0 and newPos[0] < height and newPos[1] >= 0 and newPos[1] < width:
            edges.add(getIdxFromPos(newPos, width))
    return edges

def createGrf(grf):
    for vertex in range(grf["grfProperties"]["numVertices"]):
        nbrs = getCardinalNbrs(vertex, grf["grfProperties"]["width"], grf["grfProperties"]["height"])
        grf["grfValues"].append([set(), {}])
        for nbr in nbrs:
            grf["grfValues"][vertex][0].add((nbr, ""))
    return grf

def grfParse(lstArgs):
    grf = {"grfValues": [], "grfProperties": {}}
    rwdValuation, numVertices, width, height, rwd = 1, 0, 0, 0, 12
    cardinalDirsDict = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1), "": (0, 0)}
    numVertices = int(lstArgs[0])
    grf["grfProperties"]["numVertices"] = numVertices
    del lstArgs[0]
    if not lstArgs: 
        width, height = getDimensions(numVertices)
        grf["grfProperties"]["width"] = width
        grf["grfProperties"]["height"] = height
        grf = createGrf(grf)
        return grf
    if not(lstArgs[0].isnumeric()): width, height = getDimensions(numVertices)
    else: width = int(lstArgs[0]); height = numVertices // width; del lstArgs[0]
    grf["grfProperties"]["width"] = width
    grf["grfProperties"]["height"] = height

    grf = createGrf(grf)
    for i, arg in enumerate(lstArgs):
        # G0
        if "G" in arg:
            rwdValuation = int(arg[1:])
            grf["grfProperties"]["rwdValuation"] = rwdValuation
        # B#[NSEW]+
        elif "N" in arg or "E" in arg or "S" in arg or "W" in arg:
            vertex = ""
            for i in range(1, len(arg)):
                if arg[i].isnumeric():
                    vertex += arg[i]
                else:
                    break
            vertex = int(vertex)
            dirs = arg[i:]
            nbrRowColDirs = [cardinalDirsDict[myDir] for myDir in dirs]
            potNbrs = set()
            for nbrRowColDir in nbrRowColDirs:
                vertexRow, vertexCol = getPosFromIdx(vertex, width)
                newRow, newCol = vertexRow+nbrRowColDir[0], vertexCol+nbrRowColDir[1]
                if newRow >= 0 and newRow < height and newCol >= 0 and newCol < width:
                    potNbrs.add(getIdxFromPos((newRow, newCol), width))
            
            toAdd = set()
            toRemove = set()

            for nbr in grf["grfValues"][vertex][0]:
                if nbr[0] not in potNbrs: continue
                toRemove.add(nbr[0])
            toAdd = potNbrs - toRemove

            nbrToAddSet = set()
            nbrToRemoveSet = set()
            
            for nbr in grf["grfValues"][vertex][0]:
                if nbr[0] in toRemove:
                    nbrToRemoveSet.add(nbr)
            for idx in toAdd:
                nbrToAddSet.add((idx, ""))

            grf["grfValues"][vertex][0] -= nbrToRemoveSet
            grf["grfValues"][vertex][0] |= nbrToAddSet

            for addedNbr in toAdd:
                grf["grfValues"][addedNbr][0].add((vertex, ""))
            for removedNbr in toRemove:
                for nbr in grf["grfValues"][removedNbr][0]:
                    if nbr[0] == vertex:
                        grf["grfValues"][removedNbr][0].discard(nbr)
                        break
        # B#
        elif "B" in arg:
            vertex = int(arg[1:])
            
            potNbrs = getCardinalNbrs(vertex, width, height)
            toAdd = set()
            toRemove = set()

            for nbr in grf["grfValues"][vertex][0]:
                toRemove.add(nbr[0])
            toAdd = potNbrs - toRemove

            nbrToAddSet = set()
            nbrToRemoveSet = set()
            
            for nbr in grf["grfValues"][vertex][0]:
                if nbr[0] in toRemove:
                    nbrToRemoveSet.add(nbr)
            for idx in toAdd:
                nbrToAddSet.add((idx, ""))

            grf["grfValues"][vertex][0] -= nbrToRemoveSet
            grf["grfValues"][vertex][0] |= nbrToAddSet

            for addedNbr in toAdd:
                grf["grfValues"][addedNbr][0].add((vertex, ""))
            for removedNbr in toRemove:
                for nbr in grf["grfValues"][removedNbr][0]:
                    if nbr[0] == vertex:
                        grf["grfValues"][removedNbr][0].discard(nbr)
                        break        
        # R#
        elif ":" not in arg:
            vertex = int(arg[1:])
            grf["grfValues"][vertex][1]["rwd"] = rwd
        # R:#
        elif len(arg.split(":")[0]) == 1:
            vertexRwd = arg[2:]
            if not vertexRwd: vertexRwd = rwd
            else: vertexRwd = int(vertexRwd)
            rwd = vertexRwd
        # R#:#
        else:
            split = arg.split(":")
            vertex, vertexRwd = int(split[0][1:]), int(split[1])
            grf["grfValues"][vertex][1]["rwd"] = vertexRwd
                
    return grf

def BFS(grf):
    dirSymbols = {"UR": "V", "URD": "W", "RD": "S", "LRD": "T", "LD": "E", "ULD": "F", "UL": "M", "ULR": "N", "UD": "|", "LR": "-", "ULRD": "+", "U": "U", "R": "R", "D": "D", "L": "L", "": "."}
    # dirSymbols = {"NW": "J", "N": "U", "NWE": "^", "NE": "L", "NWS": "<", "W": "L", "NWES": "+", "E": "R", "NES": ">", "WS": "7", "WES": "v", "S": "D", "ES": "r", "WE": "-", "NS": "|", "": ".", ".": "."}
    shortestPaths = ["" for i in range(grf["grfProperties"]["numVertices"])]
    rwdIdxs = [idx for idx in range(len(grf["grfValues"])) if grf["grfValues"][idx][1]]
    
    if not rwdIdxs: return "." * grf["grfProperties"]["numVertices"]
    for vertex in range(len(shortestPaths)):
        if vertex == 20:
            pass
        maxRwd = 0
        for rwdIdx in rwdIdxs:
            # if shortestPaths[vertex] and shortestPaths[vertex][0] == 0: continue
            rwd, path = shortestPathVertex(vertex, rwdIdx, grf)
            if path and len(path) == 1: shortestPaths[vertex] = [0, rwd]; break
            if shortestPaths[vertex] == "" and path: 
                maxRwd = rwd
                shortestPaths[vertex] = [len(path)-1, maxRwd]
            elif path and rwd >= maxRwd:
                if rwd > maxRwd:
                    maxRwd = rwd
                    shortestPaths[vertex] = [len(path)-1, maxRwd]
                elif len(path)-1 < shortestPaths[vertex][0]:
                    shortestPaths[vertex] = [len(path)-1, maxRwd]
                # shortestPaths[vertex] = len(path)-1
            else:
                continue
        if shortestPaths[vertex] == "":
            shortestPaths[vertex] = -1
    grfPaths = ""
    for vertex in range(len(shortestPaths)):
        if vertex in rwdIdxs:
            grfPaths += "*"
            continue
        if shortestPaths[vertex] == -1:
            grfPaths += "."
            continue
        grfPath = ""
        # cardinalEdges = getCardinalEdges(vertex, grf["grfProperties"]["width"], grf["grfProperties"]["height"])
        pathLength = shortestPaths[vertex][0]
        nbrs = sorted([nbr[0] for nbr in grf["grfValues"][vertex][0]])
        for nbr in nbrs:
            if shortestPaths[nbr][0]+1 == pathLength and shortestPaths[nbr][1] == shortestPaths[vertex][1]:
                # if "rwd" in grf["grfValues"][nbr][1] and grf["grfValues"][nbr][1]["rwd"] != shortestPaths[vertex][1]: continue
                if nbr == vertex-grf["grfProperties"]["width"]:
                    grfPath += "U"
                elif nbr == vertex-1:
                    grfPath += "L"
                elif nbr == vertex+1:
                    grfPath += "R"
                elif nbr == vertex+grf["grfProperties"]["width"]:
                    grfPath += "D"
                else:
                    grfPath += "."
  
        if "." in grfPath and len(grfPath) > 1:
            grfPath = grfPath.replace(".", "")
        grfPaths += dirSymbols[grfPath]

    return grfPaths

def shortestPathVertex(root, goal, grf):
    parseMe = [root]
    dctSeen = {root: ""}
    while parseMe:
        item = parseMe.pop(0)
        if item == goal: 
            path = []
            while goal != "":
                # if goal != item and "rwd" in grf["grfValues"][goal][1]: return None, None
                path.append(goal)
                goal = dctSeen[goal]
            return grf["grfValues"][item][1]["rwd"], list(reversed(path))
            # return list(reversed(path))
        for nbr in grf["grfValues"][item][0]:
            if nbr[0] not in dctSeen:
                if "rwd" in grf["grfValues"][nbr[0]][1] and nbr[0] != goal: continue
                parseMe.append(nbr[0])
                dctSeen[nbr[0]] = item
    return None, None

def main():
    # args = "25 R17 B8 B13 B7 R15:5 R21:6 G0 R23 B18 B12N B8W B21E B4S"
    # args = "25 R13 B16 B17 B11 R3:5 R9:6 G0 R1 B20 B10S B16N"
    # args = "45 R:5 R10 R14:500 B42 B23 B3 B15 B40 B21 B2 B41 G0 R39 R3 B21W B21S B14S B1E B33N"
    # args = "6 2 B0S B1S G0 R4"
    # args = "1"
    if type(args) == str: argsLst = args.split(" ")
    else: argsLst = args
    grf = grfParse(argsLst)
    
    bfs = BFS(grf)
    print2D(bfs, grf["grfProperties"]["width"])

    return

if __name__ == "__main__": main()

#Dhruv Chandna Period 6 2025