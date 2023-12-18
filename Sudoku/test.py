def makeLocs(pzlLen):
    N = int(pzlLen**0.5)
    rowIndices = [set(range(i*N, i*N+N)) for i in range(N)]
    colIndices = [set(range(i, pzlLen, N)) for i in range(N)]
    blockIndices = get_sudoku_block_indices_flat(N)
    return rowIndices + colIndices + blockIndices
    

def get_sudoku_block_indices_flat(N):
    # Compute the dimensions of each block
    width, height = getDimensions(N)
    print(width, height)
    
    blocks = []
    for block_row in range(N // height):
        for block_col in range(N // width):
            block = set()
            for row in range(height):
                for col in range(width):
                    index = (block_row * height + row) * N + (block_col * width + col)
                    block.add(index)
            blocks.append(block)

    return blocks

def getDimensions(pzlLen):
    l = pzlLen
    w = int(l**0.5)
    while l % w != 0:
        w+=1
    return (max(t:=(w, l//w)), min(t))

def create_idx_checks(locs, pzlLen):
    idx_checks = {}
    for idx in range(pzlLen):
        checks = set()
        for loc in locs:
            if idx in loc:
                checks = checks.union(loc)
        checks.remove(idx)
        idx_checks[idx] = checks
    return idx_checks

locs = makeLocs(81)

checks = create_idx_checks(locs, 81)

for check in checks:
    print(len(checks[check]))