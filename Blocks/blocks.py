import sys; args = sys.argv[1:]
import time

# def isInvalid(state):
#     return

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

def bruteForce(state, blocksChoices):
    # if isInvalid(state): return ""
    if len(blocksChoices) == 0: return state
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
                    bf = bruteForce(stateCopy, blockChoicesCopy)
                    if bf == "No decomposition": continue
                    return bf
    return "No decomposition"

def main():
    args = ["5x7", "2x4", "1x6", "5x4"]
    blocks = []
    for block in args[1:]:
        blockSplit = block.split("x")
        blockDims = (int(blockSplit[0]), int(blockSplit[1]))
        blocks.append(blockDims)
    blocksChoices = blocks + [(int(block[1]), int(block[0])) for block in blocks]
    dims = (int((li:=args[0].split("x"))[0]), int(li[1]))
    state = make2D(dims)
    sol = bruteForce(state, blocksChoices)
    print2D(sol)

def make2D(dims):
    return [["." for _ in range(dims[1])] for _ in range(dims[0])]

def print2D(state):
    for row in state: print(" ".join(row))

if __name__ == "__main__":
    main()
