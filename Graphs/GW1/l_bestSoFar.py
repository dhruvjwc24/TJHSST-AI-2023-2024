import sys; args = sys.argv[1:]

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

def getCardinalEdges(idx, width, height):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    pos = getPosFromIdx(idx, width)
    edges = set()
    for direction in directions:
        newPos = (pos[0]+direction[0], pos[1]+direction[1])
        if newPos[0] >= 0 and newPos[0] < height and newPos[1] >= 0 and newPos[1] < width:
            edges.add(getIdxFromPos(newPos, width))
    return edges

def getInitialGrfEdges(numVertices, width, height):
    adjacencyListOfVertices = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for vertex in range(numVertices):
        edges = getCardinalEdges(vertex, width, height)
        edgesWithEmptyRwd = {(edge, "") for edge in edges}
        adjacencyListOfVertices.append((edgesWithEmptyRwd, {}))
    return adjacencyListOfVertices

def blockEdges(graph, verticesInDirective):
    nonSliced = set(range(graph["grfProperties"]["numVertices"])) - set(verticesInDirective)
    combosOneWay = {(i, j) for i in nonSliced for j in verticesInDirective}
    combosOtherWay = {(j, i) for i in nonSliced for j in verticesInDirective}
    combos = combosOneWay | combosOtherWay
    for combo in combos:
        vertex1InEdgesOfVertex0 = False
        edgeTupToDiscard = None
        for edge in graph["edges"][combo[0]][0]:
            if edge[0] == combo[1]:
            # if the second vertex in the tuple is already in the edges of the first vertex, then skip
                vertex1InEdgesOfVertex0 = True
                edgeTupToDiscard = edge
                break

        if vertex1InEdgesOfVertex0: 
            graph["edges"][combo[0]][0].discard(edgeTupToDiscard)
        elif combo[1] in getCardinalEdges(combo[0], graph["grfProperties"]["width"], graph["grfProperties"]["height"]):
            graph["edges"][combo[0]][0].add((combo[1], ""))

def positify(vsclIdxs, numVertices):
    positifiedIdxs = []
    for idx in vsclIdxs:
        while idx < 0:
            idx += numVertices
        positifiedIdxs.append(idx)
    return positifiedIdxs

     
def getSliceIdxs(vscls, grfIdxs):
    verticesInDirective = []
    for vscl in vscls:
        if ":" not in vscl:
            vsclIdxs = [int(vscl)]
            vsclIdxs = positify(vsclIdxs, len(grfIdxs))
            verticesInDirective += vsclIdxs

        elif vscl.count(":") == 1:
            start, end = vscl.split(":")
            if start == "":
                start = 0
            if end == "":
                end = len(grfIdxs)
            start, end = int(start), int(end)
            vsclIdxs = grfIdxs[start:end]
            vsclIdxs = positify(vsclIdxs, len(grfIdxs))
            verticesInDirective += vsclIdxs
        else:
            start, end, skip = vscl.split(":")
            if start and end and skip:
                start, end, skip = int(start), int(end), int(skip)
                vsclIdxs = grfIdxs[start:end:skip]
                vsclIdxs = positify(vsclIdxs, len(grfIdxs))
                verticesInDirective += vsclIdxs
            elif start and end and not skip:
                start, end = int(start), int(end)
                vsclIdxs = grfIdxs[start:end]
                vsclIdxs = positify(vsclIdxs, len(grfIdxs))
                verticesInDirective += vsclIdxs
            elif start and not end and not skip:
                start = int(start)
                vsclIdxs = grfIdxs[start:]
                vsclIdxs = positify(vsclIdxs, len(grfIdxs))
                verticesInDirective += vsclIdxs
            elif not start and end and not skip:
                end = int(end)
                vsclIdxs = grfIdxs[:end]
                vsclIdxs = positify(vsclIdxs, len(grfIdxs))
                verticesInDirective += vsclIdxs
            elif not start and end and skip:
                end, skip = int(end), int(skip)
                vsclIdxs = grfIdxs[:end:skip]
                vsclIdxs = positify(vsclIdxs, len(grfIdxs))
                verticesInDirective += vsclIdxs
            elif start and not end and skip:
                start, skip = int(start), int(skip)
                vsclIdxs = grfIdxs[start::skip]
                vsclIdxs = positify(vsclIdxs, len(grfIdxs))
                verticesInDirective += vsclIdxs
            elif not start and not end and skip:
                skip = int(skip)
                vsclIdxs = grfIdxs[::skip]
                vsclIdxs = positify(vsclIdxs, len(grfIdxs))
                verticesInDirective += vsclIdxs
            else:
                vsclIdxs = grfIdxs
                vsclIdxs = positify(vsclIdxs, len(grfIdxs))
                verticesInDirective += vsclIdxs
    return verticesInDirective
    
