# Frontend Module Documentation
This page contains frontend module documentation.

## Start
Before using frontend module, you have to instantiate a class below.
```py
gameFrontend = GameFrontend()
```

## Open chess game window
To open chess game window, use this function.
```py
chessWindow = gameFrontend.openChessGameWindow()
```

Return:
* Instance of ChessGameWindow

## To change chessboard state
Use this function.
```
    chessWindow.setBoardState(chessboardState, ownerState)
```

Parameter:
* chessbaordState (Array 2D)
* ownerState (Array 2D)

Return:
* void

## To change pop up message
Use this function.
```
    chessWindow.setPopUpMessage(message)
```

Parameter: 
* message (string)

Return:
* void

## Highlight box
To highlight box use this function.
```
    chessWindow.showMovementHighlight(coords)
```

Parameter:
* coords (List[[x, y]])

Return:
* void

## Remove all highlight
```
    chessWindow.hideMovementHighlight()
```