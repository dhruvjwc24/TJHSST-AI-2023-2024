import sys; args = sys.argv[1:]
import time

def updateStats(funcName):
    if funcName in STATS_COUNTER: STATS_COUNTER[funcName] += 1
    else : STATS_COUNTER[funcName] = 1

def isSolved(state):  
    for row in state:
        if "." in row: return False
    return True

def updateState(height, width, pos, state):
    if (c:=pos[1])+width<=blockDims[1] and (r:=pos[0])+height<=blockDims[0] and state[r*blockDims[1]+c: r*blockDims[1]+c+width] == "." * width:
        for row in range(r, r + height):
            state = state[:(idx:=row*blockDims[1]+pos[1])] + "X" * width + state[idx+width:]
        return state
    return None

# def updateState(state, block, pos):
#     r, c = pos // len(state[0]), pos % len(state[0])
#     for row in range(r, r + block[0]):
#     # for row in range(r, r + block[0]):
#     #     for col in range(c, c + block[1]):
#     #         if row >= len(state) or col >= len(state[0]): return ""
#     #         if state[row][col] == "X": return ""
#     #         state[row][col] = "X"
#     # return state

def bruteForce(state, blocksChoices, choicesMade=None):
    if "." not in set(state): return state, choicesMade
    # print(choicesMade)
    # print2D(state, True)
    if choicesMade is None: choicesMade = []

    # if isInvalid(state): return ""
    if len(blocksChoices) == 0: return state, choicesMade
    # if isSolved(state): return state

    emptyPos = state.find(".") # find first empty position
    for choice in blocksChoices:
        updatedState = updateState(choice[0], choice[1], (emptyPos // blockDims[1], emptyPos % blockDims[1]), state)
        if updatedState: 
            # print(choicesMade + [(choice[0], choice[1])])
            # print2D(updatedState, True)
            blockChoicesCopy = blocksChoices.copy()
            blockChoicesCopy.remove(choice)
            blockChoicesCopy.remove((choice[1], choice[0]))

            bf, choices = bruteForce(updatedState, blockChoicesCopy, choicesMade + [(choice[0], choice[1])])
            if bf: return bf, choices
    return "", choicesMade

def make2D(dims):
    return [["." for _ in range(dims[1])] for _ in range(dims[0])]

def print2D(state, spaces=False):
    # for row in state: print(" ".join(row))
    # if spaces: print("\n\n")
    for i in range(0, len(state), blockDims[1]):
        print(state[i:i+blockDims[1]])
    if spaces: print("\n\n")

def parseArgs(args):
    myDims = []
    i = 0
    while i < len(args):
        if "x" in args[i].lower():
            mySplit = args[i].lower().split("x")
            myDims.append((int(mySplit[0]), int(mySplit[1])))
        else:
            myDims.append((int(args[i]), int(args[i + 1])))
            i += 1
        i+=1
    return myDims

def checkExceedingDimensions(myDims, blocks):
    totalChars = myDims[0] * myDims[1]
    runningChars = 0
    for block in blocks:
        blockArea = block[0] * block[1]
        runningChars += blockArea
        if runningChars > totalChars: return -1,True
    numOf1x1s = totalChars - runningChars
    return numOf1x1s,runningChars > totalChars

def fillHoles(state, choices):
    # holes = []
    # for r, row in enumerate(state):
    #         if "." in row:
    #             pos = (r, row.index("."))
    #             choices[f"{r},{row.index('.')}"] = (1, 1)
    myStr = "Decomposition: ["
    insideContent = ""
    for r, row in enumerate(state):
        for c, col in enumerate(row):
            if f"{r},{c}" in choices:
                insideContent += f"{choices[f'{r},{c}']} "
    if len(insideContent) == 0: return "No decomposition"
    return myStr + insideContent.strip() + "]"

def area(tup):
    return 1/(tup[0] * tup[1])

def isSolved(choices):  
    return blockDims[0] * blockDims[1] == sum([choice[0] * choice[1] for choice in choices])

def main():
    global args, STATS_COUNTER, blockDims
    STATS_COUNTER = {}
    file = open("input.txt").read().split("\n")
    for argsStr in file:
        args = argsStr.split(" ")
        # if not args: args = "14 18 14 5 1x7 1X10 8 3 3x5 18x6".split(" ")
        # if not args: args = "25x30 4X8 4x4 10 6 15x6 11X16 9X9 6x6 4x8 5X5 8x17 8x8".split(" ")
        myDims = parseArgs(args)
        blockDims = myDims[0]
        blocks = myDims[1:]
        num1x1s, exceed = checkExceedingDimensions(blockDims, blocks)
        if exceed:
            print("No decomposition")
            return
        
        blocks += [(block[1], block[0]) for block in blocks]
        blocks += [(1, 1) for _ in range(2*num1x1s)] 
        blocks = sorted(blocks, key=area)
        state = "." * blockDims[0] * blockDims[1]
        sol, choices = bruteForce(state, blocks)
        if(isSolved(choices)): print(f"Decomposition: {choices}")
        else: print("No decomposition")
        # filledSol = fillHoles(sol, choices)

        
        # print(filledSol)
        # print(STATS_COUNTER)

if __name__ == "__main__":
    main()

#Dhruv Chandna Period 6 2025