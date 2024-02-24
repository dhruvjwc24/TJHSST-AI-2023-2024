import d_10 as myFile

board = '................ooooooooxoxxxxo..ooxoooxooooooo.....o...........'
token = 'x'

stables = set()
for pos in range(64):
    if myFile.checkStability(pos, board, stables):
        stables.add(pos)
print(stables)