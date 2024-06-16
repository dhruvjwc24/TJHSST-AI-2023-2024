import sys; args = sys.argv[1:]
import time
import re

def setglobals():
    arglist = []
    SEEDSTRINGS = []
    DFILE = ""
    HEIGHT = 0
    WIDTH = 0
    BLOCKINGSQ = 0
    BOARD = ""
    NEWBOARD = ""

    arglist.append("dict3.txt")
    for x in args:
        arglist.append(x)
    hlist = arglist[1].split("x")
    HEIGHT = int(hlist[0])
    WIDTH = int(hlist[1])

    for x in arglist[1:]:
        if x.isnumeric():
            BLOCKINGSQ = int(x)
        if x.endswith(".txt"):
            DFILE = x
        if "H" in x.upper() or "V" in x.upper():
            SEEDSTRINGS.append(x)

    for i in range(int(WIDTH)):
        for i in range(int(HEIGHT)):
            BOARD += "-"
    return HEIGHT, WIDTH, BLOCKINGSQ, DFILE, SEEDSTRINGS, BOARD, NEWBOARD

def twoDPrint(newboard, height, width, blockingsq):
    if int(blockingsq) == int(len(newboard)): newboard = len(newboard)*"#"
    for i in range(int(height)):
        print(newboard[i * int(width): (i + 1) * int(width)])

def loadwords():
    worddict = {}
    tempdict = {}
    myDict = "dict3.txt"
    with open(myDict) as d:
        for word in d.readlines():
            word = word.strip()
            if len(word.strip()) < 3 or not re.match("^[a-zA-Z]+$",word): continue
            wordkey = word[0] + str(len(word))
            wordkey2 = "-"+ str(len(word))
            if wordkey in worddict:
                worddict[wordkey].append(word)
            else:
                worddict[wordkey] = [word]
            if wordkey2 in worddict:
                worddict[wordkey2].append(word)
            else:
                worddict[wordkey2] = [word]
    return worddict

def modBoard1(board, blockingsq, seedstrings, width, height):
    newboard = board
    remblocks = blockingsq
    blkinvalid = []
    for word in seedstrings:
        orientation = word[0].upper()
        if word[2].isdigit():
            x = int(word[1:3])
            if len(word) > 5 and word[5].isdigit():
                y = int(word[4:6])
                pwordstart = 6
            else:
                y = int(word[4])
                pwordstart = 5
        else:
            x = int(word[1])
            if len(word) > 4 and word[4].isdigit():
                y = int(word[3:5])
                pwordstart = 5
            else:
                y = int(word[3])
                pwordstart = 4
        if len(word) > pwordstart:
            pword = word[pwordstart:]
        else:
            pword = "#"
        index = pword.find("#")
        blkinword = False
        if index != -1:
            blkinword = True
        adder = 0
        pos = 0
        sympos = len(board) - pos - 1
        if orientation == "V":
            for ch in pword:
                pos = (y+width*x)+adder
                if ch != "#":
                    newboard = newboard[:pos] + ch + newboard[pos + 1:]
                else:
                    if newboard[pos] != "#":
                        newboard = newboard[:pos] + ch + newboard[pos + 1:]
                        sympos = len(board) - pos -1
                        newboard = newboard[:sympos] + "#" + newboard[sympos + 1:]
                        remblocks -= 2
                        if not isvalidblk(newboard,pos,width,height):
                            blkinvalid.append(pos)
                            blkinvalid.append(sympos)
                adder += width
        if orientation == "H":
            for ch in pword:
                pos = y + width * x + adder
                if ch != "#":
                    newboard = newboard[:pos] + ch + newboard[pos + 1:]
                else:
                    if newboard[pos] != "#":
                        newboard = newboard[:pos] + ch + newboard[pos + 1:]
                        sympos = len(board) - pos -1
                        newboard = newboard[:sympos] + "#" + newboard[sympos + 1:]
                        remblocks -= 2
                        if not isvalidblk(newboard,pos,width,height):
                            blkinvalid.append(pos)
                            blkinvalid.append(sympos)
                adder += 1
        #print("pword",pword)
        #twoDPrint(newboard, height, width, blockingsq)
    #print("Debug -1")
    #twoDPrint(newboard, height, width, blockingsq)
    #print("remobl",remblocks)
    newboard, remblocks = fixboard(newboard, width, height, blkinvalid, remblocks)
    print("Post Fix")
    twoDPrint(newboard, height, width, blockingsq)
    #print("remobl",remblocks)
    return newboard, remblocks

