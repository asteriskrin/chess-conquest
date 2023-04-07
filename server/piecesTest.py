from Game.GameController import GameController
from Game.Rook import Rook
from Game.Pawn import Pawn
from Game.Knight import Knight
from Game.King import King
from Game.Bishop import Bishop
from Game.Queen import Queen

# Class for Piece logic testing
"""
String value of pieces
King = K
Queen = Q
Pawn = P
Bishop = B
Knight = H
Rook = R
Star = *
None = None / .

"""
#To Print board
def printBoard(room):
    print("current board")
    #Print current board state
    for i in room.chessboard.pieces:
        for j in i:
            if j is None:
                print("n", end = "  ")
            else:
                print(str(j), end = "  ")
        print()

game = GameController()

player0 = game.makePlayer(1,"Traffy")
player0.star = 100
player1 = game.makePlayer(2, "Treno")
room = game.makeRoom(player0)

print(player0.name + " Makes a room")

room.joinPlayer(player1)
print(player1.name + " Joins the room")
#Add Pieces

#Piece belonging to player 0
rook = Rook(2,3,player0, room.chessboard)
pawn = Pawn(2,4,player0, room.chessboard)
pawn1 = Pawn(3, 5, player0, room.chessboard)
knight0 = Knight(1, 4, player0, room.chessboard)
king0 = King(5, 6, player0, room.chessboard)
bishop0 = Bishop(4, 5, player0, room.chessboard)
queen0 = Queen(0, 0, player0, room.chessboard)

#Piece belonging to player 1
pawn2 = Pawn(6, 6, player1, room.chessboard)

room.chessboard.addPiece(rook)
room.chessboard.addPiece(pawn)
room.chessboard.addPiece(pawn1)
room.chessboard.addPiece(knight0)
room.chessboard.addPiece(king0)
room.chessboard.addPiece(bishop0)
room.chessboard.addPiece(queen0)
room.chessboard.addPiece(pawn2)

#Print current board state
for i in room.chessboard.pieces:
    for j in i:
        if j is None:
            print("n", end = "  ")
        else:
            print(str(j), end = "  ")
    print()
#Print the pieces' available move
print("Rook movement")
print(rook.getMove())
print(rook.move(2,7))

print("Pawn movement")
print(pawn.getMove())
print(pawn.move(2,5))

print("Knight movement")
print(knight0.getMove())
print(knight0.move(6,6))

print("King movement")
print(king0.getMove())
print(king0.move(6,7))

print("Bishop movement")
print(bishop0.getMove())
print(bishop0.move(6,7))

print("Queen movement")
print(queen0.getMove())
print(queen0.move(7,7))

print("Eating test\n")
printBoard(room)
print("Queen eat pawn")
print(queen0.move(5,5))
print(queen0.legalMoves)
print(queen0.movePiece(6,6))
printBoard(room)

print("Promoting a pawn")
printBoard(room)
print(room.chessboard.pieces[2][4].__str__())
print(room.chessboard.promotePiece(room.chessboard.pieces[2][4], "Q"))
print("After Promotion")
printBoard(room)

print("Fusion")
pawn3 = Pawn(0, 0, player0, room.chessboard)
pawn4 = Pawn(0, 1, player0, room.chessboard)
pawn5 = Pawn(0, 2, player0, room.chessboard)
room.chessboard.addPiece(pawn3)
room.chessboard.addPiece(pawn4)
room.chessboard.addPiece(pawn5)
printBoard(room)
piecesList = room.chessboard.getOwnPawns(player0)
print(room.chessboard.getOwnPawnsCoordinates(piecesList))
room.chessboard.fusionPiece(piecesList, "h", 0,0)
printBoard(room)

