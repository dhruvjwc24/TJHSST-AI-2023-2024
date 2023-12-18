import sys; args = sys.argv[1:]

def bruteForce(pzl, hexagonIndicies, rowIndicies):
    if isInvalid(pzl, hexagonIndicies, rowIndicies): return ""
    if isSolved(pzl): return pzl
    pos = pzl.find(".")
    choicesSet = [str(i) for i in range(1, 8) if pzl.count(str(i)) < 7]
    for choice in choicesSet:
        subPzl = pzl[:pos] + choice + pzl[pos+1:]
        bf = bruteForce(subPzl, hexagonIndicies, rowIndicies)
        if bf: return bf
    return ""


def isSolved(pzl):
    return not("." in pzl)

def isInvalid(pzl, hexagonIndicies, rowIndicies):
    solved = True
    visited = None
    for strChoice in hexagonIndicies:
        visited = []
        intChoice = [eval(i) for i in strChoice.split(".")]
        for idx in intChoice:
            if pzl[idx] in visited and pzl[idx] != ".": return True
            visited.append(pzl[idx]) 
    for strChoice in rowIndicies:
        visited = []
        intChoice = [eval(i) for i in strChoice.split(".")]
        for idx in intChoice:
            if pzl[idx] in visited and pzl[idx] != ".": return True
            visited.append(pzl[idx]) 
    return False
    

hexagonIndicies = ["0.1.2.6.7.8", "2.3.4.8.9.10", "5.6.7.12.13.14", "7.8.9.14.15.16", "9.10.11.16.17.18", "13.14.15.19.20.21", "15.16.17.21.22.23"]
rowIndicies = ["0.1.2.3.4", "5.6.7.8.9.10.11", "12.13.14.15.16.17.18", "19.20.21.22.23", "0.1.5.6.12", "2.3.7.8.13.14.19", "4.10.9.16.15.21.20", "4.17.18.22.23", "5.12.13.19.20", "0.6.7.14.15.21.22", "1.2.8.9.16.17.23", "3.4.10.11.18"]

if args:
    pzl = args[0]
else:
    pzl = "." * 24

sol = bruteForce(pzl, hexagonIndicies, rowIndicies)
if sol:
    print(" "+ sol[:5] + "\n" + sol[5:12]+ "\n" + sol[12:19]+ "\n "+ sol[19:])
else:
    print("No solution possible")