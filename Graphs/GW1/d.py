import sys; args = sys.argv[1:]

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

def getInitialGrfEdges(numVertices, width, height):
    adjacencyListOfVertices = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for vertex in range(numVertices):
        edges = set()
        for direction in directions:
            pos = getPosFromIdx(vertex, width)
            newPos = (pos[0]+direction[0], pos[1]+direction[1])
            if newPos[0] >= 0 and newPos[0] < height and newPos[1] >= 0 and newPos[1] < width:
                edges.add(getIdxFromPos(newPos, width))
        adjacencyListOfVertices.append((edges, {}))
    return adjacencyListOfVertices

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
            # grfIdxs = [i for i in range(numVertices)]
            vscls = arg[1:arg.find("B")].split(",")
            for vscl in vscls:
                if ":" not in vscl:
                    vsclIdxs = {int(vscl)}
                    verticesInDirective |= vsclIdxs
                    # verticiesInDirective.append([int(vscl)])

                elif vscl.count(":") == 1:
                    start, end = vscl.split(":")
                    start, end = int(start), int(end)
                    vsclIdxs = {i for i in range(start, end)}
                    verticesInDirective |= vsclIdxs
                    # verticesInDirective.append(grfIdxs[start:end])
                else:
                    start, end, skip = vscl.split(":")
                    if start == "":
                        start = 0
                    if skip == "":
                        skip = 1
                    if end == "": 
                        end = numVertices
                    start, end, skip = int(start), int(end), int(skip)
                    vsclIdxs = {i for i in range(start, end, skip)}
                    verticesInDirective |= vsclIdxs

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
    return {"Hello": "Test"}
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
    # args = "GG13"
    # args = "GG9W9 V6BB"
    if type(args) == str: argsLst = args.split(" ")
    else: argsLst = args
    grf = grfParse(argsLst)
    # print(grfSize(grf))
    # print(grfGProps(grf))
    # print(grfNbrs(grf, 0))
    # print(grfStrEdges(grf))
    # return

if __name__ == "__main__": main()

#Dhruv Chandna Period 6 2025