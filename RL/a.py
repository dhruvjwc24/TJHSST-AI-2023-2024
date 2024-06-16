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
    cardinalDirsDict = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0), "": (0, 0)}
    numVertices = int(lstArgs[0])
    grf["grfProperties"]["numVertices"] = numVertices
    del lstArgs[0]
    if not(lstArgs[0].isnumeric()): width, height = getDimensions(numVertices)
    else: width = int(lstArgs[1]); height = numVertices // width; del lstArgs[0]
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
            nbrDirs = [cardinalDirsDict[dir] for dir in dirs]
            potNbrs = set()
            for nbrDir in nbrDirs:
                vertexRow, vertexCol = getPosFromIdx(vertex, width)
                newRow, newCol = vertexRow+nbrDir[1], vertexCol+nbrDir[0]
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
            vertexRwd = arg[1:]
            if not vertexRwd: vertexRwd = rwd
            else: vertexRwd = int(vertexRwd)
            rwd = vertexRwd
        # R#:#
        else:
            split = arg.split(":")
            vertex1, vertex2 = int(split[0][1:]), int(split[1])
            grf["grfValues"][vertex1][1]["rwd"] = grf["grfValues"][vertex2][1]["rwd"]
                
    return grf

def BFS(grf):
    dirSymbols = {"NW": "J", "N": "N", "NWE": "^", "NE": "L", "NWS": "<", "W": "W", "NWES": "+", "E": "E", "NES": ">", "WS": "7", "WES": "v", "S": "S", "ES": "r", "WE": "-", "NS": "|", "": ".", ".": "."}
    shortestPaths = ["" for i in range(grf["grfProperties"]["numVertices"])]
    rwdIdxs = [idx for idx in range(len(grf["edges"])) if grf["edges"][idx][1]]
    edgeRwdIdxs = []
    for vertex in range(len(grf["edges"])):
        for edge in grf["edges"][vertex][0]:
            if edge[1] != "":
                edgeRwdIdxs.append((vertex, edge[0]))
    if not rwdIdxs and not edgeRwdIdxs:
        return "." * grf["grfProperties"]["numVertices"], []
    edgesUsed = set()
    for vertex in range(len(shortestPaths)):
        for rwdIdx in rwdIdxs:
            if shortestPaths[vertex] == 0: continue
            path = shortestPathVertex(vertex, rwdIdx, grf)
            if shortestPaths[vertex] == "" and path: 
                shortestPaths[vertex] = len(path)-1
            elif path and len(path)-1 < shortestPaths[vertex]:
                shortestPaths[vertex] = len(path)-1
            else:
                continue
        for edge in edgeRwdIdxs:
            edgeUsed = ()
            path = shortestPathEdge(vertex, edge, grf)
            if shortestPaths[vertex] == "" and path: 
                shortestPaths[vertex] = len(path)-1
                edgeUsed = edge
            elif path and len(path)-1 <= shortestPaths[vertex]:
                shortestPaths[vertex] = len(path)-1
                edgeUsed = edge
            else:
                continue
            if vertex == 4 and edge == 17:
                print()
            edgesUsed.add(edgeUsed)
        if shortestPaths[vertex] == "":
            shortestPaths[vertex] = -1
    # for vertex in range(len(shortestPaths)):
    #     if grf["edges"][vertex][1]:
    #         shortestPaths[vertex] = 0
    grfPaths = ""
    jumpsUsed = []
    for vertex in range(len(shortestPaths)):
        if vertex in rwdIdxs:
            grfPaths += "*"
            continue
        grfPath = ""
        # cardinalEdges = getCardinalEdges(vertex, grf["grfProperties"]["width"], grf["grfProperties"]["height"])
        pathLength = shortestPaths[vertex]
        edges = sorted([edge[0] for edge in grf["edges"][vertex][0]])
        for edge in edges:
            if vertex == 4 and edge == 17:
                print()
            if shortestPaths[edge]+1 == pathLength or (vertex, edge) in edgesUsed:
                if edge == vertex-grf["grfProperties"]["width"]:
                    grfPath += "N"
                elif edge == vertex-1:
                    grfPath += "W"
                elif edge == vertex+1:
                    grfPath += "E"
                elif edge == vertex+grf["grfProperties"]["width"]:
                    grfPath += "S"
                else:
                    grfPath += "."
                    jumpsUsed.append(f"{vertex}>{edge}")
                    # break
        if "." in grfPath and len(grfPath) > 1:
            grfPath = grfPath.replace(".", "")
        grfPaths += dirSymbols[grfPath]

    return grfPaths, jumpsUsed


def shortestPathEdge(root, edgeGoal, grf):
    parseMe = [root]
    dctSeen = {root: ""}
    while parseMe:
        item = parseMe.pop(0)
        # if item == edgeGoal: 
        #     path = []
        #     while edgeGoal != "":
        #         path.append(edgeGoal)
        #         edgeGoal = dctSeen[edgeGoal]
        #     return list(reversed(path))
        for nbr in grf["edges"][item][0]:
            if (item, nbr[0]) == edgeGoal:
                # dctSeen[nbr[0]] = item
                edgeGoal = item
                path = []
                while edgeGoal != "":
                    path.append(edgeGoal)
                    edgeGoal = dctSeen[edgeGoal]
                path.insert(0, nbr[0])
                return list(reversed(path))
            # if nbr[1]:
            #     path = []
            #     while goal != "":
            #         path.append(goal)
            #         goal = dctSeen[goal]
            #     path.append(nbr[1])
            #     return list(reversed(path)) 
            if nbr[0] not in dctSeen:
                parseMe.append(nbr[0])
                dctSeen[nbr[0]] = item
    return []


def shortestPathVertex(root, goal, grf):
    parseMe = [root]
    dctSeen = {root: ""}
    while parseMe:
        item = parseMe.pop(0)
        if item == goal: 
            path = []
            while goal != "":
                path.append(goal)
                goal = dctSeen[goal]
            return list(reversed(path))
        for nbr in grf["edges"][item][0]:
            if nbr[0] not in dctSeen:
                parseMe.append(nbr[0])
                dctSeen[nbr[0]] = item
    return []

def main():
    args = "4 G0 R3 B3 B0S"
    if type(args) == str: argsLst = args.split(" ")
    else: argsLst = args
    grf = grfParse(argsLst)
    
    # bfs, jumpsUsed = BFS(grf)
    # print2D(bfs, grf["grfProperties"]["width"])

    return

if __name__ == "__main__": main()

#Dhruv Chandna Period 6 2025