def applyEDirectiveChangesToGrf(grf, newEdgesToChange, mngmnt, edgeRwd):
    if mngmnt == "!":
        for edge in newEdgesToChange:

            vertex1InEdgesOfVertex0 = False
            edgeTup = None
            for edgeInVertex0 in grf["edges"][edge[0]][0]:
                if edge[1] == edgeInVertex0[0]:
                    vertex1InEdgesOfVertex0 = True
                    edgeTup = edgeInVertex0
                    break

            if vertex1InEdgesOfVertex0:
                grf["edges"][edge[0]][0].discard(edgeTup)
    elif mngmnt == "+":
        for edge in newEdgesToChange:
            # if the second vertex in the tuple is already in the edges of the first vertex, then skip
            vertex1InEdgesOfVertex0 = False
            for edgeInVertex0 in grf["edges"][edge[0]][0]:
                if edge[1] == edgeInVertex0[0]:
                    vertex1InEdgesOfVertex0 = True
                    break
            if vertex1InEdgesOfVertex0:
                continue
            grf["edges"][edge[0]][0].add((edge[1], edgeRwd))
            # grf["edges"][edge[0]][1] = {"rwd": vertexRwd}
            # if edgeRwd != -1: grf["edges"][edge[0]] = (grf["edges"][edge[0]][0], {"rwd": edgeRwd})
    elif mngmnt == "*":
        for edge in newEdgesToChange:

            vertex1InEdgesOfVertex0 = False
            edgeTup = None
            for edgeInVertex0 in grf["edges"][edge[0]][0]:
                if edge[1] == edgeInVertex0[0]:
                    vertex1InEdgesOfVertex0 = True
                    edgeTup = edgeInVertex0
                    break

            if not vertex1InEdgesOfVertex0:
                grf["edges"][edge[0]][0].add((edge[1], edgeRwd))
            else:
                grf["edges"][edge[0]][0].discard(edgeTup)
                grf["edges"][edge[0]][0].add((edge[1], edgeRwd))
            # if edgeRwd != -1: grf["edges"][edge[0]] = (grf["edges"][edge[0]][0], {"rwd": edgeRwd})
    elif mngmnt == "~":
        for edge in newEdgesToChange:
            vertex1InEdgesOfVertex0 = False
            edgeTup = None
            for edgeInVertex0 in grf["edges"][edge[0]][0]:
                if edge[1] == edgeInVertex0[0]:
                    vertex1InEdgesOfVertex0 = True
                    edgeTup = edgeInVertex0 
                    break

            if not vertex1InEdgesOfVertex0:
                grf["edges"][edge[0]][0].add((edge[1], edgeRwd))
                # if edgeRwd != -1: grf["edges"][edge[0]] = (grf["edges"][edge[0]][0], {"rwd": edgeRwd})
                # grf["edges"][edge[0]][1] = {"rwd": vertexRwd}
            else:
                grf["edges"][edge[0]][0].discard(edgeTup)
    elif mngmnt == "@":
        for edge in newEdgesToChange:

            vertex1InEdgesOfVertex0 = False
            edgeTup = None
            for edgeInVertex0 in grf["edges"][edge[0]][0]:
                if edge[1] == edgeInVertex0[0]:
                    vertex1InEdgesOfVertex0 = True
                    edgeTup = edgeInVertex0 
                    break

            if vertex1InEdgesOfVertex0:
                grf["edges"][edge[0]][0].discard(edgeTup)
                grf["edges"][edge[0]][0].add((edge[1], edgeRwd))
                # grf["edges"][edge[0]][0] 
                # grf["edges"][edge[0]][1] = {"rwd": vertexRwd}
                # if edgeRwd != -1: grf["edges"][edge[0]] = (grf["edges"][edge[0]][0], {"rwd": edgeRwd})
    else:
        return