def fixboard(newboard, width, height, blkinvalid, remblocks):
    for pos in blkinvalid:
        posx = pos // width
        posy = pos % width
        #print("pos",pos,"posx",posx,"posy",posy)
        spaces = 0
        check = True
        # check left:
        newpos = 0
        if posy == 1 or posy == 2:
            newpos = posx*width+posy-1
            if newboard[newpos] != "#":
                newboard = newboard[:newpos] +"#"+newboard[newpos+1:]
                remblocks -= 1
        if posy == 2:
            newpos = posx*width+posy-2
            if newboard[newpos] != "#":
                newboard = newboard[:newpos] +"#"+newboard[newpos+1:]
                remblocks -= 1
        if posy > 2:
            spaces = 0
            check = True
            move = 1
            while check and spaces < 3:
                newpos = posx*width+posy-move
                if newboard[newpos] != "#": spaces += 1
                #elif newboard[newpos] != "#": check = False
                else: check = False
                move += 1
            if not check:
                for i in range(0,spaces):
                    newpos = posx * width + posy - i - 1
                    newboard = newboard[:newpos] +"#"+newboard[newpos+1:]
                    remblocks -= 1
        # check right:
        newpos = 0
        if posy == width-2 or posy == width-3:
            newpos = posx*width+posy+1
            if newboard[newpos] != "#":
                newboard = newboard[:newpos] +"#"+newboard[newpos+1:]
                remblocks -= 1
        if posy == width-3:
            newpos = posx*width+posy+2
            if newboard[newpos] != "#":
                newboard = newboard[:newpos] +"#"+newboard[newpos+1:]
                remblocks -= 1
        if posy < width-3:
            spaces = 0
            check = True
            move = 1
            while check and spaces < 3:
                newpos = posx*width+posy+move
                if newboard[newpos] != "#": spaces += 1
                else: check = False
                #elif newboard[newpos] != "#": check = False
                move += 1
            if not check:
                for i in range(0,spaces):
                    newpos = posx * width + posy + i + 1
                    newboard = newboard[:newpos] +"#"+newboard[newpos+1:]
                    remblocks -= 1
        # check up:
        newpos = 0
        if posx == 1 or posx == 2:
            newpos = (posx-1)*width+posy
            if newboard[newpos] != "#":
                newboard = newboard[:newpos] +"#"+newboard[newpos+1:]
                remblocks -= 1
        if posx == 2:
            newpos = (posx-2)*width+posy
            if newboard[newpos] != "#":
                newboard = newboard[:newpos] +"#"+newboard[newpos+1:]
                remblocks -= 1
        if posx > 2:
            spaces = 0
            check = True
            move = 1
            while check and spaces < 3:
                newpos = (posx-move)*width+posy
                if newboard[newpos] != "#": spaces += 1
                else: check = False
                #elif newboard[newpos] != "#": check = False
                move += 1
            if not check:
                for i in range(0,spaces):
                    newpos = (posx - i -1) * width + posy
                    newboard = newboard[:newpos] +"#"+newboard[newpos+1:]
                    remblocks -= 1
        # check down:
        newpos = 0
        if posx == height-2 or posx == height-3:
            newpos = (posx+1)*width+posy
            if newboard[newpos] != "#":
                newboard = newboard[:newpos] +"#"+newboard[newpos+1:]
                remblocks -= 1
        if posx == height-3:
            newpos = (posx+2)*width+posy
            if newboard[newpos] != "#":
                newboard = newboard[:newpos] +"#"+newboard[newpos+1:]
                remblocks -= 1
        if posx < height - 3:
            spaces = 0
            check = True
            move = 1
            while check and spaces < 3:
                newpos = (posx+move)*width+posy
                #print("newpos",newpos,"move",move,"width",width,"posx",posx,"post",posy)
                if newboard[newpos] != "#": spaces += 1
                #elif newboard[newpos] == "#": check = False
                else: check = False
                move += 1
            if not check:
                for i in range(0,spaces):
                    newpos = (posx + i +1) * width + posy
                    newboard = newboard[:newpos] +"#"+newboard[newpos+1:]
                    remblocks -= 1
    return newboard, remblocks


