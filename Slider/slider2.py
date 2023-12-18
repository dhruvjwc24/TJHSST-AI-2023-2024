puzzles = ["BCA_", "B_AC", "_BAC", "AB_C", "ABC_"]

def getDimensions(start):
    #return (width, height)
    l = len(start)
    w = int(l**0.5)
    while l % w != 0:
        w+=1
    return (max(t:=(w, l//w)), min(t))

def get_directions(puzzles, width):
    dirs = []
    for idx,puzzle in enumerate(puzzles[:-1]):
        dirs.append(get_shift(puzzle, puzzles[idx+1], width))
    return "".join(dirs)

def get_shift(pzl1, pzl2, width):
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
        
width,height = getDimensions(puzzles[0])
print(get_directions(puzzles, width))