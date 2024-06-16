import sys; args = sys.argv[1:]
import re
BLOCKCHAR = "#"
OPENCHAR = "-"
INITIALBOARD = ""
ITERS = []
VISITED = set()
CURRENTITER = set()
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LETTERPOS = {}

# def convert2DStateTo1D(state, h, w):

def print2DState(state, h, w, spaces=False):
    for i in range(h):
        print("".join(state[i*w:(i+1)*w]))
    if spaces: print()

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

def getSegments(h, w, state, sort=False):
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
                if space != BLOCKCHAR: segIdxs.append(idx+spaceNum)
                # if space == OPENCHAR: segIdxs.append(idx+spaceNum)
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
                if space != BLOCKCHAR: segIdxs.append(idx+w*spaceNum)
                # if space == OPENCHAR: segIdxs.append(idx+w*spaceNum)
                elif (rowNum == 0 and space == 0): segIdxs.append(-h*w)
                else: segIdxs.append(-(idx+w*spaceNum))
            segIdxs = tuple(segIdxs)
            # segIdxs = tuple([idx+w*spaceNum if space == OPENCHAR else -h*w if idx == 0 else -(idx+w*spaceNum) for spaceNum, space in enumerate(list(segment))])
            # horizOpens.add(segIdxs)
            vertOpens.append(segIdxs)
            idx+=len(segment)*w+w
    #     idx-=w
        idx%=w*h

    allSegments = horizOpens+vertOpens

    if sort: return sorted(allSegments, key=lambda x: len(x), reverse=True)
    return horizOpens, vertOpens

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

def filterWords(words, openLen, filters, wordsUsed):
    for word in words:
        word = word.upper()
        if word in wordsUsed: continue
        if len(word) != openLen: continue
        wordLst = list(word)
        passes = []
        for idx, key in enumerate(list(filters.keys())):
            passes.append(wordLst[key] == filters[key])
            if wordLst[key] != filters[key]: break
        if all(passes): return word
        # if all([wordLst[idx] == filters[key] for idx, key in enumerate(list(filters.keys()))]): return word
    return None
    # return [word for word in words if len(word) == openLen and all([word[i] == filters[i] for i in range(openLen)])]

def updateState(state, choice, wordToFit):
    if not wordToFit: return state
    stateLst = list(state)
    for relIdx, idx in enumerate(choice):
        if idx < 0: continue
        stateLst[idx] = wordToFit[relIdx]
    return "".join(stateLst)

def makeGraph(openSegments, pos=False):
    graph = {}
    for segment in openSegments:
        if pos: segment = tuple([abs(idx) for idx in segment])
        graph[segment] = []
        for otherSegment in openSegments:
            if len(graph[segment]) >= len(segment): continue
            if pos: otherSegment = tuple([abs(idx) for idx in otherSegment])
            if segment == otherSegment: continue
            if any([idx in otherSegment for idx in segment]):
                graph[segment].append(otherSegment)
    return graph

def getPatternAndFindWords(segment, wordsDict, state, exclude=set(), justVerify=False):
    pattern = ""
    for idx in segment:
        idxCh = state[idx]
        if idxCh == OPENCHAR: pattern += "."
        else: pattern += idxCh
    pattern = "^" + pattern + "$"
    keyCh = pattern[1] if pattern[1] != "." else "-"
    keyLen = str(len(segment))
    searchKey = keyCh + keyLen
    possibleWordsForSeg = set()
    for word in wordsDict[searchKey]:
        if word not in exclude and re.match(pattern, word): 
            possibleWordsForSeg.add(word)
            if justVerify: return True
    if justVerify and not possibleWordsForSeg: return False
    return possibleWordsForSeg

def getFinalSolution(h, w, state, wordsDict, openSegments, graph):
    wordsInBoard = set()
    # wordsInBoard.add("RACER")
    # wordsInBoard.add("AANDR")
    # openSegments.remove((0, 1, 2, 3, 4))
    # openSegments.remove((4, 9, 14, 19, 24))
    # for segment in openSegments:
    sol = getFinalSolutionHelper(h, w, state, wordsDict, openSegments, graph, numVisited=0, wordsInBoard=wordsInBoard)

def getFinalSolutionHelper(h, w, state, wordsDict, openSegments, graph, numVisited, wordsInBoard=set()):
    if numVisited >= len(openSegments): return state
    parentSeg = openSegments[numVisited]
    potWordsForParentSeg = getPatternAndFindWords(parentSeg, wordsDict, state, exclude=wordsInBoard, justVerify=False) 
    if not potWordsForParentSeg: return ""
    for potParentWord in potWordsForParentSeg:
        if potParentWord in wordsInBoard: continue
        potState = updateState(state, parentSeg, potParentWord)
        print2DState(potState, h, w, True)
        childSegs = graph[parentSeg]
        # sortedChildSegs = sorted(childSegs, key=lambda x: len(x), reverse=True)
        for childSeg in childSegs:
            wordsFoundInChildSeg = getPatternAndFindWords(childSeg, wordsDict, potState, exclude=wordsInBoard | {potParentWord}, justVerify=True)
            if not wordsFoundInChildSeg: break 
        if (result:=getFinalSolutionHelper(h, w, potState, wordsDict, openSegments, graph, numVisited+1, wordsInBoard | {potParentWord})): return result
    return ""

def getSolution(h, w, state, file):
    wordsDict = makeWordsDict(h, w, file)
    segments = getSegments(h, w, state, sort=True) 
    graph = makeGraph(segments)
    sol = getFinalSolution(h, w, state, wordsDict, segments, graph)
    return sol
    # print()


def parseArgs(args):
    if not args: args = "5x5 0 v1x3r V0x4racer h0x0aandr".split()
    h,w,numBlockingSquares,blocks,file = 3, 3, 0, [], "dict7.txt"
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

def makeWordsDict(h, w, file=None):
    if not file: file = args[0]
    fileContent = open(file, 'r').read().split()
    wordsDict = {}
    for word in fileContent:
        word = word.strip().upper()
        if len(word) < 3 or len(word) > max(h, w): continue
        specificKey = str(word[0]) + str(len(word))
        generalKey = "-" + str(len(word))
        if specificKey not in wordsDict: wordsDict[specificKey] = {word}
        else: wordsDict[specificKey].add(word)
        if generalKey not in wordsDict: wordsDict[generalKey] = {word}
        else: wordsDict[generalKey].add(word)
    return wordsDict


def main():
    # words = [word.strip() for word in open(args[0])]
    h, w, numBlockingSquares, blocks, file = parseArgs(args)
    # words = [word.strip() for word in open(file)]
    base = getStructure(h, w, numBlockingSquares, blocks)
    print2DState(base, h, w)
    # base = "#-A-#-####B####-#########"
    base = "------------"
    h, w = 3, 4
    # horizChoices, vertChoices = getChoices(h, w, base)
    sol = getSolution(h, w, base, file)
    print2DState(sol, h, w)

if __name__=='__main__': main()

#Dhruv Chandna Period 6 2025