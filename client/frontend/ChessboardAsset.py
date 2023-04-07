'''
Chessboard Asset class
'''

import pygame

class ChessboardAsset:
    IMAGES = {}
    
    def __init__(self, sqSize):
        self.__loadImages(sqSize)

    def __loadImages(self, sqSize):
        FILE_NAME = ['rp', 'rk', 'rc', 'rh', 'rm', 'rq', 'gp', 'gk', 'gc', 'gh', 'gm', 'gq', 'yp', 'yk', 'yc', 'yh', 'ym', 'yq', 'bp', 'bk', 'bc', 'bh', 'bm', 'bq', 'star']
        for f in FILE_NAME:
            self.IMAGES[f] = pygame.transform.scale(pygame.image.load("frontend/images/" + f + ".png"), (sqSize, sqSize))
