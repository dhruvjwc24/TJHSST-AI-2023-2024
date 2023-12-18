import sys; args = sys.argv[1:]
import time

def updateStats(funcName):
    if funcName in STATS_COUNTER: STATS_COUNTER[funcName] += 1
    else : STATS_COUNTER[funcName] = 1

def isSolved(state):  
    for row in state:
        if "." in row: return False
    return True

def updateState(state, block, r, c):
    for row in range(r, r + block[0]):
        for col in range(c, c + block[1]):
            if row >= len(state) or col >= len(state[0]): return ""
            if state[row][col] == "X": return ""
            state[row][col] = "X"
    return state

def bruteForce(state, blocksChoices, choicesMade=None):
    print(choicesMade)
    print2D(state, True)
    if choicesMade is None:
        choicesMade = {}

    # if isInvalid(state): return ""
    if len(blocksChoices) == 0: 
        return state, choicesMade
    # if isSolved(state): return state

    for r in range(len(state)):
        for c in range(len(state[r])):
            if state[r][c] == ".":
                for choice in blocksChoices:
                    stateCopy = [row[:] for row in state]
                    stateCopy = updateState(stateCopy, choice, r, c)
                    if stateCopy == "": continue

                    blockChoicesCopy = [*blocksChoices]
                    blockChoicesCopy.remove(choice)
                    blockChoicesCopy.remove((choice[1], choice[0]))

                    choicesMadeCopy = choicesMade.copy()
                    choicesMadeCopy[f"{r},{c}"] = choice
                    # choicesMadeCopy = choicesMade + [choice]
                    updateStats("bruteForce")
                    bf, choices = bruteForce(stateCopy, blockChoicesCopy, choicesMadeCopy)
                    if bf != "No decomposition":
                        return bf, choices

    return "No decomposition", choicesMade

def make2D(dims):
    return [["." for _ in range(dims[1])] for _ in range(dims[0])]

def print2D(state, spaces=False):
    for row in state: print(" ".join(row))
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
        if runningChars > totalChars: return True
    
    return runningChars > totalChars

def isSolved(myDims, blocks):
    totalChars = myDims[0] * myDims[1]
    runningChars = 0
    for block in blocks:
        blockArea = block[0] * block[1]
        runningChars += blockArea
        if runningChars > totalChars: return False
    
    return runningChars == totalChars

def fillHoles(state, choices):
    holes = []
    for r, row in enumerate(state):
            if "." in row:
                pos = (r, row.index("."))
                choices[f"{r},{row.index('.')}"] = (1, 1)
    myStr = "Decomposition: ["
    myTuples = []
    for r, row in enumerate(state):
        for c, col in enumerate(row):
            if f"{r},{c}" in choices:
                myTuples.append(choices[f"{r},{c}"])
                myStr += f"{choices[f'{r},{c}']} "
    return myTuples, myStr.strip() + "]"

def area(tup):
    return 1/(tup[0] * tup[1])

def main():
    global args, STATS_COUNTER
    STATS_COUNTER = {}
    if not args: args = "13X14 11x3 1 6 4X3 3 13 9x8 10 1".split(" ")
    myDims = parseArgs(args)
    blockDims = myDims[0]
    blocks = myDims[1:]
    if checkExceedingDimensions(blockDims, blocks):
        print("No decomposition")
        return
    blocksChoices = blocks + [(block[1], block[0]) for block in blocks]
    sortedBlocks = sorted(blocksChoices, key=area)
    state = make2D(blockDims)
    sol, choices = bruteForce(state, sortedBlocks)
    filledTuples, filledSol = fillHoles(sol, choices)
    print(filledSol)
    print(isSolved(blockDims, filledTuples))
    # print2D(filledTuples, True)

if __name__ == "__main__":
    main()

#Dhruv Chandna Period 6 2025