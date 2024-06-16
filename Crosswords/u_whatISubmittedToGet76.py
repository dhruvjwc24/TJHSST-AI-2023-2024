import sys; args = sys.argv[1:]
import re
import time
BLOCKCHAR = "#"
OPENCHAR = "-"
INITIALBOARD = ""
ITERS = []
VISITED = set()
CURRENTITER = set()
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LETTERPOS = {}
FINALSTATE = ""
PARTIALSTATE = ""
wordsInBoard = set()
NUM_RECURSIONS = 0
WHY_OUT = ""

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

    # allSegments = horizOpens+vertOpens   
    allSegments = combine_alternately (horizOpens,vertOpens )          
    # if sort: return sorted(allSegments, key=lambda x: len(x), reverse=True)
    # Sort the segments by their length in descending order
    sortedSegments = sorted(allSegments, key=lambda x: len(x), reverse=True)

    return sortedSegments

def combine_alternately(horizOpens, vertOpens):
    combined = []

    horizOpens = sorted(horizOpens)
    vertOpens = sorted(vertOpens)

    # Iterate through the arrays, taking one element from each alternately
    for item1, item2 in zip(horizOpens, vertOpens):
        combined.append(item1)
        combined.append(item2)
    
    # If array1 is longer, append the remaining elements
    if len(horizOpens) > len(vertOpens):
        combined.extend(horizOpens[len(vertOpens):])
    
    # If array2 is longer, append the remaining elements
    elif len(vertOpens) > len(horizOpens):
        combined.extend(vertOpens[len(horizOpens):])
    
    return combined

def filter_segments(state, segments):
    """
    Remove segments from the list if all coordinates in the segment are filled with characters.
    
    :param board: String representation of the board.
    :param segments: List of tuples representing segment coordinates.
    :param row_length: Length of a row in the board.
    :return: Filtered list of segments.
    """
    word = ""
    filtered_segments = []    
    for segment in segments:
        word = ""
        all_filled = True  # Assume all are filled initially
        for pos in segment:
            word += state[pos]
            if state[pos] == '#' or state[pos] == '-':
                all_filled = False
        if not all_filled:
            filtered_segments.append(segment)
        else: wordsInBoard.add(word)           

    return filtered_segments
     
def rearrange_segments(state, segments, wordsDict):
    # Function to count filled positions and block count in a segment
    
    # return sorted(segments, key=lambda x: len(wordsDict[x]), reverse=True)
    
    def segment_info(segment):
        filled_count = sum(1 for i in segment if state[i] not in '#-')
        block_count = sum(1 for i in segment if state[i] == '#')
        return filled_count, -block_count, len(segment)  # Negative block count for sorting

    # Sort segments by filled count (descending), then by block count (ascending), and finally by segment length (descending)
    sorted_segments = sorted(segments, key=segment_info, reverse=True)
    return sorted_segments


def getStructure(h, w, numBlockingSquares, blocks):
    global INITIALBOARD
    startingState = OPENCHAR*h*w
    startingStateWithBlocks = placeBlocks(h, w, startingState, blocks, numBlockingSquares)
    if numBlockingSquares == 0: return startingStateWithBlocks
    if numBlockingSquares == h*w: return startingStateWithBlocks.replace(OPENCHAR, BLOCKCHAR)
    state = fixBoard(h, w, startingStateWithBlocks, numBlockingSquares)
    INITIALBOARD = state
    if h > 8 or w > 8: return getStructureHelperBigCases(h, w, numBlockingSquares, state)
    return getStructureHelper(h, w, numBlockingSquares, state)

def getChoices(h, w, state):
    choices = []
    idxChecked = set()
    for idx, ch in enumerate(state):
        if ch == OPENCHAR and state[-idx-1] == OPENCHAR:
            if idx in idxChecked: continue
            idxChecked.add(idx)
            idxChecked.add(-idx-1)
            choices.append((state, idx, h, w))
    return choices

