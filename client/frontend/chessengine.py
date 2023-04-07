class GameState():
    def __init__(self):
        self.board = [
            ["star","--","bp","bk","bp","--","--","star"],
            ["--","--","--","bp","--","--","--","--"],
            ["rp","--","--","--","--","--","--","yp"],
            ["rk","rp","--","star","star","--","yp","yk"],
            ["rp","--","--","star","star","--","--","yp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","gp","--","--","--","--"],
            ["star","--","gp","gk","gp","--","--","star"]]

    def Makemove(self, move):
        if self.board[move.startRow][move.startCol] != "--" :  
            piece,pieceid = self.getpiece(move.startRow,move.startCol)
            self.board[move.startRow][move.startCol] = "--"
            self.board[move.endRow][move.endCol] = move.pieceMoved
            #print("Move : " + str(move.startRow) + "," + str(move.startCol) +" to "+ str(move.endRow) + "," + str(move.endCol) + " " + piece)
        else :
            pass

    def getpiece(self, row,col):
        piece = ""
        pieceid = 0
        if self.board[row][col][1] == 'p':
            piece = "Pawn"
            pieceid = 0
        elif self.board[row][col][1] == 'h':
            piece = "Horse"
            pieceid = 1
        elif self.board[row][col][1] == 'm':
            piece = "Bishop"
            pieceid = 2
        elif self.board[row][col][1] == 'c':
            piece = "Castle"
            pieceid = 3
        elif self.board[row][col][1] == 'q':
            piece = "Queen"
            pieceid = 4
        elif self.board[row][col][1] == 'k':
            piece = "King"
            pieceid = 5
        else :
            piece = "None"
            pieceid = None
        return piece,pieceid


    def delpiece(self,delete):
            piece,pieceid = self.getpiece(delete.row,delete.col)
            self.board[delete.row][delete.col] = "--"
            #print("Deleted : " + str(delete.row) + "," + str(delete.col) + " "+ piece)

    def changepiece(self,change):
        if self.board[change.row][change.col] != "--" and self.board[change.row][change.col] != "star":
            if change.pieceid == 1:
                if self.board[change.row][change.col][0] == 'b':
                    self.board[change.row][change.col] = 'bh'
                elif self.board[change.row][change.col][0] == 'y':
                    self.board[change.row][change.col] = 'yh'
                elif self.board[change.row][change.col][0] == 'r':
                    self.board[change.row][change.col] = 'rh'
                elif self.board[change.row][change.col][0] == 'g':
                    self.board[change.row][change.col] = 'gh'    
            elif change.pieceid == 2:
                if self.board[change.row][change.col][0] == 'b':
                    self.board[change.row][change.col] = 'bm'
                elif self.board[change.row][change.col][0] == 'y':
                    self.board[change.row][change.col] = 'ym'
                elif self.board[change.row][change.col][0] == 'r':
                    self.board[change.row][change.col] = 'rm'
                elif self.board[change.row][change.col][0] == 'g':
                    self.board[change.row][change.col] = 'gm'    
            elif change.pieceid == 3:
                if self.board[change.row][change.col][0] == 'b':
                    self.board[change.row][change.col] = 'bc'
                elif self.board[change.row][change.col][0] == 'y':
                    self.board[change.row][change.col] = 'yc'
                elif self.board[change.row][change.col][0] == 'r':
                    self.board[change.row][change.col] = 'rc'
                elif self.board[change.row][change.col][0] == 'g':
                    self.board[change.row][change.col] = 'gc'
            elif change.pieceid == 4:
                if self.board[change.row][change.col][0] == 'b':
                    self.board[change.row][change.col] = 'bq'
                elif self.board[change.row][change.col][0] == 'y':
                    self.board[change.row][change.col] = 'yq'
                elif self.board[change.row][change.col][0] == 'r':
                    self.board[change.row][change.col] = 'rq'
                elif self.board[change.row][change.col][0] == 'g':
                    self.board[change.row][change.col] = 'gq'    
    


class moveBidak():
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]


    # def getMove(self):
    #     move = str(self.startRow) + "," + str(self.startCol) + " to " + str(self.endRow) + "," + str(self.endCol) + " " + piece
    #     return move


class delBidak():
    def __init__(self,startSq, board):
        self.row = startSq[0]
        self.col = startSq[1]

class changeBidak():
    def __init__(self,startSq,pieceID, board):
        self.row = startSq[0]
        self.col = startSq[1]
        self.pieceid = pieceID
