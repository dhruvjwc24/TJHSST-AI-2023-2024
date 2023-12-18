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
    numOf1x1s = totalChars - runningChars
    return numOf1x1s,runningChars > totalChars

def fillHoles(state, choices):
    # holes = []
    # for r, row in enumerate(state):
    #         if "." in row:
    #             pos = (r, row.index("."))
    #             choices[f"{r},{row.index('.')}"] = (1, 1)
    myStr = "Decomposition: ["
    for r, row in enumerate(state):
        for c, col in enumerate(row):
            if f"{r},{c}" in choices:
                myStr += f"{choices[f'{r},{c}']} "
    return myStr.strip() + "]"

def area(tup):
    return 1/(tup[0] * tup[1])

def main():
    global args, STATS_COUNTER
    STATS_COUNTER = {}
    file = open("/Users/dhruvchandna/Documents/Documents - Jitendra’s MacBook Pro/AI/Blocks/testCases.txt").read().split("\n")
    # args = "10 11 10x2 10 2 3X10 2X5 10 1 2x10".split(" ")
    for argsStr in file:
        args = argsStr.split(" ")
        myDims = parseArgs(args)
        blockDims = myDims[0]
        blocks = myDims[1:]
        num1x1s, exceed = checkExceedingDimensions(blockDims, blocks)
        if exceed:
            print("No decomposition")
            return
        
        blocksChoices = blocks + [(block[1], block[0]) for block in blocks]
        blocksChoices += [(1, 1) for _ in range(2*num1x1s)] 
        blocksChoices = sorted(blocksChoices, key=area)
        state = make2D(blockDims)
        sol, choices = bruteForce(state, blocksChoices)
        filledSol = fillHoles(sol, choices)
        print(filledSol)
        # print(STATS_COUNTER)

if __name__ == "__main__":
    main()

#Dhruv Chandna Period 6 2025