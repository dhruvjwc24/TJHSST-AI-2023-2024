import sys; args = sys.argv[1:]
BLOCKCHAR = "#"
OPENCHAR = "-"
INITIALBOARD = ""
ITERS = []
VISITED = set()
CURRENTITER = set()
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LETTERPOS = {}
CHOICES_CACHE = {}

# def convert2DStateTo1D(state, h, w):

def print2DState(state, h, w):
    for i in range(h):
        print("".join(state[i*w:(i+1)*w]))

def parseDims(dimStr):
    releventText = "".join([myChar*(myChar.isdigit() or myChar == 'x') for myChar in dimStr])
    return int((d:=releventText.split('x'))[0]), int(d[1])

def getTextFromBlock(block):
    text = ""
    i = len(block)-1
    while i >= 0:
        if not block[i].isdigit():
            text = block[i] + text
            i -= 1
        else:
            break
    if not text: text = BLOCKCHAR
    return text

def getPosFromIdx(idx, h, w):
    return idx//w, idx%w

def getIdxFromPos(pos, w):
    return pos[0]*w+pos[1]

def placeBlocks(h, w, state, blocks, numBlockingSquares):
    global LETTERPOS
    center = (h//2, w//2)
    stateArr = list(state)
    if (h*w)%2==1 and numBlockingSquares%2==1: stateArr[getIdxFromPos(center, w)] = BLOCKCHAR
    for block in blocks:
        orientation, bh, bw, text = block
        rd, cd = 0, 0
        if orientation == "h": cd = 1
        else: rd = 1
        rCurr, cCurr = bh, bw
        for myChar in text:
            idx = getIdxFromPos((rCurr, cCurr), w)
            stateArr[idx] = myChar
            LETTERPOS[idx] = myChar
            if myChar == BLOCKCHAR: 
                stateArr[-idx-1] = BLOCKCHAR
                LETTERPOS[-idx-1+w*h] = myChar
            rCurr += rd
            cCurr += cd
    return "".join(stateArr)

def sqrtCase(h, w, numBlockingSquares, state):
    boxSize = int((h*w-numBlockingSquares)**0.5)
    wMargin = int((w-boxSize)/2)
    hMargin = int((h-boxSize)/2)
    wIndices = [idx for idx in range(w)][wMargin:w-wMargin]
    hIndices = [idx for idx in range(h)][hMargin:h-hMargin]
    stateArr = list(state)
    for idx, ch in enumerate(stateArr):
        if not(idx%w in wIndices and idx//w in hIndices):
            stateArr[idx] = BLOCKCHAR
    return "".join(stateArr)

def isValidState(h, w, state):
    global VISITED, ITERS, LETTERPOS
    for idx in LETTERPOS:
        if state[idx] != LETTERPOS[idx]: return False
    filled = fill(state, getPosFromIdx(state.find(OPENCHAR), h, w), h, w)
    VISITED = set()
    ITERS = []

    if OPENCHAR in filled: return False
    for row in range(h):
        oneRow = state[row*w:(row+1)*w]
        rowDivided = oneRow.split(BLOCKCHAR)
        lens = [0 < len(group) < 3 for group in rowDivided]
        if any(lens): return False
    for col in range(w):
        oneCol = state[col::w]
        colDivided = oneCol.split(BLOCKCHAR)
        lens = [0 < len(group) < 3 for group in colDivided]
        if any(lens): return False
    return True

def fixBoard(h, w, state, numBlockingSquares):
    global CURRENTITER, VISITED, ITERS
    # if state != INITIALBOARD: return state
    listState = list(state)
    for row in range(h):
        currC = 0
        idxs = []
        while currC < w:
            if listState[(idx:=getIdxFromPos((row, currC), w))] != BLOCKCHAR:
                idxs.append(idx)
            else:
                if len(idxs) < 3:
                    for pos in idxs:
                        if listState[pos] == OPENCHAR and listState[-pos-1] == OPENCHAR: 
                            listState[pos] = BLOCKCHAR
                            listState[-pos-1] = BLOCKCHAR
                idxs = []
            currC += 1
    for col in range(w):
        currR = 0
        idxs = []
        while currR < h:
            if listState[(idx:=getIdxFromPos((currR, col), w))] != BLOCKCHAR:
                idxs.append(idx)
            else:
                if len(idxs) < 3:
                    for pos in idxs:
                        if listState[pos] == OPENCHAR and listState[-pos-1] == OPENCHAR: 
                            listState[pos] = BLOCKCHAR
                            listState[-pos-1] = BLOCKCHAR
                idxs = []
            currR += 1

    for idx in range(len(listState)):
        if (ch:=listState[idx]) == OPENCHAR:
            if idx in VISITED or -idx-1+w*h in VISITED: continue
            CURRENTITER = set()
            filled = fill("".join(listState), getPosFromIdx(idx, h, w), h, w, fromFix=True, ch=BLOCKCHAR)
            ITERS.append(CURRENTITER)
    sortedIters = sorted(ITERS, key=lambda x: len(x))[:-1]
    for mySet in sortedIters:
        while mySet:
            listState[mySet.pop()] = BLOCKCHAR
    VISITED = set()
    ITERS = []
    return "".join(listState)

def isFinalState(state, numBlockingSquares): return state.count(BLOCKCHAR) == numBlockingSquares

def countLetters(state):
    global LETTERS
    return sum([state.count(letter) for letter in LETTERS])

def fill(state, pos, h, w, ch="*", fromFix=False):
    global VISITED, CURRENTITER, INITIALBOARD

    listState = list(state)
    r, c = pos
    idx = getIdxFromPos(pos, w)
    if not(0 <= r < h and 0 <= c < w): return state
    if state[idx] != BLOCKCHAR and state[idx] != ch:
        listState[idx] = ch
        if ch == BLOCKCHAR: 
            listState[-idx-1] = ch
            if fromFix: 
                CURRENTITER.add(idx)
                CURRENTITER.add(-idx-1+h*w)
                VISITED.add(idx)
                VISITED.add(-idx-1+h*w)
        else:
            CURRENTITER.add(idx)
            VISITED.add(idx)

        state = "".join(listState)
        state = fill(state, (r+1, c), h, w, ch, fromFix)
        state = fill(state, (r-1, c), h, w, ch, fromFix)
        state = fill(state, (r, c+1), h, w, ch, fromFix)
        state = fill(state, (r, c-1), h, w, ch, fromFix)
    return state

def getStructure(h, w, numBlockingSquares, blocks):
    global INITIALBOARD
    startingState = OPENCHAR*h*w
    startingStateWithBlocks = placeBlocks(h, w, startingState, blocks, numBlockingSquares)
    if numBlockingSquares == 0: return startingStateWithBlocks
    if numBlockingSquares == h*w: return startingStateWithBlocks.replace(OPENCHAR, BLOCKCHAR)
    state = fixBoard(h, w, startingStateWithBlocks, numBlockingSquares)
    # if h*w-countLetters(state) == numBlockingSquares: return state.replace(OPENCHAR, BLOCKCHAR)
    # if int((s:=(w*h-numBlockingSquares)**0.5)) == s: return sqrtCase(h, w, numBlockingSquares, startingStateWithBlocks)
    INITIALBOARD = state
    # print2DState(state, h, w); print()
    # filled = fill(state, getPosFromIdx(state.find(OPENCHAR), h, w), h, w)
    # print2DState(filled, h, w); print()
    return getStructureHelper(h, w, numBlockingSquares, state)

def getStructureHelper(h, w, numBlockingSquares, state):
    if state.count(BLOCKCHAR) > numBlockingSquares: return ""
    if not isValidState(h, w, state): return ""
    if isFinalState(state, numBlockingSquares): return state
    # state = fixBoard(h, w, state, numBlockingSquares)
    # filledSet = fill(state, getPosFromIdx(state.find(OPENCHAR), h, w), h, w)
    # if OPENCHAR in filledSet and state != INITIALBOARD: return ""
    #Should return set
    # areaFill(state, state.find(OPENCHAR))
    # Put Area Fill Stuff Here
    for idx, ch in enumerate(state):   
        if ch == OPENCHAR and state[-idx-1] == OPENCHAR:
            newStartingState = list(state)
            newStartingState[idx] = BLOCKCHAR
            newStartingState[-idx-1] = BLOCKCHAR
            newStartingStateFixed = fixBoard(h, w, "".join(newStartingState), numBlockingSquares)
            if not isValidState(h, w, "".join(newStartingStateFixed)): continue
            if (result:=getStructureHelper(h, w, numBlockingSquares, newStartingStateFixed)): return result
    return ""

def filterWords(words, openLen, filters, wordsUsed=set()):
    valids = []
    for word in words:
        word = word.upper()
        if word in wordsUsed: continue
        if len(word) != openLen: continue
        wordLst = list(word)
        passes = []
        for idx, key in enumerate(list(filters.keys())):
            passes.append(wordLst[key] == filters[key])
            if wordLst[key] != filters[key]: break
        # if all(passes): return word
        if all(passes): valids.append(word)
        # if all([wordLst[idx] == filters[key] for idx, key in enumerate(list(filters.keys()))]): return word
    # return None
    return valids

def updateState(state, choice, wordToFit):
    if not wordToFit: return state
    stateLst = list(state)
    for relIdx, idx in enumerate(choice):
        if idx < 0: continue
        stateLst[idx] = wordToFit[relIdx]
    return "".join(stateLst)

def getChoices(h, w, state, combine=False):
    # get all horizontal opens
    horizOpens = []
    rows = [state[i*w:(i+1)*w] for i in range(h)]
    for rowNum, row in enumerate(rows):
        segments = row.split(BLOCKCHAR)
        idx = rowNum*w
        for segment in segments:
            # if not segment or OPENCHAR not in segment: idx+=1; continue
            if not segment: idx+=1; continue
            segIdxs = []
            for spaceNum, space in enumerate(list(segment)):
                if space == OPENCHAR: segIdxs.append(idx+spaceNum)
                elif (rowNum == 0 and space == 0): segIdxs.append(-h*w)
                else: segIdxs.append(-(idx+spaceNum))
            segIdxs = tuple(segIdxs)
            # segIdxs = tuple([idx+spaceNum if space == OPENCHAR else -h*w if idx == 0 else -(idx+spaceNum) for spaceNum, space in enumerate(list(segment))])
            # horizOpens.add(segIdxs)
            horizOpens.append(segIdxs)
            idx+=len(segment)+1
        # idx-=1
    # get all vertical opens
    vertOpens = []
    cols = [state[i::w] for i in range(w)]
    for colNum, col in enumerate(cols):
        segments = col.split(BLOCKCHAR)
        idx = colNum
        for segment in segments:
            # if not segment or OPENCHAR not in segment: idx+=w; continue
            if not segment: idx+=w; continue
            segIdxs = []
            for spaceNum, space in enumerate(list(segment)):
                if space == OPENCHAR: segIdxs.append(idx+w*spaceNum)
                elif (rowNum == 0 and space == 0): segIdxs.append(-h*w)
                else: segIdxs.append(-(idx+w*spaceNum))
            segIdxs = tuple(segIdxs)
            # segIdxs = tuple([idx+w*spaceNum if space == OPENCHAR else -h*w if idx == 0 else -(idx+w*spaceNum) for spaceNum, space in enumerate(list(segment))])
            # horizOpens.add(segIdxs)
            vertOpens.append(segIdxs)
            idx+=len(segment)*w+w
    #     idx-=w
        idx%=w*h

    if combine: return horizOpens+vertOpens
    return horizOpens, vertOpens

def getAllValidChoices(h, w, state, words, openSegments, sort=False):
    validsDict = {}
    for choice in openSegments:
        filters = {}
        openLen = len(choice)
        for relPlace, idx in enumerate(choice):
            if idx < 0:
                if idx == -h*w:
                    filters[0] = state[0]
                else:
                    filters[relPlace] = state[-1*idx]
        wordsToFit = filterWords(words, openLen, filters)
        validsDict[choice] = wordsToFit
        CHOICES_CACHE[choice] = wordsToFit
        # CHOICES_CACHE[choice] = wordsToFit[:2500]
    if sort: validsDict = dict(sorted(validsDict.items(), key=lambda item: len(item[1])))
    return validsDict

# def isFinalStateMain(state, 

def isValidStateMain(state, openSegments, words):
    for segment in openSegments:
        if all([state[idx].isalpha() for idx in segment]): 
            word = "".join([state[idx] for idx in segment])
            if word not in words: return False
    return True

def isFinalStateMain(openSegments, state):
    if OPENCHAR not in state and len(openSegments) == 0: return True

def makeGraph(validsDict, openSegments):
    # changed = False
    # count = 0
    # while changed or count == 0:
    graph = {}
    for segment in openSegments:
        graph[segment] = []
        for otherSegment in openSegments:
            if len(graph[segment]) >= len(segment): continue
            if segment == otherSegment: continue
            if any([idx in otherSegment for idx in segment]):
                graph[segment].append(otherSegment)
    print(graph)
    return graph

def findWords(graph, openSegments, words, h, w):
    count = 0
    change = False
    while change or count == 0:
        change = False
        for parent in graph:
            for child in graph[parent]:
                sharedIdx = (set(parent) & set(child)).pop()
                sharedIdxInParent = parent.index(sharedIdx)
                sharedIdxInChild = child.index(sharedIdx)
                # if sharedIdx == -h*w: sharedIdx = 0
                # if sharedIdx < 0: sharedIdx *= -1
                parentCharsAtIdx = {word[sharedIdxInParent]:False for word in CHOICES_CACHE[parent]}
                numChildWords = len(CHOICES_CACHE[child])
                currChildWordIdx = 0
                for idx in range(numChildWords):
                    childWord = CHOICES_CACHE[child][currChildWordIdx]
                    if childWord[sharedIdxInChild] not in parentCharsAtIdx: CHOICES_CACHE[child].remove(childWord); change = True
                    else: parentCharsAtIdx[childWord[sharedIdxInChild]] = True; currChildWordIdx+=1
                for ch in parentCharsAtIdx:
                    if parentCharsAtIdx[ch]: continue
                    numParentWords = len(CHOICES_CACHE[parent])
                    currParentWordIdx = 0
                    for idx in range(numParentWords):
                        parentWord = CHOICES_CACHE[parent][currParentWordIdx]
                        if parentWord[sharedIdxInParent] == ch: CHOICES_CACHE[parent].remove(parentWord); change = True
                        else: currParentWordIdx+=1
        count += 1
        print(count)
    print(CHOICES_CACHE, count)
        

# def getFinalSol(graph):


def getSolution(h, w, baseState, words):
    openSegments = getChoices(h, w, baseState, combine=True)
    if not isValidStateMain(baseState, openSegments, words): return "No Solution"
    if isFinalStateMain(openSegments, baseState): return baseState
    validsDict = getAllValidChoices(h, w, baseState, words, openSegments, sort=True)
    graph = makeGraph(validsDict, openSegments) 
    findWords(graph, openSegments, words, h, w)
    # finalSol = getFinalSol(graph)

    # validsDict = {'':''}
    # while validsDict:
    #     # valids dict is {(tuple of idx of open spots in a segment): [words that fit in that segment]}
    #     validsDict = getAllValidChoices(h, w, state, words, sort=True)

    # wordsUsed = set()
    # for choice in vertOpens:
    #     filters = {}
    #     openLen = len(choice)
    #     for relPlace, idx in enumerate(choice):
    #         if idx < 0:
    #             if idx == -h*w:
    #                 filters[0] = state[0]
    #             else:
    #                 filters[relPlace] = state[-1*idx]
    #     wordToFit = filterWords(words, openLen, filters, wordsUsed)
    #     wordsUsed.add(wordToFit)
    #     state = updateState(state, choice, wordToFit)
    # return state


def parseArgs(args):
    if not args: args = "3x5 0".split()
    # if not args: args = "3x5 0".split()
    # if not args: args = "5x4 2".split()
    # if not args: args = "3x3 0 H2x0STD".split()
    # if not args: args = "3x3 0 H1x2a".split()
    # if not args: args = "4x4 0 h0x1h".split()
    # if not args: args = "5x5 0 v1x3r V0x4racer".split()
    # if not args: args = "5x4 2 H3x1E H2x2R".split()
    # if not args: args = "6x6 10 v5x2S v0x1# v0x5 v1x1# h1x3G v4x2R".split()
    # if not args: args = "7x7 11 H3x4VOS V0x3FTD v0x1# H6x4# V3x3".split()
    # if not args: args = "8x9 14 H2x4E H1x1N v3x4A H7x4 V1x8C H6x1E H2x3R v7x1S V2x8A H3x6L H7x0TSP# v4x8# h4x7".split()
    # if not args: args = "13x9 19 H9x7 H10x3 h12x3# V3x2# h3x0".split()
    if not args: args = "15x15 45 h5x4 h5x5 V6x11A v4x2 V3x3 H5x6 V7x6# V6x8 h4x11 h5x12 h3x9# v3x10 H2x7 H7x5 v6x5 v6x7 H6x6#".split()
    # if not args: args = "20x20 70 v15x2 h4x2# V1x0A h1x5E".split() # FAILED
    # if not args: args = "4x4 0 h0x1h".split()
    # if not args: args = "6x6 10 v5x2S v0x1# v0x5 v1x1# h1x3G v4x2R".split()
    # if not args: args = "4x4 0".split()
    h,w,numBlockingSquares,blocks,file = 3, 3, 0, [], "dict3.txt"
    for arg in args:
        if arg.endswith('.txt'): file = arg
        elif 'x' in arg.lower() and 'v' not in arg.lower() and 'h' not in arg.lower(): h,w = (d:=parseDims(arg))[0], d[1]
        elif arg.isdigit(): numBlockingSquares = int(arg)
        elif 'v' in arg.lower() or 'h' in arg.lower(): 
            orientation = arg[0].lower()
            bh, bw = (d:=parseDims(arg[1:]))[0], d[1]
            text = getTextFromBlock(arg.upper())
            blocks.append((orientation, bh, bw, text))
    return h, w, numBlockingSquares, blocks, file

def main():
    global CHOICES_CACHE
    # words = [word.strip() for word in open(args[0])]
    h, w, numBlockingSquares, blocks, file = parseArgs(args)
    words = [word.strip() for word in open(file)]
    base = getStructure(h, w, numBlockingSquares, blocks)
    print2DState(base, h, w)
    # base = "------------"
    # h, w = 5, 5
    # base = "#-A-#-####B####-#########"
    # h, w = 5, 5
    # print("\n\n")
    
    sol = getSolution(h, w, base, words)
    # print2DState(sol, h, w)
    # print2DState(sol, h, w)

if __name__=='__main__': main()

#Dhruv Chandna Period 6 2025