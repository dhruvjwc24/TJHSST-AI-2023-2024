import sys; args = sys.argv[1:]

def bruteForce(pzl):
    if isInvalid(pzl): return ""
    if isSolved(pzl): return pzl
    pos = pzl.find(".")
    choicesSet = [str(i) for i in range(DIM) if pzl.count(str(i)) < DIM]
    for choice in choicesSet:
        subPzl = pzl[:pos] + choice + pzl[pos+1:]
        bf = bruteForce(subPzl)
        if bf: return bf
    return ""

def isSolved(pzl):
    return not("." in pzl)

def isInvalid(pzl):
    row = byRow(pzl)
    col = byCol(pzl)
    diag = byDiag(pzl)

    solved = True
    visited = None
    for r in row:
        visited = []
        for e in r:
            if e in visited and e != ".": return True
            visited.append(e)
    for c in col:
        visited = []
        for e in c:
            if e in visited and e != ".": return True
            visited.append(e)
    for d in diag:
        visited = []
        for e in d:
            if e in visited and e != ".": return True
            visited.append(e)
    return False
            

def byCol(pzl):
    return [pzl[i::DIM] for i in range(DIM)]
def byRow(pzl):
    return [pzl[i:i+DIM] for i in range(0, len(pzl), DIM)]
def byDiag(pzl):
    return [pzl[0::DIM+1], pzl[DIM-1:-1:DIM-1]]

def main():
    global DIM
    args = [4, 5, 6, 7]
    for arg in args:
        DIM = arg
        pzl = "." * DIM**2
        sol = bruteForce(pzl)
        for row in byRow(sol):
            print(row)
        print()

if __name__ == "__main__": main()
