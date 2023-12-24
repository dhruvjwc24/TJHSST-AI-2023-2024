import sys; args = sys.argv[1:]

import time, math, random, re

dims = (4,4)

# Main Function
def aStar(root, goal):
    if not(isPossible(root, goal)): return(f"{root}: X")
    if root == goal: return(f"{root}: G")
    openSet = {i:[] for i in range(81)}
    fVal = f(root, goal, 0)
    openSet[fVal].append((root, 0))
    closedSet = {root: ""}
    while True:
        #openSet.sort()
        for idx in openSet:
            bucket = openSet[idx]
            if bucket:
                element = bucket.pop(0)
                node, nodeLevel = element
                break
        for nbr in neighbors(node):
            if nbr in closedSet: continue
            closedSet[nbr] = node
            openSet[f(node, goal, nodeLevel)].append((nbr, nodeLevel+1))
            if nbr == goal: 
                path = [nbr]
                while node:
                    path.insert(0, node)
                    node = closedSet.get(node)
                return (f"{root}: {getCondensedPath(path)}")
# Get Underscore Shift
def getShift(pzl1, pzl2):
    width = dims[0]
    pzl1UndPos = pzl1.find("_")
    pzl2UndPos = pzl2.find("_")

    pzl1UndPosMod = pzl1UndPos % width
    pzl2UndPosMod = pzl2UndPos % width

    if pzl1UndPosMod == pzl2UndPosMod:
        if(pzl2UndPos<pzl1UndPos):
            return "U"
        else:
            return "D"
    else:
        if(pzl2UndPos>pzl1UndPos):
            return "R"
        else:
            return "L"

# Get Condensed Path
def getCondensedPath(puzzles):
    return "".join([getShift(puzzle, puzzles[idx+1]) for idx, puzzle in enumerate(puzzles[:-1])])

# Get Neighbors
def neighbors(puzzle):
    w, h = dims
    undInd = puzzle.index('_')
    col, row = undInd % w, undInd // w
    neighbors = []

    def is_valid(x, y):
        return 0 <= x < w and 0 <= y < h

    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_col, new_row = col + dx, row + dy
        if is_valid(new_col, new_row):
            new_undInd = new_row * w + new_col
            new_puzzle = list(puzzle)
            new_puzzle[undInd], new_puzzle[new_undInd] = new_puzzle[new_undInd], new_puzzle[undInd]
            neighbors.append(''.join(new_puzzle))

    return neighbors

# Inversion Count
def inversionCount(puzzle):
    count = 0
    for i in range((l:=len(puzzle))):
        for j in range(i+1, l):
            if puzzle[i] != '_' and puzzle[j] != '_' and puzzle[i] > puzzle[j]:
                count += 1
    return count

# Is it possible to reach goal from root
def isPossible(root, goal):
    icRoot = inversionCount(root)
    icGoal = inversionCount(goal)
    return not(icRoot%2!=icGoal%2 and dims[0]%2==1)

# f(x) = h(x) + level
def f(root, goal, level):
    return h(root, goal) + level

# Manhattan Distance
def h(root, goal):
    return sum(get_tile_MD(tile, root, goal) for tile in root if tile != '_')

# Manhattan Distance Helper Functions
def get_vertical_dist(tile, root, goal):
    return abs(root.find(tile) % dims[0] - goal.find(tile) % dims[0])

def get_horizontal_dist(tile, root, goal):
    return abs(root.find(tile) // dims[1] - goal.find(tile) // dims[1])

def get_tile_MD(tile, root, goal):
    return get_horizontal_dist(tile, root, goal) + get_vertical_dist(tile, root, goal)


puzzlesFile = open("input.txt").read().splitlines()
# puzzlesFile = open(args[0]).read().splitlines()
goal = puzzlesFile[0]

t1_start = time.perf_counter() 
for start in puzzlesFile:
    print(aStar(start, goal))
print(f"\nElasped time: {time.perf_counter()-t1_start}s")

#Dhruv Chandna Period 6 2025