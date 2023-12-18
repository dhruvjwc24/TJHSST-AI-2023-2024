def getDimensions(N):
    l = N
    w = int(l**0.5)
    while l % w != 0:
        w += 1
    return (max(t := (w, l // w)), min(t))

def get_sudoku_block_indices_flat(N):
    # Compute the dimensions of each block
    width, height = getDimensions(N)
    print(width, height)
    
    blocks = []
    for block_row in range(N // height):
        for block_col in range(N // width):
            block = []
            for row in range(height):
                for col in range(width):
                    index = (block_row * height + row) * N + (block_col * width + col)
                    block.append(index)
            blocks.append(block)

    return blocks

# Example usage
N = 6  # for a 4x4 Sudoku
blocks = get_sudoku_block_indices_flat(N)
for i, block in enumerate(blocks):
    print(f"Block {i+1}: {block}")