def isvalidblk(newboard, pos, width, height):
    posx = pos // width
    posy = pos % width
    isvalid = True
    # check left
    if posy != 0:
        if newboard[posx*width+posy-1] != "#":
            if (posy <= 2) or (posy > 2 and not
            (newboard[posx*width+posy-2] != "#" and newboard[posx*width+posy-3] != "#")):
                isvalid = False
                return isvalid
    # check right
    if posy != width-1:
        if newboard[posx*width+posy+1] != "#":
            if (posy >= width-3) or (posy < width-3
                 and not(newboard[posx*width+posy+2] != "#" and newboard[posx*width+posy+3] != "#")):
                isvalid = False
                return isvalid
    # check up
    if posx != 0:
        if newboard[(posx-1)*width+posy] != "#":
            if (posx <= 2) or (posx > 2 and not
            (newboard[(posx-2)*width+posy] != "#" and newboard[(posx-3)*width+posy] != "#")):
                isvalid = False
                return isvalid
    # check down
    if posx != height-1:
        if newboard[(posx+1)*width+posy] != "#":
            if (posx >= height-3) or (posx < height - 3 and not
            (newboard[(posx+2)*width+posy] != "#" and newboard[(posx+3)*width+posy] != "#")):
                isvalid = False
                return isvalid
    return isvalid