def getStructureHelperBigCases(h, w, numBlockingSquares, state):
    if state.count(BLOCKCHAR) > numBlockingSquares: return ""
    if not isValidState(h, w, state): return ""
    if isFinalState(state, numBlockingSquares): return state

    for idx, ch in enumerate(state):
        if ch == OPENCHAR and state[-idx-1] == OPENCHAR:
            newStartingState = list(state)
            newStartingState[idx] = BLOCKCHAR
            newStartingState[-idx-1] = BLOCKCHAR
            newStartingStateFixed = fixBoard(h, w, "".join(newStartingState), numBlockingSquares)
            if not isValidState(h, w, "".join(newStartingStateFixed)): continue
            if (result:=getStructureHelperBigCases(h, w, numBlockingSquares, newStartingStateFixed)): return result
    return ""

def getStructureHelper(h, w, numBlockingSquares, state):
    if state.count(BLOCKCHAR) > numBlockingSquares: return ""
    if not isValidState(h, w, state): return ""
    if isFinalState(state, numBlockingSquares): return state

    choices = getChoices(h, w, state)
    sortedChoices = sorted(choices, key=lambda x: heuristic(*x), reverse=True)
    for choice in sortedChoices:   
        idx = choice[1]
        ch = state[idx]
        if ch == OPENCHAR and state[-idx-1] == OPENCHAR:
            newStartingState = list(state)
            newStartingState[idx] = BLOCKCHAR
            newStartingState[-idx-1] = BLOCKCHAR
            newStartingStateFixed = fixBoard(h, w, "".join(newStartingState), numBlockingSquares)
            if not isValidState(h, w, "".join(newStartingStateFixed)): continue
            if (result:=getStructureHelper(h, w, numBlockingSquares, newStartingStateFixed)): return result
    return ""

def heuristic(state, idx, h, w):
    horizs = [(0, 1), (0, -1)]
    verts = [(1, 0), (-1, 0)]
    startRow, startCol = getPosFromIdx(idx, h, w)

    vertScore = []
    for vert in verts:
        currRow, currCol = startRow+vert[0], startCol+vert[1]
        score = 0
        while 0 <= currRow < h and 0 <= currCol < w:
            if state[getIdxFromPos((currRow, currCol), w)] == BLOCKCHAR: break
            score += 1
            currRow += vert[0]
            currCol += vert[1]
        vertScore.append(score)
    horizScore = []
    for horiz in horizs:
        currRow, currCol = startRow+horiz[0], startCol+horiz[1]
        score = 0
        while 0 <= currRow < h and 0 <= currCol < w:
            if state[getIdxFromPos((currRow, currCol), w)] == BLOCKCHAR: break
            score += 1
            currRow += horiz[0]
            currCol += horiz[1]
        horizScore.append(score)
    return min(vertScore) + min(horizScore)

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

def getPatternAndFindWords1(segment, wordsDict, state, exclude=set(), justVerify=False):
    # pattern = wordsDict[segment]
    pattern = ""
    for idx in segment:
        idxCh = state[idx]
        if idxCh == OPENCHAR: pattern += "."
        else: pattern += idxCh
    if "." not in pattern and justVerify: return True
    pattern = "^" + pattern + "$"
    keyCh = pattern[1] if pattern[1] != "." else "-"
    keyLen = str(len(segment))
    searchKey = keyCh + keyLen
    possibleWordsForSeg = set()

    if searchKey in wordsDict:     
        for word in wordsDict[searchKey]:
            if word not in exclude and re.match(pattern, word): 
                possibleWordsForSeg.add(word)
                if justVerify: return True
        if justVerify and not possibleWordsForSeg: return False
    return possibleWordsForSeg

def getPatternAndFindWords(segment, wordsDict, state, exclude=set(), justVerify=False):
    pattern = getPattern(segment, state)
    if "." not in pattern and justVerify: return True
    possibleWordsForSeg = set()
    for word in wordsDict[segment]:
        if word not in exclude and re.match(pattern, word): 
            possibleWordsForSeg.add(word)
            if justVerify: return True
    if not possibleWordsForSeg and justVerify: return False
    return possibleWordsForSeg

def getPattern(segment, state):
    pattern = ""
    for idx in segment:
        idxCh = state[idx]
        if idxCh == OPENCHAR: pattern += "."
        else: pattern += idxCh
    pattern = "^" + pattern + "$"
    return pattern