def grfParse(lstArgs):
    grf = {"edges": [], "grfProperties": ""}
    grfType, numVertices, width, height, rwd = "G", 0, 0, 0, 12
    cardinalDirsDict = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0), "": (0, 0)}
    # adjacencyListOfVertices = []
    for arg in lstArgs:
        if arg[0] == "G":
            startPosForSize = -1
            if not arg[1].isnumeric(): 
                grfType = arg[1]
                startPosForSize = 2
            else: startPosForSize = 1
            numVertices = ""
            for i in range(startPosForSize, len(arg)):
                if arg[i].isnumeric():
                    numVertices += arg[i]
                else:
                    break
            if not numVertices: numVertices = 0
            else: numVertices = int(numVertices)
            grfIdxs = [i for i in range(numVertices)]
            if "R" in arg: rwd = int(arg[arg.index("R")+1:])

            if grfType == "N":
                grf["grfProperties"] = {"grfType": grfType, "numVertices": numVertices, "rwd": rwd}
                continue
            
            width = ""
            if "W" in arg:
                for i in range(arg.index("W")+1, len(arg)):
                    if arg[i].isnumeric():
                        width += arg[i]
                    else:
                        break
                width = int(width)
                if width == 0:
                    grfType = "N"
                    grf["grfProperties"] = {"grfType": grfType, "numVertices": numVertices, "rwd": rwd, "width": width}
                    continue
                height = numVertices // width
            else:
                width, height = getDimensions(numVertices)
            edges = getInitialGrfEdges(numVertices, width, height)
            grf["grfProperties"] = {"grfType": grfType, "numVertices": numVertices, "width": width, "height": height, "rwd": rwd}
            grf["edges"] = edges
        elif arg[0] == "V":
            block = False
            terminal = False
            if "B" in arg:
                block = True
            if "T" in arg:
                terminal = True
            if "R" in arg: 
                vertexRwd = ""
                for i in range(arg.index("R")+1, len(arg)):
                    if arg[i].isnumeric():
                        vertexRwd += arg[i]
                    else:
                        break
                if not vertexRwd: vertexRwd = rwd
                else: vertexRwd = int(vertexRwd)
            else: vertexRwd = rwd
            vscls = ""
            for i in range(1, len(arg)):
                if arg[i].isalpha():
                    break
                vscls += arg[i]
            vscls = vscls.split(",")
            verticesInDirective = getSliceIdxs(vscls, grfIdxs)
            verticesInDirectiveFixed = positify(verticesInDirective, numVertices)
            # while verticesInDirective:
            #     vertex = verticesInDirective.pop()
            #     while vertex < 0:
            #         vertex += numVertices
            #     verticesInDirectiveFixed.add(vertex)
            if block: 
                blockEdges(grf, verticesInDirectiveFixed)
            if "R" in arg:
                for vertex in verticesInDirectiveFixed:
                    grf["edges"][vertex][1]["rwd"] = vertexRwd
        else: # i.e. E == arg[0]
            # NSEW E Directive
            terminal = False
            if "T" in arg:
                terminal = True
            edgeRwd = ""
            # edgeRwd = rwd
            if "R" in arg: 
                for i in range(arg.index("R")+1, len(arg)):
                    if arg[i].isnumeric():
                        edgeRwd += arg[i]
                    else:
                        break
                if not edgeRwd: edgeRwd = rwd
                else: edgeRwd = int(edgeRwd)
            mngmnt = "~"
            start = 1
            if arg[1] in "!+*~@": 
                mngmnt = arg[1]
                start = 2
            if "N" in arg or "E" in arg[start:] or "S" in arg or "W" in arg:
                # earliestIdx = -1
                # for cardinalDir in ["N", "E", "S", "W"]:
                #     findPos = arg.find(cardinalDir)
                #     if findPos != -1 and (findPos < earliestIdx or earliestIdx == -1):
                #         earliestIdx = findPos
                # vscls = arg[start:earliestIdx].split(",")
                vscls = ""
                for i in range(start, len(arg)):
                    # if arg[i].isnumeric() or arg[i] == "-" or arg[i] == ":":
                    #     vscls += arg[i]
                    if arg[i] in "NWSE":
                        start = i
                        break
                    vscls += arg[i]
                vscls = vscls.split(",")
                verticesInDirective = []
                for vscl in vscls:
                    if ":" not in vscl:
                        vsclIdxs = [int(vscl)]
                        vsclIdxs = positify(vsclIdxs, len(grfIdxs))
                        verticesInDirective += vsclIdxs
                    else:
                        vsclIdxs = getSliceIdxs([vscl], grfIdxs)
                        verticesInDirective += vsclIdxs
                dirs = ""
                for i in range(start, len(arg)):
                    if arg[i] in "=~":
                        start = i+1
                        directionality = arg[i]
                        break
                    dirs += arg[i]
                
                # verticesInDirective = getSliceIdxs(vscls, grfIdxs)
                # dirs = ""
                
                # for i in range(start, len(arg)):
                #     if arg[i] in "=~":
                #         directionality = arg[i]
                #         start = i+1
                #         break
                #     dirs += arg[i]
                # print(dirs, directionality)
                for vertex in verticesInDirective:
                    newEdgesToChange = set()
                    vertexRow, vertexCol = getPosFromIdx(vertex, grf["grfProperties"]["width"])
                    for cardinalDir in dirs:
                        wInc, hInc = cardinalDirsDict[cardinalDir]
                        newRow, newCol = vertexRow+hInc, vertexCol+wInc
                        if newRow >= 0 and newRow < grf["grfProperties"]["height"] and newCol >= 0 and newCol < grf["grfProperties"]["width"]:
                            edgeVertex = getIdxFromPos((newRow, newCol), grf["grfProperties"]["width"])
                            newEdgesToChange.add((vertex, edgeVertex))
                            if directionality == "=": newEdgesToChange.add((edgeVertex, vertex))
                    applyEDirectiveChangesToGrf(grf, newEdgesToChange, mngmnt, edgeRwd)     
            else:
                directionality = ""
                vscls1 = ""
                for i in range(start, len(arg)):
                    if arg[i] in "=~":
                        start = i+1
                        directionality = arg[i]
                        break
                    vscls1 += arg[i]
                vscls1 = vscls1.split(",")
                verticesInDirective1 = getSliceIdxs(vscls1, grfIdxs)

                vscls2 = ""
                for i in range(start, len(arg)):
                    if arg[i].isalpha():
                        start = i+1
                        break
                    vscls2 += arg[i]
                vscls2 = vscls2.split(",")
                verticesInDirective2 = getSliceIdxs(vscls2, grfIdxs)
                newEdgesToChange = set(zip(verticesInDirective1, verticesInDirective2))
                if directionality == "=":
                    newEdgesToChange |= (set(zip(verticesInDirective2, verticesInDirective1)))
                applyEDirectiveChangesToGrf(grf, newEdgesToChange, mngmnt, edgeRwd)     
                # print(newEdgesToChange)
                # ZIP E Directive
                
    return grf
    # return graphType, numNodes, w, h, reward
