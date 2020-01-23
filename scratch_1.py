import sys
import pygame
pygame.init()
import random
import numpy
from PIL import Image
import os


print(pygame.ver)
pygame.font.init()

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
        self.gameOver = False
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
            return True
        else:
            return False

    def start_Screen(self):
        quitScreen = False
        display_surf.blit(startScreen, (0,0))
        pygame.display.update()
        while(not quitScreen):
            for event in pygame.event.get():
                #TODO: get mouse pos
                #TODO: check if inside
                posMouse = pygame.mouse.get_pos()

                if ((event.type == pygame.MOUSEBUTTONDOWN)
                    and (self.checkMouseInside(111,380,250,300, posMouse))):
                    quitScreen = True
                    self.diff = difficulty.Easy
                elif((event.type == pygame.MOUSEBUTTONDOWN)
                    and (self.checkMouseInside(111,380,322,366, posMouse))):
                    self.diff = difficulty.Hard
                    quitScreen = True

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
        #NOTE: for debugging
        #print('upper : ', verticalPosUpperLimit, 'lower : ', verticalLowerLimit)

        #up to 50 pixel to the right of the position of mole
        horizontalLimitLeft = posMole[0]
        horizontalLimitRight = posMole[0] + 50
        #NOTE: for debugging
        #print('upper : ', horizontalLimitLeft, 'lower : ', horizontalLimitRight)

        inVerticalRange = (posMouse[1] >= verticalPosUpperLimit) and (posMouse[1] <= verticalLowerLimit)
        #NOTE: for debugging
        #print(posMouse[1], verticalPosUpperLimit, posMouse[0], verticalLowerLimit)
        
        inHorizontalRange = (posMouse[0] >= horizontalLimitLeft) and (posMouse[0] <= horizontalLimitRight)
        if (inVerticalRange and inHorizontalRange):
            self.nbMoleHit += 1
        return (inVerticalRange and inHorizontalRange)

    def blitMole(self, initPosToBlit, newPos, blockAbovePos):
        display_surf.blit(imageWall, blockAbovePos)
        display_surf.blit(imageTarger, newPos)
        display_surf.blit(imageWall, initPosToBlit)

    def blitScore(self):
        font = pygame.font.SysFont('Comic Sans MS', 20)
        self.score = font.render(str(self.nbMoleHit), False, (0, 0, 0))

    def moleGoUp(self):
        posMolePixels = 0
        countDownTillDrawMap = 20
        a = pygame.time.get_ticks()
        self.drawMap()
        b = pygame.time.get_ticks()
        print (b - a)
        moleWhacked = False

        #returns a random position
        initialPos = self.returnRandPosition()
        positionHammer = ()

        while posMolePixels < 50 :
            # the mole will go up by 1 pixel everytime moleSpeedTickCounter reaches a multiple of pygame.time.get_ticks() % self.diff
            moleSpeedTickCounter = pygame.time.get_ticks() % self.diff
            if moleSpeedTickCounter == 0:
                posMolePixels += 1
                countDownTillDrawMap -= 1

            #gets position of mouse
            mousePos = pygame.mouse.get_pos()

            #blits the background block that the mole is supposed to go to
            blockAbovePos = (initialPos[1] * 50, initialPos[0] * 50 - 50)

            #blits the mole at position (goes up by one pixel every 20 ticks)
            newPos = (initialPos[1] * 50, (initialPos[0]*50 - posMolePixels))

            initPosToBlit = (initialPos[1] * 50, initialPos[0] * 50)

            for event in pygame.event.get():
                mousePos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    sys.exit()
                # detect if mole is whacked
                if event.type == pygame.MOUSEBUTTONDOWN and self.moleClickDetection(mousePos, newPos, [initialPos[1]*50, initialPos[0]*50]):
                    moleWhacked = True
                    # Assign the position of the hammer for 
                    positionHammer = (mousePos[0] - 25, mousePos[1] - 25)
                    # Blits the score
                    self.blitScore()
                if countDownTillDrawMap <= 0:
                    # Redraws the whole map when countDownTillDrawMap goes down to 20
                    countDownTillDrawMap = 20
                    self.drawMap()

            # counts how many ticks has passed
            self.blitBlocksAroundHammer(mousePos)
            if not moleWhacked:
                self.blitMole(initPosToBlit, newPos, blockAbovePos)
            #blits the background at the original position of the mole
            display_surf.blit(imageWall,initPosToBlit)
            #blits the hammer
            display_surf.blit(imagePlayer, mousePos)
            if moleWhacked:
                display_surf.blit(imageFinish, positionHammer)

            #blits the background over the mole
            if posMolePixels == 50:
                display_surf.blit(imageWall, (initialPos[1]*50, initialPos[0]*50 - posMolePixels))
            display_surf.blit(self.score, (70, 20))
            pygame.display.update()

    def start_play(self):
        finished = False
        self.start_Screen()
        while (not finished):
            self.moleGoUp()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True


def clearImage(path : str):
    #path
    image2BCleared = Image.open(path)
    imageArray = numpy.array(image2BCleared)
    width, height = image2BCleared.size
    transparent = (255, 255, 255, 0)

    for i in range(0, width):
        for j in range(0, height):
            newDataItem = imageArray[i][j]
            #NOTE: for new image, specify color
            if tuple(newDataItem) == (255, 255, 255, 255):
                imageArray[i][j] = transparent
    im = Image.fromarray(imageArray)
    im.save("image_boom.png", "png")

mazeDisplayed = map()
mazeDisplayed.start_play()