def getFinalSolution(h, w, state, wordsDict, openSegments, graph, ts):
    sol = getFinalSolutionHelper(h, w, state, wordsDict, openSegments, graph, numVisited=0, wordsInBoard=wordsInBoard, segmentsVisited=set(), ts=ts)
    return sol

def getFinalSolutionHelper(h, w, state, wordsDict, openSegments, graph, numVisited, wordsInBoard=set(), segmentsVisited = set(), ts=0):
    global FINALSTATE, PARTIALSTATE, NUM_RECURSIONS 
    
    if time.time() - ts > 29.75:
        FINALSTATE = state
        return True

    # if NUM_RECURSIONS > 1000: 
    #     FINALSTATE = state
    #     return True

    if len(openSegments) == 0: 
        complete = True
        print("*** LINE355")
        print2DState(state, h, w, True)
        FINALSTATE = state
        return True #####SHOULD SEND STATE AT THE GLOBAL LEVEL 

    openSegments = rearrange_segments(state, openSegments, wordsDict)
    parentSeg = openSegments[0]

    potWordsForParentSeg = getPatternAndFindWords(parentSeg, wordsDict, state, exclude=wordsInBoard, justVerify=False) 

    if not potWordsForParentSeg: 
        partial = True
        print("*** LINE361")
        print2DState(state, h, w, True)
        return False  
    for potParentWord in potWordsForParentSeg:
        potState = updateState(state, parentSeg, potParentWord)
        print("*** LINE370")
        print2DState(potState, h, w, True)
        childSegs = graph[parentSeg]
        # sortedChildSegs = sorted(childSegs, key=lambda x: len(x), reverse=True)
        childrenWork = True
        for childSeg in childSegs:
            wordsFoundInChildSeg = getPatternAndFindWords(childSeg, wordsDict, potState, exclude=wordsInBoard | {potParentWord}, justVerify=True)
            if not wordsFoundInChildSeg: 
                childrenWork = False
                break ### GO GET NEXT WORD FROM PARENT -- OUTER LOOP
        if childrenWork:    ### IF THE PARENT WORD WORKED WITH CHILDREN AND RECUR
            segmentsVisited.add(parentSeg)        
            openSegments.remove(parentSeg)
            # wordsDictSetAtSegment = wordsDict[parentSeg]
            # wordsDict[parentSeg] = {potParentWord}    
            # NUM_RECURSIONS += 1
            result = getFinalSolutionHelper(h, w, potState, wordsDict, openSegments, graph, numVisited+1,  wordsInBoard | {potParentWord},segmentsVisited, ts)
            if result:
                return result   
            segmentsVisited.remove(parentSeg)
            openSegments.append(parentSeg)
            # wordsDict[parentSeg] = wordsDictSetAtSegment

    # print("*** LINE384")
    return False


def getSolution(h, w, state, file, ts):
    global FINALSTATE, PARTIALSTATE
    segments = getSegments(h, w, state, sort=True)
    wordsDict = makeWordsDict(h, w, segments, state, file)
    if h > 8 or w > 8:
        wordsUsed = set()
        horizSegments = [segment for segment in segments if segment[0]+1 == segment[1]]
        for segment in horizSegments:
            word = wordsDict[segment].pop()
            while word in wordsUsed: word = wordsDict[segment].pop()
            wordsUsed.add(word)
            # key = str(state[segment[0]]) + str(len(segment))
            state = updateState(state, segment, word)
        # print2DState(state, h, w, True)
        FINALSTATE = state
        return state
    graph = makeGraph(segments)
    # segments = filter_segments(state, segments)
    segments = rearrange_segments(state, segments, wordsDict)
    sol = getFinalSolution(h, w, state, wordsDict, segments, graph, ts)
    return sol
    # print()