def grfSize(graph): # COMPLETE
    return graph["grfProperties"]["numVertices"]
def grfNbrs(graph, v): # COMPLETE
    if graph["grfProperties"]["grfType"] == "N": return set()
    edges = []
    for edge in graph["edges"][v][0]:
        edges.append(edge[0])
    return edges
def grfGProps(graph): # COMPLETE
    gPropsDict = {}
    for prop in graph["grfProperties"]:
        if prop == "rwd" or prop == "width":
            gPropsDict[prop] = graph["grfProperties"][prop]
    return gPropsDict
def grfVProps(graph, v): # COMPLETE
    if v < len(graph["edges"]): return graph["edges"][v][1]
    return {}
def grfEProps(graph, v, u): # INCOMPLETE
    vertex1InEdgesOfVertex0 = False
    edgeTup = None
    for edge in graph["edges"][v][0]:
        if edge[0] == u and edge[1] != "":
        # if the second vertex in the tuple is already in the edges of the first vertex, then skip
            vertex1InEdgesOfVertex0 = True
            edgeTup = edge
            break
    if vertex1InEdgesOfVertex0: return {"rwd": edgeTup[1]}
    return {}
def grfStrEdges(graph): # COMPLETE
    dirSymbols = {"NW": "J", "N": "N", "NWE": "^", "NE": "L", "NWS": "<", "W": "W", "NWES": "+", "E": "E", "NES": ">", "WS": "7", "WES": "v", "S": "S", "ES": "r", "WE": "-", "NS": "|", "": "."}
    dirPath = ""
    for vertex in range(len(graph["edges"])):
        edgesDirs = ""
        cardinalEdges = getCardinalEdges(vertex, graph["grfProperties"]["width"], graph["grfProperties"]["height"])
        edges = []
        for edge in graph["edges"][vertex][0]:
            if edge[0] in cardinalEdges:
                edges.append(edge)

        # edges = graph["edges"][vertex][0] & cardinalEdges
        sortedEdges = sorted(edges)
        for edge in sortedEdges:
            if edge[0] == vertex-graph["grfProperties"]["width"]:
                edgesDirs += "N"
            elif edge[0] == vertex-1:
                edgesDirs += "W"
            elif edge[0] == vertex+1:
                edgesDirs += "E"
            elif edge[0] == vertex+graph["grfProperties"]["width"]:
                edgesDirs += "S"
            else:
                continue
        dirPath += dirSymbols[edgesDirs]
    jumpedEdges = []
    for vertexIdx in range(len(graph["edges"])):
        cardinalEdges = getCardinalEdges(vertexIdx, graph["grfProperties"]["width"], graph["grfProperties"]["height"])
        for edge in graph["edges"][vertexIdx][0]:
            if edge[0] not in cardinalEdges:
                jumpedEdges.append((vertexIdx, edge[0]))
    if len(jumpedEdges) > 0:
        stringified = "Jumps: "
        stringified += ",".join([str(jump[0]) for jump in jumpedEdges]) + "~" + ",".join([str(jump[1]) for jump in jumpedEdges])
        return dirPath + "\n" + stringified
    return dirPath
