# Game Module Documentation
This page contains documentation of Game Module.

## Prerequisite
You have to instantiate GameController class.
```python
game = GameController()
```

## Create Room
When a player wants to create a room, call this function:
```python
game.createRoom(socketId, playerName)
```
Parameter:
* socketId (int): Socket port
* playerName (string): Player name

Return:
* Room ID (int): Room ID. If the room creation is failed, then room ID is -1.

## Join Room
When a player wants to join a room, call this function:
```py
game.enterRoom(socketId, playerName, roomId)
```
Parameter:
* socketId (int): Socket port
* playerName (string): Player name
* roomId (int): Room ID
  
Return:
* Room ID (int). If joining room is failed, it returns -1.
* List of [Player Socket ID, Player Name]. For example, [[6000, "Lily"], [6020, "Jack"]]

## Start game
When a room host clicks on Start Game button, use this function.

```py
game.startGame(playerSocketId, roomId)
```

Parameter:
* playerSocketId (int): Room host player socket ID
* roomId (int): Room ID

Return:
* Status (bool). True if game is started successfully.
* List of [Player Socket ID, Player Name]. For example, [[6000, "Lily"], [6020, "Jack"]]

## Get Available Movement of Piece
This function is triggered when a player click on his piece on chessboard.

A chessboard is represented as 2D Array. 
For example, if the chessboard size is 8x8, then it is the same as 2D Array with 8x8 size.

Use this function to get all of available movement of a piece on specific position in a room.
```py
game.getPieceMove(roomId, x, y)
```

Parameter:
* roomId (int): Room ID
* x (int): X position of the piece
* y (int): Y position of the peice

Return:
* List of available movement (List of [x, y]). For example, [[1,2],[2,3],[3,4]]. If the list is empty ([]), it means that there is no available move for the piece.

Note:

X = 0 and Y = 0 are on the top left.

## Move Piece
To move a piece in chessboard, use this function.
```py
game.playerMovePiece(playerSocketId, sx, sy, fx, fy)
```

Parameter:
* playerSocketId (int): player socket ID
* sx (int): piece x position
* sy (int): piece y position
* fx (int): x destination
* fy (int): y destination

Return:
* Chessboard state (Array 2D). If moving piece is failed, it returns None.
* Next player turn [Player Socket ID, Player Name]. For example, [6000, "Lily"]
* Chessboard owner state (Array 2D) containing owner name for each (x, y) piece
* Player List In Room (Array of [Player Socket ID, Player Name]). For example: [[6000, "Lily"], [6001, "Aba"]]
* Star data (Array of [Player Name, Amount Star]). For example: [["Lily", 3], ["Aba", 5]]
* Winner (string). If the game is not over yet, winner is not None. If the game is over, winner contains the winner name.

## Buy Pawn
Player can buy pawn. Price is 1 star. Buying pawn counts as 1 turn.

Use this function.
```
game.buyPawn(playerSocketId, x, y)
```

Parameter:
* playerSocketId (int): Player's socket ID who buys pawn
* x (int): New pawn x position
* y (int): New pawn y position

Return:
* Chessboard state (Array 2D). If moving piece is failed, it returns None.
* Next player turn [Player Socket ID, Player Name]. For example, [6000, "Lily"]
* Chessboard owner state (Array 2D) containing owner name for each (x, y) piece
* Player List In Room (Array of [Player Socket ID, Player Name]). For example: [[6000, "Lily"], [6001, "Aba"]]
* Star data (Array of [Player Name, Amount Star]). For example: [["Lily", 3], ["Aba", 5]]

## Promote Pawn
A pawn can be promoted by paying star points.

For example, John have a Pawn on (2, 3) position.
He have 5 star points.
He can pay 5 star points and change the Pawn into Knight.

Note:

Promoting pawn counts as one turn. In other word, after promoting pawn, the turn is over.

Call this function to promote a pawn.

```py
game.promotePawn(socketPlayerId, x, y, pieceType)
```

Parameter:
* socketPlayerId (int): Player's socket ID
* x (int): Pawn x position
* y (int): Pawn y position
* pieceType (string): New piece type (see note below)

Return:
* Chessboard state (Array 2D). If moving piece is failed, it returns None.
* Next player turn [Player Socket ID, Player Name]. For example, [6000, "Lily"]
* Chessboard owner state (Array 2D) containing owner name for each (x, y) piece
* Player List In Room (Array of [Player Socket ID, Player Name]). For example: [[6000, "Lily"], [6001, "Aba"]]
* Star data (Array of [Player Name, Amount Star]). For example: [["Lily", 3], ["Aba", 5]]

Note:

Piece Type:
* "q" = queen
* "h" = knight
* "c" = rook
* "m" = bishop

## Fusion piece
All pawn can be combined into a new piece with different type. 

For example, knight price is 3 star points while pawn price is 1 star points. 
John have 3 pawns in chessboard.
He can remove all pawns and get a knight.
The knight can be placed anywhere in the chessboard.

Another example, knight price is 3 star points while pawn price is 1 star points. 
John have 6 pawns in chessboard.
He can remove all pawns and get a knight.
The knight can be placed anywhere in the chessboard.

Use this function to do fusion.
```
game.fusionPiece(socketPlayerId, pieceType, x, y)
```

Parameter:
* socketPlayerId (int): Player's socket ID who does fusion
* pieceType (string): New piece type (see note below)
* x (int): New piece x position
* y (int): New piece y position

Return:
* Chessboard state (Array 2D). If moving piece is failed, it returns None.
* Next player turn [Player Socket ID, Player Name]. For example, [6000, "Lily"]
* Chessboard owner state (Array 2D) containing owner name for each (x, y) piece
* Player List In Room (Array of [Player Socket ID, Player Name]). For example: [[6000, "Lily"], [6001, "Aba"]]

Piece Type:
* "q" = queen
* "h" = knight
* "c" = rook
* "m" = bishop