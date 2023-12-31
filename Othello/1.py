import sys; args = sys.argv[1:]

def print2D(choicesBoard, spaces=False):
    for i in range(0, len(choicesBoard), int(len(choicesBoard)**0.5)):
        print(choicesBoard[i:i+int(len(choicesBoard)**0.5)])
    if spaces: print("\n")

def idxToPos(idx):
    return (idx // int(len(board)**0.5), idx % int(len(board)**0.5))

def posToIdx(pos):
    return pos[0] * int(len(board)**0.5) + pos[1]

def findPossibleMoves():
    validMoves = {}
    for idx, cell in enumerate(board):
        if cell == token:
            r, c = idxToPos(idx)
            for ra in range(-1, 2):
                for ca in range(-1, 2):
                    if r+ra >= 0 and r+ra < int(len(board)**0.5) and c+ca >= 0 and c+ca < int(len(board)**0.5):
                        if board[(tp:=posToIdx((r+ra, c+ca)))] == oppositeToken:
                            rStart, cStart = r+ra, c+ca
                            flips = {posToIdx((rStart, cStart))}
                            while rStart+ra >= 0 and rStart+ra < int(len(board)**0.5) and cStart+ca >= 0 and cStart+ca < int(len(board)**0.5):
                                if board[(tp:=posToIdx((rStart+ra, cStart+ca)))] == ".":
                                    validMoves[tp] = flips
                                    break
                                elif board[tp] == token: break
                                else: flips.add(tp)
                                rStart += ra
                                cStart += ca
    return validMoves

def main():
    global board, token, oppositeToken
    # args = ['..................x.o.....ooxx..xxxxxx.....ox.......o...........']
    argsLen = len(args)
    if argsLen == 0:
        board = '.'*27+'OX......XO'+'.'*27
        token = 'x'
    elif argsLen == 1:
        if "x" == args[0].lower() or "o" == args[0].lower():
            board = '.'*27+'OX......XO'+'.'*27
            token = args[0].lower()
        else:
            board = args[0]
            numTokens = len(board)-board.count(".")
            if numTokens % 2 == 0: token = 'x'
            else: token = 'o'
    else: board, token = args[0], args[1]
    board = board.lower()
    token = token.lower()
    oppositeToken = 'o' if token == 'x' else 'x'
    validMoves = findPossibleMoves()
    if len(validMoves) == 0: 
        print("No moves possible")
        return
    validMovesStr = ", ".join(sorted([str(move) for move in validMoves.keys()]))
    choicesBoard = board
    for move in validMoves:
        choicesBoard = choicesBoard[:move] + '*' + choicesBoard[move+1:]
    print2D(choicesBoard, True)
    print(f"{board} {board.count('x')}/{board.count('o')}")
    # print(list(validMoves.keys()).split(", "))
    print(f"Possible moves for {token}: {validMovesStr}")

if __name__ == "__main__":
    main()

#Dhruv Chandna 2025 Period 6