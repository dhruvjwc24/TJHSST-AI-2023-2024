def idxToPos(idx): return (idx // 8, idx % 8)

def posToIdx(row, col): return row * 8 + col

def getOppositeToken(token): return 'o' if token == 'x' else 'x'

def checkSafeToken(pos, brd, token):
    safeDirs = set()
    eTkn = getOppositeToken(token)
    for rc in range(-1, 2):
        for cc in range(-1, 2):
            if rc == 0 and cc == 0: continue
            r, c = idxToPos(pos)
            while r+rc >= 0 and r+rc < 8 and c+cc >= 0 and c+cc < 8:
                r += rc
                c += cc
                if brd[posToIdx(r, c)] == eTkn or brd[posToIdx(r, c)] == ".": continue
            if not (-r, -c) in safeDirs: safeDirs.add((r, c))
            if len(safeDirs) == 4: return True

def main():
    brd = ".......................x...xx.xo...xxxxo..xxxxoo..oooooo.ooooooo"
    tkn = "o"
    print(sum([checkSafeToken(i, brd, tkn) for i in range(64) if brd[i] == "o"]))
    # for pos in range(64):
    #     if brd[pos] == "." and checkSafeToken(pos, brd, tkn):
            

if __name__ == "__main__": main()

#Dhruv Chandna 2025 Period 6