def parseArgs(args):
    # if not args: args = "15x15 38 h2x9 h12x10 v13x9S v8x9A V8x4A".split()
    # if not args: args = "5x5 0 V0x4seems".split()
    # if not args: args = "15x15 45 V5x4# h12x5A V7x2 h6x4 h6x11 h4x9 V6x5# h2x11# H2x6 h3x10# h0x5 v3x2 H4x8 H4x3 h5x8#".split()
    # if not args: args = "25x19 91 v4x2 h4x16# H18x17E H21x11S h10x1T".split()
    # if not args: args = "25x19 91 v4x2 h4x16# H18x17E H21x11S h10x1T".split()
    # if not args: args = "6x8 2 H3x1E H2x2R".split()
    # if not args: args = "9x13 19 v1x0# H7x3# v8x12 H8x8# h0x9#".split()
    # if not args: args = "3x4 0".split()
    # if not args: args = "3x3 0".split()
    # if not args: args = "7x7 11 V0x2OLYMPIA H1x6# H1x1ALEXA".split()
    # if not args: args = "5x5 4 H2x0enter".split()
    # if not args: args = "5x5 0 v1x3r V0x4racer".split()
    # if not args: args = "5x5 0 v1x3r V0x4racer h0x0aandr".split()
    # if not args: args = "5x5 0 v1x3r V0x4racer h0x0aandr h1x0agora".split()
    # if not args: args = "7x7 11 V0x5ASSOC V6x6# v5x5# H3x4MOB h3x3#".split()
    # if not args: args = "7x7 0 V6x3#".split()
    # if not args: args = "5x5 0".split() # WORKED on dict3.txt
    # if not args: args = "3x5x 0".split() ##dict7P1.txt
    # if not args: args = "15x15 0".split() #THIS BREAKS
    # if not args: args = "6x8 2 H3x1E H2x2R".split()  ##dict7P1.txt
    # if not args: args = "8x9 14 H2x4E H1x1N v3x4A H7x4 V1x8C H6x1E H2x3R v7x1S V2x8A H3x6L H7x0TSP# v4x8# h4x7".split()
    # if not args: args = "3x3 0 H2x0STD".split()
    # if not args: args = "3x3 0 H1x2a".split()
    # if not args: args = "4x4 0".split()
    # if not args: args = "4x4 0 h0x1h".split()
    # if not args: args = "5x5 0 v1x3r V0x4racer".split() #USE THIS FOR DEBUGGING
    # if not args: args = "5x4 2 H3x1E H2x2R".split() ### CHECK
    # if not args: args = "6x6 10 v5x2S v0x1# v0x5 v1x1# h1x3G v4x2R".split()
    # if not args: args = "7x7 11 H3x4VOS V0x3FTD v0x1# H6x4# V3x3".split()
    # if not args: args = "8x9 14 H2x4E H1x1N v3x4A H7x4 V1x8C H6x1E H2x3R v7x1S V2x8A H3x6L H7x0TSP# v4x8# h4x7".split()
    # if not args: args = "13x9 19 H9x7 H10x3 h12x3# V3x2# h3x0".split()
    # if not args: args = "15x15 45 h5x4 h5x5 V6x11A v4x2 V3x3 H5x6 V7x6# V6x8 h4x11 h5x12 h3x9# v3x10 H2x7 H7x5 v6x5 v6x7 H6x6#".split()
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

def makeWordsDict(h, w, segments, baseState, file=None):
    fileContent = open(args[0]).read().splitlines()
    # fileContent = open(file).read().splitlines()

    patternsDict = {}
    wordsDict = {}
    for segment in segments:
        pattern = getPattern(segment, baseState)
        patternsDict[segment] = pattern
    for word in fileContent:
        word = word.strip().upper()
        if len(word) < 3 or len(word) > max(h, w): continue
        for segment in segments:
            if re.match(patternsDict[segment], word):
                if segment not in wordsDict: wordsDict[segment] = {word}
                else: wordsDict[segment].add(word)
    return wordsDict

def main():
    # words = [word.strip() for word in open(args[0])]
    ts = time.time()
    h, w, numBlockingSquares, blocks, file = parseArgs(args)
    # words = [word.strip() for word in open(file)]
    base = getStructure(h, w, numBlockingSquares, blocks)
    print2DState(base, h, w)
    # base = "#-A-#-####B####-#########"
    # h, w = 5, 5
    # horizChoices, vertChoices = getChoices(h, w, base)
    
    sol = getSolution(h, w, base, file, ts)
    print("***********IN MAIN")
    if sol: 
        print2DState(FINALSTATE, h, w)
    else:
        print2DState(PARTIALSTATE, h, w)
    
                

if __name__=='__main__': main()

#Dhruv Chandna Period 6 2025