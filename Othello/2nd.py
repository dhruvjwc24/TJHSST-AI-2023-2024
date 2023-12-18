import sys; args = sys.argv[1:]

def print2D(choicesBoard, spaces=False):
    for i in range(0, len(choicesBoard), int(len(choicesBoard)**0.5)):
        print(choicesBoard[i:i+int(len(choicesBoard)**0.5)])
    if spaces: print("\n")

def idxToPos(idx):
    return (idx // int(len(board)**0.5), idx % int(len(board)**0.5))

def posToIdx(row, col):
    return row * int(len(board)**0.5) + col

def findPossibleMoves():
    validMoves = {}
    for idx, cell in enumerate(board):
        if cell == token:
            r, c = idxToPos(idx)
            for ra in range(-1, 2):
                for ca in range(-1, 2):
                    flips = set()
                    if r+ra >= 0 and r+ra < int(len(board)**0.5) and c+ca >= 0 and c+ca < int(len(board)**0.5):
                        if board[(tp:=posToIdx(r+ra, c+ca))] == oppositeToken:
                            rStart, cStart = r+ra, c+ca
                            flips.add(posToIdx(rStart, cStart))
                            while rStart+ra >= 0 and rStart+ra < int(len(board)**0.5) and cStart+ca >= 0 and cStart+ca < int(len(board)**0.5):
                                if board[(tp:=posToIdx(rStart+ra, cStart+ca))] == ".":
                                    if tp in validMoves: validMoves[tp] |= flips
                                    else: validMoves[tp] = flips
                                    break
                                elif board[tp] == token: break
                                else: flips.add(tp)
                                rStart += ra
                                cStart += ca
    return validMoves

def convertMoveToIdx(move):
    if len(move) > 2: return -1
    if move.isdigit():
        return int(move)
    else:
        col, row = ord(move[0])-65, int(move[1])-1
        return posToIdx(row, col)

def makeMove(move, validMoves, token):
    newBoard = board
    newBoard = newBoard[:move] + token + newBoard[move+1:]
    for idx in validMoves[move]:
        newBoard = newBoard[:idx] + token + newBoard[idx+1:]
    return newBoard
        
def getToken(board):
    numTokens = len(board)-board.count(".")
    if numTokens % 2 == 0: return 'x'
    else: return 'o'

def main():
    global args, board, token, moves, oppositeToken
    board, token, moves = '', '', []
    # if len(args) == 0: args = "xo.oooxoxxoxooxoxoxoooooxxooxxooxxxxoxxoxoooooxoxooxxxxooooooooo o 2".split(" ")
    for arg in args:
        if len(arg) == 64:
            board = arg
        elif arg.lower() in "xo":
            token = arg.lower()
        else:
            moves.append(arg)
    if board == '': board = '.'*27+'ox......xo'+'.'*27
    board = board.lower()
    if token == '': token = getToken(board)
    if moves == '': moves = []

    oppositeToken = 'o' if token == 'x' else 'x'
    validMoves = findPossibleMoves()
    if len(validMoves) == 0: print(f"{board} {board.count('x')}/{board.count('o')}"); return
    validMovesStr = ", ".join(sorted([str(move) for move in validMoves.keys()]))
    choicesBoard = board
    for move in validMoves: choicesBoard = choicesBoard[:move] + '*' + choicesBoard[move+1:]
    print2D(choicesBoard, True)
    print(f"{board} {board.count('x')}/{board.count('o')}")
    print(f"Possible moves for {token}: {validMovesStr}\n")

    for move in moves:
        moveIdx = convertMoveToIdx(move.upper())
        if not moveIdx in validMoves: print("Invalid move"); return
        board = makeMove(moveIdx, validMoves, token)
        token = oppositeToken
        oppositeToken = 'o' if token == 'x' else 'x'
        validMoves = findPossibleMoves()
        # if len(validMoves) == 0: print("No moves possible"); return
        validMovesStr = ", ".join(sorted([str(move) for move in validMoves.keys()]))
        choicesBoard = board
        for move in validMoves: choicesBoard = choicesBoard[:move] + '*' + choicesBoard[move+1:]
        print(f"{oppositeToken} plays to {moveIdx}")
        print2D(choicesBoard, True)
        print(f"{board} {board.count('x')}/{board.count('o')}")
        print(f"Possible moves for {token}: {validMovesStr}\n")

if __name__ == "__main__":
    main()

#Dhruv Chandna 2025 Period 6