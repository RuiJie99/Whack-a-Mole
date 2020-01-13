import sys
import pygame
pygame.init()
import random
import numpy
from PIL import Image
import os


print(pygame.ver)
pygame.font.init()
#just to make it easier
false = False
true = True

#lenght and width of player image
xPlayer = 50
yPlayer = 50
playerNumber = 30

#LOADED IMAGES
imagePlayer = pygame.image.load("image_player.png")
imageWall = pygame.image.load("image_wall.png")
imageStart = pygame.image.load("image_start.png")
imageFinish = pygame.image.load("image_boom.png")
imageTarger = pygame.image.load("image_target.png")
scoreBoard = pygame.image.load("SCOREBOARD.png")
startScreen = pygame.image.load("start_screen.png")


class difficulty:
    Easy = 10
    Hard = 5


#SCREEN
windowWidth = 500
windowLenght = 500
display_surf = pygame.display.set_mode((windowWidth, windowLenght))

"""
future methods:
    - multiple moles at the same time
    - multiple blocks coverage
"""

#maze and everything related

#TODO: restructure code (isolate mole as class)
#TODO: restructure code (isolate scoreBoard as class)
#TODO: restucture code (isolate hammer as class)

class map:
    def __init__(self):
        self.gameOver = false
        self.width = 10
        self.lenght = 10
        self.nbMoleHit = 0
        self.score = pygame.font.SysFont(
            'Comic Sans MS', 20).render(str(self.nbMoleHit), False, (0, 0, 0))
        self.diff = difficulty.Easy
        self.map = [
            [ 0, 2, 1, 1, 1,  1, 1, 1, 1, 1],
            [ 0, 2, 1, 1, 1,  1, 1, 1, 1, 1],
            [ 0, 2, 1, 1, 1,  1, 1, 1, 1, 1],
            [ 1, 1, 1, 1, 1,  1, 1, 1, 1, 1],
            [ 1, 1, 1, 1, 1,  1, 1, 1, 1, 1],
            [ 1, 1, 1, 1, 1,  1, 1, 1, 1, 1],
            [ 1, 1, 1, 1, 1,  1, 1, 1, 1, 1],
            [ 1, 1, 1, 1, 1,  1, 1, 1, 1, 1],
            [ 1, 1, 1, 1, 1,  1, 1, 1, 1, 1],
            [ 1, 1, 1, 1, 1,  1, 1, 1, 1, 1],
        ]
    def checkMouseInside(self, xMin, xMax, yMin, yMax, posMouse):
        if (posMouse[0] > xMin and posMouse[0] < xMax
        and posMouse[1] > yMin and posMouse[1] < yMax):
            return true
        else:
            return false

    def start_Screen(self):
        quitScreen = false
        display_surf.blit(startScreen, (0,0))
        pygame.display.update()
        while(not quitScreen):
            for event in pygame.event.get():
                #TODO: get mouse pos
                #TODO: check if inside
                posMouse = pygame.mouse.get_pos()

                if ((event.type == pygame.MOUSEBUTTONDOWN)
                    and (self.checkMouseInside(111,380,250,300, posMouse))):
                    quitScreen = true
                    self.diff = difficulty.Easy
                elif((event.type == pygame.MOUSEBUTTONDOWN)
                    and (self.checkMouseInside(111,380,322,366, posMouse))):
                    self.diff = difficulty.Hard
                    quitScreen = true

                if event.type == pygame.QUIT:
                    exit()

    def drawMap(self):
        #TODO: pass image by adress or by pointer
        for i in range(0,self.width):
            for j in range(0,self.lenght):
                if self.map[i][j] == 1:
                    display_surf.blit(imageWall, (i*xPlayer, j*yPlayer))
                elif self.map[i][j] == 2:
                    display_surf.blit(imageWall, (i*xPlayer, j*yPlayer))
                elif self.map[i][j] == 0:
                    display_surf.blit(scoreBoard, (0, 0))

    def fillScreenBlack(self):
        pygame.Surface.fill(display_surf,(0,0,0))

    def getPossiblePositions(self):
        array2BReturned = []
        for i in range(0, self.width):
            for j in range(0, self.lenght):
                if self.map[i][j] == 1:
                    array2BReturned.append([i, j])
        return array2BReturned

    def returnRandPosition(self):
        positionArray = self.getPossiblePositions()
        x = random.randint(0, len(positionArray)-1)
        position = positionArray[x]
        return position

    def drawBlock(self, image, position):
        if(position == [0, 0] or position == [0, 1]):
            display_surf.blit(scoreBoard, tuple([0,0]))

    def blitBlocksAroundHammer(self, positions):
        # TODO: correct positions of blocks
        # NOTE: x and y positions are inverted
        newPositions = [(positions[0] - positions[0]%50), (positions[1] - positions[1]%50)]
        newBlockCenter = newPositions

        newBlockBottomRight = (newPositions[0]+50, newPositions[1]+50)
        newBlockUpLeft = (newPositions[0]-50, newPositions[1]-50)
        newBlockUpRight = (newPositions[0]+50, newPositions[1]-50)
        newBlockBottomLeft = (newPositions[0]-50, newPositions[1]+50)

        newBlockUpRight2 = (newPositions[0]+100, newPositions[1]-50)
        newBlockBottomRight2 = (newPositions[0]+100, newPositions[1]+50)

        newBlockRight = (newPositions[0]-50, newPositions[1])
        newBlockLeft = (newPositions[0]+50, newPositions[1])
        newBlockLeft2 = (newPositions[0] + 100, newPositions[1])
        newBlockUp = (newPositions[0], newPositions[1]+50)
        newBlockBottom = (newPositions[0], newPositions[1]-50)

        display_surf.blit(imageWall, newBlockCenter)
        display_surf.blit(imageWall, newBlockBottomRight)
        display_surf.blit(imageWall, newBlockUpLeft)

        display_surf.blit(imageWall, newBlockUpRight)
        display_surf.blit(imageWall, newBlockBottomLeft)
        display_surf.blit(imageWall, newBlockUp)

        display_surf.blit(imageWall, newBlockBottom)
        display_surf.blit(imageWall, newBlockRight)
        display_surf.blit(imageWall, newBlockLeft)

        display_surf.blit(imageWall, newBlockLeft2)
        display_surf.blit(imageWall, newBlockUpRight2)
        display_surf.blit(imageWall, newBlockBottomRight2)

        display_surf.blit(scoreBoard, (0,0))

    def moleClickDetection(self, posMouse, posMole, initialPos):

        if posMouse == posMole:
            display_surf.blit(imageFinish, tuple(posMouse))
        #click area must be within:

        verticalPosUpperLimit = posMole[1]
        verticalLowerLimit = initialPos[1]
        print('upper : ', verticalPosUpperLimit, 'lower : ', verticalLowerLimit)

        #up to 50 pixel to the right of the position of mole
        horizontalLimitLeft = posMole[0]
        horizontalLimitRight = posMole[0] + 50
        print('upper : ', horizontalLimitLeft, 'lower : ', horizontalLimitRight)


        inVerticalRange = (posMouse[1] >= verticalPosUpperLimit) and (posMouse[1] <= verticalLowerLimit)
        print(posMouse[1], verticalPosUpperLimit, posMouse[0], verticalLowerLimit)
        inHorizontalRange = (posMouse[0] >= horizontalLimitLeft) and (posMouse[0] <= horizontalLimitRight)
        if (inVerticalRange and inHorizontalRange):
            self.nbMoleHit += 1
        return (inVerticalRange and inHorizontalRange)

    def blitScore(self, score):
        # TODO: blit score to score board
        arrayScore = []

    def moleGoUp(self):
        nbPixel = 0
        nbPixelBackUp = 20
        a = pygame.time.get_ticks()
        self.drawMap()
        b = pygame.time.get_ticks()
        print (b - a)
        moleWhacked = false
        mole2Whacked = false

        #returns a random position
        initialPos = self.returnRandPosition()
        initialPos2 = self.returnRandPosition()

        positionHammer = ()

        while nbPixel < 50 :
            tickCounter = pygame.time.get_ticks() % 15
            if tickCounter == 0:
                nbPixel += 1
                nbPixelBackUp -= 1

            #gets position of mouse
            mousePos = pygame.mouse.get_pos()

            #blits the background block that the mole is supposed to go to
            blockAbovePos = (initialPos[1] * 50, initialPos[0] * 50 - 50)
            blockAbovePos2 = (initialPos2[1] * 50, initialPos2[0] * 50 - 50)

            #blits the mole at position (goes up by one pixel every 20 ticks)
            newPos = (initialPos[1] * 50, (initialPos[0]*50 - nbPixel))
            newPos2 = (initialPos2[1] * 50, (initialPos2[0]*50 - nbPixel))

            initPosToBlit = (initialPos[1] * 50, initialPos[0] * 50)
            initPosToBlit2 = (initialPos2[1] * 50, initialPos2[0] * 50)

            for event in pygame.event.get():
                mousePos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and self.moleClickDetection(mousePos, newPos, [initialPos[1]*50, initialPos[0]*50]):
                    moleWhacked = true
                    positionHammer = (mousePos[0] - 25, mousePos[1] - 25)
                    #nbPixel = 0
                    font = pygame.font.SysFont('Comic Sans MS', 20)
                    print('mole 1')
                    self.score = font.render(str(self.nbMoleHit), False, (0, 0, 0))

                if event.type == pygame.MOUSEBUTTONDOWN:
                    print([initialPos2[1]*50, initialPos2[0]*50], mousePos)

                if event.type == pygame.MOUSEBUTTONDOWN and self.moleClickDetection(mousePos, newPos, [initialPos2[1]*50, initialPos2[0]*50]):
                    mole2Whacked = true
                    positionHammer = (mousePos[0] - 25, mousePos[1] - 25)
                    #nbPixel = 0
                    print('mole 2')
                    font = pygame.font.SysFont('Comic Sans MS', 20)
                    self.score = font.render(str(self.nbMoleHit), False, (0, 0, 0))

                if nbPixelBackUp <= 0:
                    nbPixelBackUp = 20
                    self.drawMap()


            # counts how many ticks has passed
            self.blitBlocksAroundHammer(mousePos)

            if not moleWhacked:
                display_surf.blit(imageWall, blockAbovePos)
                display_surf.blit(imageTarger, newPos)
                display_surf.blit(imageWall, initPosToBlit)

            if not mole2Whacked:
                display_surf.blit(imageWall, blockAbovePos2)
                display_surf.blit(imageTarger, newPos2)
                display_surf.blit(imageWall, initPosToBlit2)

            #blits the background at the original position of the mole
            #display_surf.blit(imageWall,initPosToBlit)
            #display_surf.blit(imageWall, initPosToBlit2)

            #blits the hammer
            display_surf.blit(imagePlayer, mousePos)
            if moleWhacked or mole2Whacked:
                display_surf.blit(imageFinish, positionHammer)

            #blits the background over the mole
            if nbPixel == 50:
                display_surf.blit(imageWall, (initialPos[1]*50, initialPos[0]*50 - nbPixel))
                display_surf.blit(imageWall, (initialPos2[1]*50, initialPos2[0]*50 - nbPixel))

            display_surf.blit(self.score, (70, 20))

            pygame.display.update()

    def start_play(self):
        #TODO:
        finished = false
        self.start_Screen()
        while (not finished):
            self.moleGoUp()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = true



def clearImage():
    #path
    image2BCleared = Image.open("C:/Users/CIQBILLY/Desktop/Whack-A-Mole/boom.png")
    imageArray = numpy.array(image2BCleared)
    width, height = image2BCleared.size
    transparent = (255, 255, 255, 0)

    for i in range(0, width):
        for j in range(0, height):
            newDataItem = imageArray[i][j]
            #NOTE: for new image, specify color
            if tuple(newDataItem) == (255, 255, 255, 255):
                imageArray[i][j] = transparent
    dirpath = os.getcwd()
    im = Image.fromarray(imageArray)
    im.save("image_boom.png", "png")

mazeDisplayed = map()
mazeDisplayed.start_play()










