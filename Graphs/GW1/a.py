import sys; args = sys.argv[1:]

def getDimensions(numNodes):
    numNodes
    width = int(numNodes**0.5)
    while numNodes % width != 0:
        width+=1
    return (max(dims:=(width, numNodes//width)), min(dims))

def grfParse(lstArgs):
    grf = {"edges": "", "vertexProperties": ""}
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
                grf["vertexProperties"] = {"grfType": grfType, "numVertices": numVertices, "rwd": rwd}
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
                    grf["vertexProperties"] = {"grfType": grfType, "numVertices": numVertices, "rwd": rwd, "width": width}
                    continue
                height = numVertices // width
            else:
                width, height = getDimensions(numVertices)
            grf["vertexProperties"] = {"grfType": grfType, "numVertices": numVertices, "width": width, "height": height, "rwd": rwd}
        elif arg[0] == "V":
            verticesInDirective = set()
            # grfIdxs = [i for i in range(numVertices)]
            vscls = arg[1:arg.find("[")].split(",")
            for vscl in vscls:
                if ":" not in vscl:
                    vsclIdxs = {int(vscl)}
                    verticesInDirective |= vsclIdxs
                    # verticiesInDirective.append([int(vscl)])
                    continue
                if vscl.count(":") == 1:
                    start, end = vscl.split(":")
                    start, end = int(start), int(end)
                    vsclIdxs = {i for i in range(start, end)}
                    verticesInDirective |= vsclIdxs
                    # verticesInDirective.append(grfIdxs[start:end])
                else:
                    start, end, skip = vscl.split(":")
                    if end == "": 
                        end = numVertices
                    start, end, skip = int(start), int(end), int(skip)
                    vsclIdxs = {i for i in range(start, end, skip)}
                    verticesInDirective |= vsclIdxs
                    # verticesInDirective.append(grfIdxs[start:end:skip])

    return grf
    # return graphType, numNodes, w, h, reward
def grfSize(graph): # COMPLETE
    return graph["vertexProperties"]["numVertices"]
def grfNbrs(graph, v): # COMPLETE
    return graph[v]
def grfGProps(graph): # COMPLETE
    gPropsDict = {}
    for prop in graph["vertexProperties"]:
        if prop == "rwd" or prop == "width":
            gPropsDict[prop] = graph["vertexProperties"][prop]
    return gPropsDict
def grfVProps(graph, v): # INCOMPLETE
    return {}
def grfEProps(graph, v, u): # INCOMPLETE
    return {}
def grfStrEdges(graph): # INCOMPLETE
    return
def grfStrProps(graph): # INCOMPLETE
    gPropsDict = {}
    for prop in graph["vertexProperties"]:
        if prop == "rwd" or prop == "width":
            gPropsDict[prop] = graph["vertexProperties"][prop]
    return str(gPropsDict)

def main():
    # args = "GG12 V0::2,6:,1B"
    # args = "GG12 0::2,6:,1B"
    # args = "GG9W3"
    grf = grfParse(args.split(" "))
    print(grfSize(grf))
    print(grfGProps(grf))
    print(grfStrProps(grf))
    return

if __name__ == "__main__": main()

#Dhruv Chandna Period 6 2025