def grfStrProps(graph): # INCOMPLETE
    
    vProps = []
    for vertex in range(len(graph["edges"])):
        if graph["edges"][vertex][1]:
            vProps.append(str(vertex) + ":rwd:" + str(graph["edges"][vertex][1]["rwd"]))
    vPropsStr = "\n".join(vProps)
    
    eProps = []
    for vertex in range(len(graph["edges"])):
        for edge in graph["edges"][vertex][0]:
            if edge[1]:
                eProps.append(f"({vertex}, {edge[0]}):rwd:{edge[1]}")
    ePropsStr = "\n".join(eProps)

    gPropsDict = {}
    for prop in graph["grfProperties"]:
        if prop == "rwd" or prop == "width":
            gPropsDict[prop] = graph["grfProperties"][prop]
    gPropsStr = str(gPropsDict)
    return vPropsStr + "\n" + ePropsStr + "\n" + gPropsStr

def main():
    # args = "GG12 V0::2,6:,1B"
    # args = "GN19"
    # args = "GG50W10 V:-40:3"
    # args = "G24W8 V::-8B"
    # args = "GG25 V-16R5"
    # args = "GG12W12 V1B"
    # args = "GG16W8 E~12,5=13,6"
    # args = "GG30 E+7,20~18,13R V4BR6"
    # args = "GG32 E~19,8,14,27=25,19,10,18R E*26E~R1 E+19N=R V17B E~25,24=12,2R4 E@17,31~31,11R14 V29R12B E@23~27R5 E~11~24R E@15~4R"
    # args = "GG55W11 V23R5"
    if type(args) == str: argsLst = args.split(" ")
    else: argsLst = args
    grf = grfParse(argsLst)
    # print(grfSize(grf))
    # print(grfGProps(grf))
    # print(grfVProps(grf, 8))
    # print(grfEProps(grf, 26, 27))
    # print(grfNbrs(grf, 3))

    if grf["grfProperties"]["grfType"] == "N":
        print(grfStrProps(grf))
        return

    edgesAndJump = grfStrEdges(grf)
    if "Jumps" in edgesAndJump:
        edges, jumps = edgesAndJump.split("\n")
        print2D(edges, grf["grfProperties"]["width"])
        print()
        print(jumps)
    else:
        print2D(edgesAndJump, grf["grfProperties"]["width"])

    print(grfStrProps(grf))
    # return

if __name__ == "__main__": main()

#Dhruv Chandna Period 6 2025