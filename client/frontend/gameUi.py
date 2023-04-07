import pygame
import chessengine
import button

#Window size
winWidth = 1000
winHeight = 800

#chessboard size
chessWidth = 560
chessHeight = 560

#chessboard dimension
dimension = 8
sqSize = chessWidth // dimension

IMAGES = {}

fps = 20

#color
white = pygame.Color("white")
black = pygame.Color("Black")
blue = pygame.Color("dark blue")

def loadImage():
    pieces = ['rp', 'rk', 'rc', 'rh', 'rm', 'rq', 'gp', 'gk', 'gc', 'gh', 'gm', 'gq', 'yp', 'yk', 'yc', 'yh', 'ym', 'yq', 'bp', 'bk', 'bc', 'bh', 'bm', 'bq', 'star']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (sqSize, sqSize))


def main():
    run = True
    pygame.init()
    #font
    baseFont = pygame.font.Font(None, 24)

    #popupMessage
    popupMessage = "You can Move the Chess Piece"

    WIN = pygame.display.set_mode((winWidth, winHeight))
    WIN.fill(black)
    pygame.display.set_caption('Chess Conquest')
    clock = pygame.time.Clock()
    userText = ""
    background = pygame.image.load("images/background.png")
    
    #button image
    delete_img = pygame.image.load('images/delete.png').convert_alpha()
    castle_img = pygame.image.load('images/wc.png').convert_alpha()
    horse_img = pygame.image.load('images/wh.png').convert_alpha()
    bishop_img = pygame.image.load('images/wm.png').convert_alpha()
    queen_img = pygame.image.load('images/wq.png').convert_alpha()

    #button
    delete_button = button.Button(80, 670, delete_img, 0.2)
    castle_button = button.Button(235, 670, castle_img, 0.6) 
    horse_button = button.Button(335, 670, horse_img, 0.6)
    bishop_button = button.Button(435, 670, bishop_img, 0.6)
    queen_button = button.Button(535, 670, queen_img, 0.6)


    #button flag
    deleteFlag = False
    castleChange = False
    horseChange = False
    bishopChange = False
    queenChange = False

    #Change Piece ID
    changePieceID = 0


    #Gameboard
    gs = chessengine.GameState()
    loadImage()
    ##inputRect = pygame.Rect(610, 710, 330, 30)
    ##chatActive = True
    sqSelected = ()
    playerClicks = []

    while run:
        WIN.blit(background,(0,0))
        # button drawn
        if delete_button.draw(WIN):
            if deleteFlag == False :
                deleteFlag = True
                popupMessage = "Please Select the Piece You Want to Delete"
            else :
                deleteFlag = False
                popupMessage = "You can Move the Chess Piece"

        if castle_button.draw(WIN):
            if castleChange == False :
                castleChange = True
                horseChange = False
                bishopChange = False
                queenChange = False
                changePieceID = 3
                print("Castle Change : " + str(castleChange))
                popupMessage = "Please Select the Piece You Want to Change With Castle"
            else:
                castleChange = False
                popupMessage = "You can Move the Chess Piece"
                print("Castle Change : " + str(castleChange))
        
        if horse_button.draw(WIN):
            if horseChange == False :
                horseChange = True
                castleChange = False
                bishopChange = False
                queenChange = False
                changePieceID = 1
                print("Horse Change : " + str(horseChange))
                popupMessage = "Please Select the Piece You Want to Change With Horse"
            else:
                horseChange = False
                popupMessage = "You can Move the Chess Piece"
                print("Horse Change : " + str(horseChange))
        
        if bishop_button.draw(WIN):
            if bishopChange == False :
                bishopChange = True
                castleChange = False
                horseChange = False
                queenChange = False
                changePieceID = 2
                print("Bishop Change : " + str(bishopChange))
                popupMessage = "Please Select the Piece You Want to Change With Bishop"
            else:
                bishopChange = False
                popupMessage = "You can Move the Chess Piece"
                print("Bishop Change : " + str(bishopChange))

        if queen_button.draw(WIN):
            if queenChange == False :
                queenChange = True
                castleChange = False
                horseChange = False
                bishopChange = False
                changePieceID = 4
                print("Queen Change : " + str(queenChange))
                popupMessage = "Please Select the Piece You Want to Change With Queen"
            else:
                queenChange = False
                popupMessage = "You can Move the Chess Piece"
                print("Queen Change : " + str(queenChange))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
            #     if inputRect.collidepoint(event.pos):
            #         chatActive == True
            #     else:
            #         chatActive == False
            # message = ""
                mouseLocation = pygame.mouse.get_pos()
                print(mouseLocation)
                col = (mouseLocation[0]// sqSize) - 1
                row = (mouseLocation[1]// sqSize) - 1
                if col >= 0 and col  < 8 and row >= 0 and row < 8 :
                    if sqSelected == (row,col):
                        sqSelected = ()
                        playerClicks = []
                    else :
                        sqSelected = (row,col)
                        piece,pieceid = gs.getpiece(row,col)
                        print("Piece : " + piece + " " + "Piece ID : " + str(pieceid))
                        playerClicks.append(sqSelected)
                    
                    if len(playerClicks) == 1 and deleteFlag == True :
                        delete = chessengine.delBidak(playerClicks[0], gs.board)
                        gs.delpiece(delete)
                        deleteFlag = False
                        playerClicks = []
                        popupMessage = "You can Move the Chess Piece"
                        # print(len(playerClicks))
                    elif len(playerClicks) == 1 and castleChange == True:
                        change = chessengine.changeBidak(playerClicks[0], changePieceID, gs.board)
                        gs.changepiece(change)
                        castleChange = False
                        playerClicks = []
                        popupMessage = "You can Move the Chess Piece"
                    elif len(playerClicks) == 1 and horseChange == True:
                        change = chessengine.changeBidak(playerClicks[0], changePieceID, gs.board)
                        gs.changepiece(change)
                        horseChange = False
                        playerClicks = []
                        popupMessage = "You can Move the Chess Piece"
                    elif len(playerClicks) == 1 and bishopChange == True:
                        change = chessengine.changeBidak(playerClicks[0], changePieceID, gs.board)
                        gs.changepiece(change)
                        bishopChange = False
                        playerClicks = []
                        popupMessage = "You can Move the Chess Piece"
                    elif len(playerClicks) == 1 and queenChange == True:
                        change = chessengine.changeBidak(playerClicks[0], changePieceID, gs.board)
                        gs.changepiece(change)
                        queenChange = False
                        playerClicks = []
                        popupMessage = "You can Move the Chess Piece"
                    if len(playerClicks) == 2 :
                        move = chessengine.moveBidak(playerClicks[0], playerClicks[1], gs.board)
                        gs.Makemove(move)
                        # print(move.getMove())
                        sqSelected = ()
                        playerClicks = []                   
            if event.type == pygame.KEYDOWN:
               ## if chatActive == True:
                    ##if event.key == pygame.K_RETURN:
                       ## message == userText
                     ##   userText = ""
                    if event.key == pygame.K_BACKSPACE:
                        userText = userText[:-1]
                    else:
                        userText += event.unicode
        
        drawMessage(81,50,popupMessage,WIN,baseFont)
        drawMessage(370,650,"Piece Change",WIN,baseFont)
        drawMessage(90,750,"Point Needed",WIN,baseFont)
        drawMessage(270,750,"2",WIN,baseFont)
        drawMessage(370,750,"3",WIN,baseFont)
        drawMessage(470,750,"4",WIN,baseFont)
        drawMessage(570,750,"5",WIN,baseFont)
        drawGameState(WIN, gs,sqSelected,blue)
        ##drawChat(WIN, baseFont, userText, inputRect)
        clock.tick(fps)
        pygame.display.flip()


def drawGameState(screen, gs,sqSelected,color):
    drawBoard(screen)
    highlightSquare(screen,sqSelected,color)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for r in range(dimension):
        for c in range(dimension):
            color = colors[((r + c) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(c * sqSize + 80, r * sqSize + 80, sqSize, sqSize))


def drawPieces(screen, board):
    for r in range(dimension):
        for c in range(dimension):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(c * sqSize + 80, r * sqSize + 80, sqSize, sqSize))

def drawChat(screen, font, userText, inputRect):
    pygame.draw.rect(screen, white, pygame.Rect(600, 100, 350, 600))
    pygame.draw.rect(screen, blue, pygame.Rect(600, 700, 350, 50))
    #if active:
        #color = white
    #else:
        #color = black

    pygame.draw.rect(screen, white, inputRect, 2)
    textSurface = font.render(userText, True, (255, 255, 255))
    screen.blit(textSurface, (inputRect.x + 5, inputRect.y + 5))

    # if message != "":
    #     textSurface2 = font.render(message, True, (0, 0, 0))
    #     screen.blit(textSurface2, (625, 100))


def drawMessage(x,y,message,screen,font):
    popup = font.render(message,True,(255,255,255))
    screen.blit(popup,(x, y))

def highlightSquare(screen,sqSelected,color):
    if sqSelected != ():
        r,c = sqSelected
        if c >= 0 and c < 8 and r >=0 and r < 8 :
            s = pygame.Surface((sqSize,sqSize))
            s.set_alpha(100)
            s.fill(color)
            screen.blit(s, (c*sqSize+80, r*sqSize+80))

if __name__ == "__main__":
    main()