def modBoard2(newboard, blockingsq, width, height):
    newwboard = newboard
    if blockingsq == 0: return newboard, 0
    if blockingsq == len(newboard): return "#"*len(newboard), 0
    fillblocks = 0
    pos = 0
    #twoDPrint(newboard,height,width,blockingsq)
    while (pos < (len(newboard)//2)) and (fillblocks < blockingsq):
        sympos = len(newboard) - pos - 1
        newwboard = newboard
        if (newboard[pos] == "-" and (newboard[sympos] == "-" or newboard[sympos] == "#") and
                isvalidblk(newboard,pos,width,height)):
                newboard = newboard[:pos] + "#" + newboard[pos + 1:]
                fillblocks += 1
                if newboard[sympos] != "#" and isvalidblk(newboard,sympos,width,height):
                    newboard = newboard[:sympos] + "#" + newboard[sympos + 1:]
                    fillblocks += 1
                else:
                    newboard = newwboard
                    fillblocks -=1
        #twoDPrint(newboard, height, width, blockingsq)
        pos += 1
    return newboard, blockingsq-fillblocks


def modBoard3(newboard, blockingsq, width, height):
    newwboard = newboard
    if blockingsq == 0: return newboard, 0
    if blockingsq == len(newboard): return "#"*len(newboard), 0
    fillblocks = 0
    pos = 0
    #twoDPrint(newboard,height,width,blockingsq)
    while (pos < (len(newboard)//2)) and (fillblocks < blockingsq):
        sympos = len(newboard) - pos - 1
        newwboard = newboard
        if (newboard[pos] == "-" and (newboard[sympos] == "-" or newboard[sympos] == "#") and
                isvalidblk(newboard,pos,width,height)):
                newboard = newboard[:pos] + "#" + newboard[pos + 1:]
                fillblocks += 1
                if newboard[sympos] != "#" and isvalidblk(newboard,sympos,width,height):
                    newboard = newboard[:sympos] + "#" + newboard[sympos + 1:]
                    fillblocks += 1
                else:
                    newboard = newwboard
                    fillblocks -=1
        #twoDPrint(newboard, height, width, blockingsq)
        pos += 1
    return newboard, blockingsq-fillblocks


def fillrows(newboard, remblocks, width, height):
    stpos = 0
    fillblocks = 0
    rowhash = "#" * (width)
    for row in range(0,height):
        rowstr = newboard[stpos:stpos+width]
        countsp = width - rowstr.count("#")
        if countsp  <= remblocks and (height - 2*(row+1) >= 3):
            sympos = len(newboard) - (stpos+width)
            countblock = rowstr.count("#")
            if (fillblocks + 2*(width-countblock)) > remblocks: break
            newboard = newboard[:stpos]+rowhash+newboard[stpos+width:]
            newboard = newboard[:sympos]+rowhash+newboard[sympos+width:]
            fillblocks += 2*(width-countblock)
            countblock = 0
            stpos += width
        else: break
    return newboard, remblocks-fillblocks

def fillcols(newboard, remblocks, width, height):
    stpos = 0
    fillblocks = 0
    stpos = newboard.find("-")
    strow = stpos // width
    begrow = strow
    endrow = height - begrow - 1
    rowstr = newboard[strow*width:strow*width+width]
    while fillblocks < remblocks:
        if begrow > endrow:
            begrow = strow
            stpos = begrow*width
        rowstr = newboard[begrow*width:begrow*width+width]
        stpos += rowstr.find("-")
        sympos = len(newboard) - stpos - 1
        newboard = newboard[:stpos] + "#"+ newboard[stpos+1:]
        newboard = newboard[:sympos] + "#" + newboard[sympos+1:]
        fillblocks += 2
        begrow += 1
        stpos = begrow*width
    return newboard


def placewords(placesf, fill, width, height):
    global words, worddict, placed, boardarray, NEWBOARD, counter, posdict, constraints, \
        partial, partialboard, complete
    if fill == len(placesf):
        complete = True
        # Check if all horizontal words are placed
        horizontal_placed = all('H' in place[1] for place in placesf)
        if horizontal_placed:
            print("All horizontal words placed:")
            twoDPrint(NEWBOARD, height, width, 0)
        return True
    wordlen = 0
    pattern = "^"
    places = placesf[fill]
    pos = places[0]
    wordlen = places[2]
    posdisp = "" + str(places[0])+places[1]
    for i in posdict[posdisp]:
        cell = NEWBOARD[i]
        if cell == "#":
            break
        elif cell == "-":
            pattern = pattern + "."
        else:
            pattern = pattern + cell.upper()
    pattern = pattern + "$"
    visited = list()
#    wordlist = [word for word in words if re.match(pattern,word.upper()) and len(word) == wordlen]
    #print(places[0], places[1],places[2],len(wordlist))
    if pattern[1] == ".": wordkey = "-"+str(wordlen)
    elif pattern[1].lower()+str(wordlen) not in worddict.keys(): wordkey = "-"+str(wordlen)
    else: wordkey = pattern[1].lower()+str(wordlen)
    #print("posdisp, pattern, wordkey, worddict",posdisp,pattern,wordkey, worddict[wordkey])
    for word in worddict[wordkey]:
        if word.upper() in placed or not re.match(pattern,word.upper()): continue
        visited.append(word)
        #print("matching", places[0], places[1],places[2],word)
        NEWWBOARD = NEWBOARD
        if places[1] == "H":
            for i in range(len(word)):
                NEWBOARD = NEWBOARD[:pos+i]+word[i]+NEWBOARD[pos+i+1:]
        else:
            for i in range(len(word)):
                NEWBOARD = NEWBOARD[:pos+i*width]+word[i]+NEWBOARD[pos+i*width+1:]
        failedcon = False
        for con in constraints[posdisp]:
            patcon = "^"
            lencon = 0
            letter = False
            for poscon in posdict[con]:
                if NEWBOARD[poscon] == "-":
                    patcon = patcon + "."
                else:
                    patcon = patcon + NEWBOARD[poscon].upper()
                    letter = True
                lencon += 1
            if letter:
                patcon = patcon + "$"
                if patcon[1] == ".":
                    patkey = "-" + str(lencon)
                elif patcon[1].lower() + str(lencon) not in worddict.keys():
                    patkey = "-" + str(lencon)
                else:
                    patkey = patcon[1].lower() + str(lencon)
                #print("  word",word," posdisp",posdisp,"patcon",patcon,"patkey:",patkey,"newboard",NEWBOARD, )
                matchlist = [word for word in worddict[patkey] if re.match(patcon,word.upper())]
                if matchlist == []:
                    #print("matchng", patcon, patkey, worddict[patkey]);
                    failedcon = True
                    break
        #print("failedcon ",failedcon)
        if failedcon: NEWBOARD = NEWWBOARD; continue
        placed.append(word.upper())
        if "Recursion" in stats:
            stats["Recursion"] += 1
        else:
            stats["Recursion"] = 1
        if time.time() - s > counter: counter = counter + 30; print(stats); twoDPrint(NEWBOARD, height, width, 0)
        match = placewords(placesf,fill+1,width,height)
        if match:
            return match
        placed.remove(word.upper())
        NEWBOARD = NEWWBOARD
    if not partial:
        partialboard = NEWBOARD
    partial = True
    return False
worddict = {}
placed = list()
boardarray = [[]]
stats = {}
s = time.time()
NEWBOARD = ""
counter = 29
posdict = {}
constraints = {}
partial = False
complete = False
partialboard = ""
def main():
    global words, placed, worddict, posdict, constraints, NEWBOARD, partial, partialboard, complete, args
    # if not args: args = "7x7 11 V0x5ASSOC V6x6# v5x5# H3x4MOB h3x3#".split()
    if not args: args = "5x5 0 v1x3r V0x4racer".split()
    # if len(args) == 0: print("Command line arguments required");exit()
    HEIGHT, WIDTH, BLOCKINGSQ, DFILE, SEEDSTRINGS, BOARD, NEWBOARD = setglobals()
    worddict = loadwords()
    remblocks = BLOCKINGSQ
    NEWBOARD = BOARD
    if len(BOARD) != BLOCKINGSQ and BLOCKINGSQ > 0 and BLOCKINGSQ % 2 == 1:
        BLOCKINGSQ -= 1
        remblocks = BLOCKINGSQ
        center = (HEIGHT // 2) * WIDTH + (WIDTH//2)
        BOARD = BOARD[:center] + "#" + BOARD[center+1:]
        NEWBOARD = BOARD
    if SEEDSTRINGS != []:
        NEWBOARD, remblocks = modBoard1(BOARD, BLOCKINGSQ, SEEDSTRINGS, WIDTH, HEIGHT)
    # checking for connected
    CHECK = False
    pos1 = WIDTH-3
    pos2 = 2*WIDTH-3
    pos3 = 3*WIDTH-3
    pos4 = (HEIGHT-3)*WIDTH
    pos5 = (HEIGHT-2)*WIDTH
    pos6 = (HEIGHT-1)*WIDTH
    hash3 = "###"
    NEWBOARD5 = NEWBOARD
    if (NEWBOARD5[pos1-1] == "#" and NEWBOARD5[pos2-1] == "#" and NEWBOARD5[pos3-1] == "#" and
            NEWBOARD5[pos3+WIDTH:pos3+WIDTH+3] == "###"):
        CHECK = True
        NEWBOARD5 = (NEWBOARD5[0:pos1] + hash3 + NEWBOARD5[pos1+3:pos2] + hash3 + NEWBOARD5[pos2+3:pos3]
                     + hash3 + NEWBOARD5[pos3+3:pos4] + hash3 + NEWBOARD5[pos4+3:pos5] + hash3 + NEWBOARD5[pos5+3:pos6] + hash3 + NEWBOARD5[pos6+3:])
        print("post connected ", remblocks)
        twoDPrint(NEWBOARD5, HEIGHT, WIDTH, BLOCKINGSQ)
    newwboard = NEWBOARD
    remmblocks = remblocks
    print("post modboard 2 ", remblocks)
    NEWBOARD, remblocks = modBoard2(NEWBOARD, remblocks,WIDTH, HEIGHT)
    twoDPrint(NEWBOARD, HEIGHT, WIDTH, BLOCKINGSQ)
    if remblocks > 0:
        NEWBOARD = newwboard
        remblocks = remmblocks
        twoDPrint(NEWBOARD, HEIGHT, WIDTH, BLOCKINGSQ)
        print("before rows and cols",remblocks)
        NEWBOARD, remblocks = fillrows(NEWBOARD, remblocks,WIDTH, HEIGHT)
        if remblocks > 0:
            NEWBOARD = fillcols(NEWBOARD, remblocks, WIDTH, HEIGHT)
    if CHECK:
        print("post check-connected ", remblocks)
        twoDPrint(NEWBOARD5,HEIGHT,WIDTH,BLOCKINGSQ)
    else:
        print("post check-not connected ", remblocks)
        twoDPrint(NEWBOARD,HEIGHT,WIDTH,BLOCKINGSQ)
    boardarray = [["-" for _ in range(WIDTH)] for _ in range(HEIGHT)]
    pos = 0
    placesf = list()
    posdict = {}
    for row in range(HEIGHT):
        for col in range(WIDTH):
            boardarray[row][col] = NEWBOARD[pos]
            if NEWBOARD[pos] != "#" and (NEWBOARD[pos-1] == "#" or pos%WIDTH == 0):
                poslist = list()
                posdisp = "" + str(pos) + "H"
                checkplaces = WIDTH - col
                wordlen = 0
                charlen = 0
                word = ""
                for i in range(checkplaces):
                    if NEWBOARD[pos + i] == "#": break
                    elif NEWBOARD[pos + i] == "-": wordlen += 1; poslist.append(pos + i)
                    else: word += NEWBOARD[pos+i]; charlen += 1;wordlen += 1; poslist.append(pos+i)
                if wordlen == 0 or wordlen == len(word):
                    placed.append(word.upper())
                else:
                    posword = (pos,"H",wordlen, charlen)
                    placesf.append(posword)
                    posdict[posdisp] = poslist
            if NEWBOARD[pos] != "#" and (NEWBOARD[pos-WIDTH] == "#" or row == 0):
                poslist = list()
                posdisp = "" + str(pos) + "V"
                checkplaces = HEIGHT - row
                wordlen = 0
                charlen = 0
                word = ""
                for i in range(checkplaces):
                    if NEWBOARD[pos + i * WIDTH] == "#": break
                    elif NEWBOARD[pos + i * WIDTH] == "-": wordlen += 1; poslist.append(pos+i*WIDTH)
                    else: word += NEWBOARD[pos+i*WIDTH]; charlen += 1;wordlen += 1;poslist.append(pos+i*WIDTH)
                if wordlen == 0 or wordlen == len(word):
                    placed.append(word.upper())
                else:
                    posword = (pos,"V",wordlen, charlen)
                    placesf.append(posword)
                    posdict[posdisp] = poslist
            pos += 1
    #print("worddict: ",worddict)
    #for place in placesf:
    def plindex(places):
        return places[2]
    placesf = sorted(placesf,key=plindex,reverse=True)
    for k in posdict.keys():
        conlist = set()
        for v in posdict[k]:
            for k1 in posdict.keys():
                if k1 == k: continue
                if v in posdict[k1]:
                    conlist.add(k1)
        constraints[k] = conlist
    print("time: ",time.time()-s)
    match = placewords(placesf,0, WIDTH, HEIGHT)
    print()
    if partial and not complete:
        twoDPrint(partialboard, HEIGHT, WIDTH, 0)
    else:
        twoDPrint(NEWBOARD, HEIGHT, WIDTH, 0)
    print("time: ",time.time()-s)

if __name__ == '__main__': main()
