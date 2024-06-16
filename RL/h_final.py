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
    grf["grfProperties"]["rwdValuation"] = rwdValuation

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
        # maxValuation = 0
        pots = []
        if vertex in rwdIdxs:
            # shortestPaths[vertex] = [0, grf["grfValues"][vertex][1]["rwd"]]
            pots.append((0, grf["grfValues"][vertex][1]["rwd"], grf["grfValues"][vertex][1]["rwd"]))
            shortestPaths[vertex] = pots
            continue
        for rwdIdx in rwdIdxs:
            # if shortestPaths[vertex] and shortestPaths[vertex][0] == 0: continue
            rwd, path = shortestPathVertex(vertex, rwdIdx, grf)
            if not path: continue
            pots.append((len(path)-1, rwd, rwd/(len(path)-1)))
            # if path and len(path)-1 == 0: shortestPaths[vertex] = [0, rwd]

            # rwdValuation = rwd
            # if grf["grfProperties"]["rwdValuation"] == 1:
            #     rwdValuation = rwd/(len(path)-1)
            # else:
            #     rwdValuation = rwd

            # if shortestPaths[vertex] == "" and path: 
            #     maxValuation = rwdValuation
            #     shortestPaths[vertex] = [len(path)-1, maxValuation]
            # elif path and rwdValuation >= maxValuation:
            #     if rwdValuation > maxValuation:
            #         maxValuation = rwdValuation
            #         shortestPaths[vertex] = [len(path)-1, maxValuation]
            #     elif len(path)-1 < shortestPaths[vertex][0]:
            #         shortestPaths[vertex] = [len(path)-1, maxValuation]
            #     # shortestPaths[vertex] = len(path)-1
            # else:
            #     continue
        if not pots:
            shortestPaths[vertex] = -1
        else:
            shortestPaths[vertex] = pots
    grfPaths = ""
    for vertex in range(len(shortestPaths)):
        if vertex == 22:
            pass
        if vertex in rwdIdxs:
            grfPaths += "*"
            continue
        if shortestPaths[vertex] == -1:
            grfPaths += "."
            continue
        grfPath = ""
        nbrs = sorted([nbr[0] for nbr in grf["grfValues"][vertex][0]])

        if grf["grfProperties"]["rwdValuation"] == 0:
            maxTupByRwd = sorted(shortestPaths[vertex], key=lambda x: x[1]+1/x[0], reverse=True)[0]
            pathLength, rwd = maxTupByRwd[0], maxTupByRwd[1]
            for nbr in nbrs:
                for tupInNbr in shortestPaths[nbr]:
                    if tupInNbr[0]+1 == pathLength and tupInNbr[1] == rwd:
                        if nbr == vertex-grf["grfProperties"]["width"]:
                            grfPath += "U"
                            break
                        elif nbr == vertex-1:
                            grfPath += "L"
                            break
                        elif nbr == vertex+1:
                            grfPath += "R"
                            break
                        elif nbr == vertex+grf["grfProperties"]["width"]:
                            grfPath += "D"
                            break
                        else:
                            grfPath += "."
                            break
        else:
            # maxTupByRwdOverLen = sorted(shortestPaths[vertex], key=lambda x: x[2], reverse=True)[0]
            # pathLength, rwd, rwdOverLen = maxTupByRwdOverLen[0], maxTupByRwdOverLen[1], maxTupByRwdOverLen[2]
            # for nbr in nbrs:
            #     for tupInNbr in shortestPaths[nbr]:
            #         # if (tupInNbr[0] + 1 == pathLength and tupInNbr[1] == rwd and tupInNbr[2] >= rwdOverLen) or (tupInNbr[0] + 1 == pathLength and tupInNbr[2] == rwdOverLen):
            #         if (tupInNbr[0] + 1 == pathLength and tupInNbr[1] == rwd and tupInNbr[2] >= rwdOverLen):
            #             if nbr == vertex-grf["grfProperties"]["width"]:
            #                 grfPath += "U"
            #                 break
            #             elif nbr == vertex-1:
            #                 grfPath += "L"
            #                 break
            #             elif nbr == vertex+1:
            #                 grfPath += "R"
            #                 break
            #             elif nbr == vertex+grf["grfProperties"]["width"]:
            #                 grfPath += "D"
            #                 break
            #             else:
            #                 grfPath += "."
            #                 break
            
            sortedTupsByRwdOverLen = sorted(shortestPaths[vertex], key=lambda x: x[2], reverse=True)
            maxTupsByRwdOverLen = [tup for tup in sortedTupsByRwdOverLen if tup[2] == sortedTupsByRwdOverLen[0][2]]
            movementIndices = set()
            for tup in maxTupsByRwdOverLen:
                for nbr in nbrs:
                    for tupInNbr in shortestPaths[nbr]:
                        if tupInNbr[0]+1 == tup[0] and tupInNbr[1] == tup[1] and tupInNbr[2] >= tup[2]:
                            movementIndices.add(nbr)
                            break
            for idx in sorted(list(movementIndices)):
                if idx == vertex-grf["grfProperties"]["width"]:
                    grfPath += "U"
                elif idx == vertex-1:
                    grfPath += "L"
                elif idx == vertex+1:
                    grfPath += "R"
                elif idx == vertex+grf["grfProperties"]["width"]:
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
    # args = "25 R13 B16 B17 B11 R3:5 R9:6 R5 B5 B12N B5N B8S"
    # args = "25 R17 B8 B13 B7 R15:5 R21:6 G1 R23 B18 B12N B8W B21E B4S"
    # args = "25 R13 B16 B17 B11 R3:5 R9:6 G0 R1 B20 B10S B16N"
    # args = "45 R:5 R10 R14:500 B42 B23 B3 B15 B40 B21 B2 B41 G0 R39 R3 B21W B21S B14S B1E B33N"
    # args = "6 2 B0S B1S G0 R4"
    # args = "1"
    # args = "25 R13 B16 B17 B11 R3:5 R9:6 R11 B9 B19S B1S B12N"
    # args = "25 R13 B16 B17 B11 R3:5 R9:6 R20 B4 B5S B16S B14W B9S"
    # args = "25 G0 R13 B16 B17 B11 R3:5 R9:6 R20 B4 B5S B16S B14W B9S"
    # args = "25 R17 B8 B13 B7 R15:5 R21:6 R12 B1 B7E B21N B5N"
    # args = "99 B97 B84 B83 B50 B3 B98 B63 B71 B57 B23 B63W B68E B26E B7S B14S B36W B84E B43W B73S B67W B6S B90N B4W B69N B4E R12:78 R58:26 R40:35 R77:7 R63:70 R24:14 R33:78 R94:36 R7:59 R15:22 R59:93 R25:63 R21:53 R8:12 R44:94 R43:99 R18:78 R66:17 R31:35 R34:15"
    # args = "25 r2 r22"
    if type(args) == str: argsLst = args.split(" ")
    else: argsLst = args
    grf = grfParse(argsLst)
    
    bfs = BFS(grf)
    print2D(bfs, grf["grfProperties"]["width"])

    return

if __name__ == "__main__": main()

#Dhruv Chandna Period 6 2025