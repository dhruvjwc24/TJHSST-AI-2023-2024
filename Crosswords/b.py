import sys; args = sys.argv[1:]
BLOCKCHAR = "#"
OPENCHAR = "-"

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
            stateArr[getIdxFromPos((rCurr, cCurr), w)] = myChar
            if myChar == BLOCKCHAR: stateArr[-getIdxFromPos((rCurr, cCurr), w)-1] = BLOCKCHAR
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
    # for idx, ch in enumerate(state):
    #     if ch == BLOCKCHAR:
    #         r, c = getPosFromIdx(idx, h, w)
    #         for inc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
    #             dirChars = []
    #             currR, currC = r, c
    #             dr, dc = inc
    #             while h > (currR:=currR+dr) and w > (currC:=currC+dc) and currR >= 0 and currC >= 0:
    #                 if state[getIdxFromPos((currR, currC), w)] != BLOCKCHAR:
    #                     dirChars.append(state[getIdxFromPos((currR, currC), w)])
    #                 else:
    #                     if 0 < len(dirChars) < 3: return False 
    #                     break
    #             if 0 < len(dirChars) < 3: return False
    # return True
    for row in range(h):
        row = state[row*w:(row+1)*w]
        rowDivided = row.split(BLOCKCHAR)
        lens = [0 < len(group) < 3 for group in rowDivided]
        if any(lens): return False
    for col in range(w):
        col = state[col::w]
        colDivided = col.split(BLOCKCHAR)
        lens = [0 < len(group) < 3 for group in colDivided]
        if any(lens): return False
    return True

def fixBoard(h, w, state, numBlockingSquares):
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
    return "".join(listState)

def isFinalState(state, numBlockingSquares): return state.count(BLOCKCHAR) == numBlockingSquares

# def areaFill(state, pos):


def getStructure(h, w, numBlockingSquares, blocks):
    startingState = OPENCHAR*h*w
    startingStateWithBlocks = placeBlocks(h, w, startingState, blocks, numBlockingSquares)
    # updatedNumBlockingSquares = numBlockingSquares - getBlockingSquareCount(startingStateWithBlocks)
    # return startingStateWithBlocks.replace(INDETERMINED, OPENCHAR)
    # if numBlockingSquares == 0: return startingStateWithBlocks.replace(INDETERMINED, OPENCHAR)
    if numBlockingSquares == 0: return startingStateWithBlocks
    if numBlockingSquares == h*w: return startingStateWithBlocks.replace(OPENCHAR, BLOCKCHAR)
    if int((s:=(w*h-numBlockingSquares)**0.5)) == s: return sqrtCase(h, w, numBlockingSquares, startingStateWithBlocks)
    state = fixBoard(h, w, startingStateWithBlocks, numBlockingSquares)
    return getStructureHelper(h, w, numBlockingSquares, state)

def getStructureHelper(h, w, numBlockingSquares, state):
    # center = (h//2, w//2)
    # print2DState(state, h, w)
    # print("\n"*3)
    if state.count(BLOCKCHAR) > numBlockingSquares: return ""
    if not isValidState(h, w, state): return ""
    if isFinalState(state, numBlockingSquares): return state
    state = fixBoard(h, w, state, numBlockingSquares)
    # areaFill(state, state.find(OPENCHAR))
    # Put Area Fill Stuff Here
    for idx, ch in enumerate(state):   
        # if idx < pos: continue 
        if ch == OPENCHAR and state[-idx-1] == OPENCHAR:
            newStartingState = list(state)
            newStartingState[idx] = BLOCKCHAR
            newStartingState[-idx-1] = BLOCKCHAR
            newStartingStateFixed = fixBoard(h, w, "".join(newStartingState), numBlockingSquares)
            # newStartingState = state[:idx] + BLOCKCHAR + state[idx+1:]
            if (result:=getStructureHelper(h, w, numBlockingSquares, newStartingStateFixed)): return result
    return ""


def parseArgs(args):
    # if not args: args = "13x13 25 H6x4no#on v5x5nor v0x0ankles h0x4Trot H0x9fall V0x12limp".split()
    # if not args: args = "10x10 86".split()
    # if not args: args = "11x9 16 V0x1Mus".split()
    # if not args: args = "15x15 39 H0x0Mute V0x0mule V10x13Alias H7x5# V3x4# H6x7# V11x3#".split()
    # if not args: args = "9x11 16 V0x1Mrs".split()
    # if not args: args = "13x13 25 H6x4no#on v5x5rot v0x0pigeon h0x4Trot H0x9Calf V0x12foot".split()
    h,w,numBlockingSquares,blocks,file = 3, 3, 0, [], ""
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
    # if not args: args = "11x13 27 wordList.txt H0x0begin V8x12end".split()
    h, w, numBlockingSquares, blocks, file = parseArgs(args)
    sol = getStructure(h, w, numBlockingSquares, blocks)
    # print(sol)
    print2DState(sol, h, w)
    # print(isValidState(h, w, "MUTE########---U-###------#---L---#------#---E---#------#----------------------------------------#------------#####------------#-----------------------------------I----#------#--N----#------#--L----#------###O----########--G-"))

if __name__=='__main__': main()

#Dhruv Chandna Period 6 2025