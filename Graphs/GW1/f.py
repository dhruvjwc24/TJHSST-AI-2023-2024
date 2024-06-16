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
        adjacencyListOfVertices.append((edges, {}))
    return adjacencyListOfVertices

def blockEdges(graph, verticesInDirective):
    nonSliced = set(range(graph["grfProperties"]["numVertices"])) - verticesInDirective
    combosOneWay = {(i, j) for i in nonSliced for j in verticesInDirective}
    combosOtherWay = {(j, i) for i in nonSliced for j in verticesInDirective}
    combos = combosOneWay | combosOtherWay
    for combo in combos:
        if combo[1] in graph["edges"][combo[0]][0]: 
            graph["edges"][combo[0]][0].discard(combo[1])
        elif combo[1] in getCardinalEdges(combo[0], graph["grfProperties"]["width"], graph["grfProperties"]["height"]):
            graph["edges"][combo[0]][0].add(combo[1])
            


def grfParse(lstArgs):
    grf = {"edges": [], "grfProperties": ""}
    grfType, numVertices, width, height, rwd = "G", 0, 0, 0, 12
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
            verticesInDirective = set()
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

            grfIdxs = [i for i in range(numVertices)]
            vscls = ""
            for i in range(1, len(arg)):
                if arg[i].isalpha():
                    break
                vscls += arg[i]
            vscls = vscls.split(",")
            for vscl in vscls:
                if ":" not in vscl:
                    vsclIdxs = {int(vscl)}
                    verticesInDirective |= vsclIdxs
                    # verticiesInDirective.append([int(vscl)])

                elif vscl.count(":") == 1:
                    start, end = vscl.split(":")
                    if start == "":
                        start = 0
                    if end == "":
                        end = numVertices
                    start, end = int(start), int(end)
                    vsclIdxs = set(grfIdxs[start:end])
                    verticesInDirective |= vsclIdxs
                    # verticesInDirective.append(grfIdxs[start:end])
                else:
                    start, end, skip = vscl.split(":")
                    if skip == "":
                        skip = 1
                    if start == "":
                        if "-" in skip: start = numVertices-1
                        else: start = 0
                    if end == "": 
                        if "-" in skip: end = -1
                        else: end = numVertices
                    start, end, skip = int(start), int(end), int(skip)
                    vsclIdxs = set(grfIdxs[start:end:skip])
                    verticesInDirective |= vsclIdxs
            if block: 
                verticesInDirectiveFixed = set()
                while verticesInDirective:
                    vertex = verticesInDirective.pop()
                    while vertex < 0:
                        vertex += numVertices
                    verticesInDirectiveFixed.add(vertex)

                blockEdges(grf, verticesInDirectiveFixed)
            for vertex in verticesInDirective:
                grf["edges"][vertex][1]["block"] = block
                grf["edges"][vertex][1]["terminal"] = terminal
                grf["edges"][vertex][1]["rwd"] = vertexRwd
    return grf
    # return graphType, numNodes, w, h, reward
def grfSize(graph): # COMPLETE
    return graph["grfProperties"]["numVertices"]
def grfNbrs(graph, v): # COMPLETE
    if graph["grfProperties"]["grfType"] == "N": return set()
    return graph["edges"][v][0]
def grfGProps(graph): # COMPLETE
    gPropsDict = {}
    for prop in graph["grfProperties"]:
        if prop == "rwd" or prop == "width":
            gPropsDict[prop] = graph["grfProperties"][prop]
    return gPropsDict
def grfVProps(graph, v): # INCOMPLETE
    if v in graph["edges"]: return graph["edges"][v][1]
    return {}
def grfEProps(graph, v, u): # INCOMPLETE
    return {"Bye": "Test"}
def grfStrEdges(graph): # COMPLETE
    dirSymbols = {"NW": "J", "N": "N", "NWE": "^", "NE": "L", "NWS": "<", "W": "W", "NWES": "+", "E": "E", "NES": ">", "WS": "7", "WES": "v", "S": "S", "ES": "r", "WE": "-", "NS": "|", "": "."}
    dirPath = ""
    for vertex in range(len(graph["edges"])):
        edgesDirs = ""
        sortedEdges = sorted(graph["edges"][vertex][0])
        for edge in sortedEdges:
            if edge == vertex-graph["grfProperties"]["width"]:
                edgesDirs += "N"
            elif edge == vertex-1:
                edgesDirs += "W"
            elif edge == vertex+1:
                edgesDirs += "E"
            elif edge == vertex+graph["grfProperties"]["width"]:
                edgesDirs += "S"
            else:
                continue
        dirPath += dirSymbols[edgesDirs]
    return dirPath
def grfStrProps(graph): # INCOMPLETE
    gPropsDict = {}
    for prop in graph["grfProperties"]:
        if prop == "rwd" or prop == "width":
            gPropsDict[prop] = graph["grfProperties"][prop]
    return str(gPropsDict)

def main():
    # args = "GG12 V0::2,6:,1B"
    # args = "GN19"
    # args = "GG50W10 V:-40:3"
    # args = "G24W8 V::-8B"
    args = "GG12W12 V1B"
    if type(args) == str: argsLst = args.split(" ")
    else: argsLst = args
    grf = grfParse(argsLst)
    # print(grfSize(grf))
    # print(grfGProps(grf))
    print(grfVProps(grf, 1))

    if grf["grfProperties"]["grfType"] == "N":
        print(grfStrProps(grf))
        return

    edges = grfStrEdges(grf)
    print2D(edges, grf["grfProperties"]["width"])
    print(grfStrProps(grf))
    # return

if __name__ == "__main__": main()

#Dhruv Chandna Period 6 2025