import pygame
import random

#nessecary starting stuff
pygame.init()

#screen
WIDTH, HEIGHT=900,600
screen=pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze game")
running=True

#timings
clock=pygame.time.Clock()
FPS=30
FPSScaling=30/FPS

#colours
RED=(255,0,0)
DARK_RED=(137,0,0)
ORANGE=(255,137,0)
DARK_ORANGE=(137,68,0)
YELLOW=(255,255,0)
DARK_YELLOW=(137,137,0)
GREEN=(0,230,15)
LIGHT_GREEN=(125,255,125)
DARK_GREEN=(0, 150, 0)
TEAL=(55,225,250)
DARK_TEAL=(0, 137, 137)
BLUE=(0,0,255)
DARK_BLUE=(0,0,170)
LIGHT_BLUE=(0,230,255)
PURPLE=(179,0,255)
DARK_PURPLE=(100, 0, 150)
MAGENTA=(255,0,255)
DARK_MAGENTA=(137,0,137)
WHITE=(255,255,255)
BLACK=(0,0,0)
GRAY=(177,177,177)
DARK_GRAY=(100,100,100)

#fonts/font sizes
fontType='freesansbold.ttf'
font15=pygame.font.Font(fontType, 15)
font20=pygame.font.Font(fontType, 20)
font25=pygame.font.Font(fontType, 25)
font30=pygame.font.Font(fontType, 30)
font37=pygame.font.Font(fontType, 37)
font40=pygame.font.Font(fontType, 40)
font200=pygame.font.Font(fontType, 200)

#helpful pushing text to screen function
def toScreen(words, font, colour, x, y):
    text=font.render(words, True, colour)
    textRect=text.get_rect()
    textRect.center=(x, y)
    screen.blit(text, textRect)
#versions to push more than 1 line
def toScreen2(words1, words2, font, colour, x, y):
    toScreen(words1, font, colour, x, y-font.get_height()//2)
    toScreen(words2, font, colour, x, y+font.get_height()//2)
def toScreen3(words1, words2, words3, font, colour, x, y):
    toScreen(words1, font, colour, x, y-font.get_height())
    toScreen(words2, font, colour, x, y)
    toScreen(words3, font, colour, x, y+font.get_height())


#sprite class
class Player(pygame.sprite.Sprite):
    #creating the sprite
    def __init__(self, x, y, width, height, speed):
        super().__init__()
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.xSpeed=0
        self.ySpeed=0
        self.speed=speed

        #drawing
        image=pygame.image.load("button.png")#will probably add a function to change the image for movement
        self.image=pygame.transform.scale(image, (width,height))
        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
    
    def update(self, xMovement, yMovement):
        self.x+=xMovement
        self.y+=yMovement
        self.rect=(self.x, self.y, self.width, self.height)
        

    def checkCollide(self, walls):
        playerRect=self.image.get_rect()
        playerRect.x=self.x
        playerRect.y=self.y
        knockback=4/FPSScaling
        for wall in walls:
            if playerRect.colliderect(wall.rect):#pygame.Rect.colliderect(self.get_rect(), wall.getRect()):
                if (wall.isHorizontal):
                    if rightPosition(wall.x, wall.width, self.x, self.xSpeed):
                        if self.y>wall.y:
                            self.y+=knockback
                        else:
                            self.y-=knockback
                    else:
                        if self.x>wall.x:
                            self.x+=knockback
                        else:
                            self.x-=knockback
                #vertical paddles
                else:
                    if rightPosition(wall.y, wall.length, self.y, self.ySpeed):
                        if self.x>wall.x:
                            self.x+=knockback
                        else:
                            self.x-=knockback
                    else:
                        if self.y>wall.y:
                            self.y+=knockback
                        else:
                            self.y-=knockback        

#wall class
class Wall():
    #creating the walls
    def __init__(self, x, y, width, length, colour=BLACK):
        self.x=x
        self.y=y
        self.width=width
        self.length=length
        self.colour=colour
        self.isHorizontal=width!=5

        #drawing
        self.rect=pygame.Rect(x, y, width, length)
        self.wall=pygame.draw.rect(screen, colour, self.rect)

    #drawing to the screen
    def draw(self):
        self.rect=pygame.Rect(self.x, self.y, self.width, self.length)
        self.wall=pygame.draw.rect(screen, self.colour, self.rect)

#button class
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.hoveredOver=False

        image=pygame.image.load("button.png")
        self.image=pygame.transform.scale(image, (width, height))
        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y

    def update(self):
        #checking if te mouse is hovered over it
        mouseX, mouseY=pygame.mouse.get_pos()
        if mouseX>self.x and mouseX<self.x+self.width and mouseY>self.y and mouseY<self.y+self.height:
            image=pygame.image.load("buttonPressed.png")
            self.hoveredOver=True
            #checking if it got pressed
        else:
            image=pygame.image.load("button.png")
            self.hoveredOver=False
        self.image=pygame.transform.scale(image, (self.width, self.height))

#trailing ball class
class Ball():
    def __init__(self, x, y, colour, radius):
        self.x=x
        self.y=y
        self.colour=colour
        self.radius=radius

        self.ball=pygame.draw.circle(screen, self.colour, (self.x, self.y), self.radius)
        self.ballRect=pygame.Rect(self.x, self.y, self.radius*2, self.radius*2)

    def update(self):
        self.radius-=0.01/FPSScaling

    def draw(self):
        self.ball=pygame.draw.circle(screen, self.colour, (self.x, self.y), self.radius)
        self.ballRect=pygame.Rect(self.x, self.y, self.radius*2, self.radius*2)

#pie!
class Pie(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.x=x
        self.y=y
        self.size=size
        image=pygame.image.load("pie.png")
        self.image=pygame.transform.scale(image, (size, size))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

#having the important stats and stuff for the playing in one class so it saves
class PlayingState:
    def __init__(self, maze):
        if maze==1:
            maxTime=60
            walls=createMaze()
            playerXPos=WIDTH//6+10
            playerSize=35
            pieYPos=HEIGHT-70
        elif maze==2:
            maxTime=75
            walls=createMaze2()
            playerXPos=WIDTH//6-25
            playerSize=25
            pieYPos=HEIGHT-90
        elif maze==3:
            maxTime=90
            walls=createMaze3()
            playerXPos=WIDTH//2-54
            playerSize=20
            pieYPos=HEIGHT-90
            
        self.trails=[]
        #creating the sprites
        self.player=Player(playerXPos, 10, playerSize, playerSize, 4)
        self.sprites=pygame.sprite.Group()
        self.pie=Pie(WIDTH//2+250, pieYPos, 50)
        self.sprites.add(self.pie)
        self.sprites.add(self.player)
        self.gameState="Intro"
        self.firstTime=False
        self.walls=walls
        self.maxTime=maxTime
        self.maze1Time=1000
        self.maze2Time=1000
        self.maze3Time=1000
        self.maze=maze
        self.time=0

    def updateTimers(self):
        if self.maze==1:
            self.maze1Time=self.time
        elif self.maze==2:
            self.maze2Time=self.time
        elif self.maze==3:
            self.maze3Time=self.time
        self.time=0

#checking that the ball has the right x/y coords
def rightPosition(wallPos, wallLength, playerPos, playerDirect):
    #Between the top and bottom of the paddle
    if playerPos+4>wallPos and playerPos-4<wallPos+wallLength:
        return True
    else:
        if (playerPos>wallPos+wallLength and playerDirect>0) or (playerPos<wallPos+wallLength and playerDirect<0):
            return True
        else:
            return False

#checking if the mouse over the button
def checkSpot(xPos, yPos, width, height, colour):
    #getting mouse positions
    mouseX, mouseY=pygame.mouse.get_pos()
    if (mouseX>xPos and mouseX<xPos+width) and (mouseY>yPos and mouseY<yPos+height):
        if colour%2==0:
            colour+=1
    elif colour%2==1:
        colour-=1
    #returning the colour
    return colour

#drawing the outline for the buttons
def drawOutlines(xPos, yPos, width, height):
    rect=(xPos, yPos, width, height)
    pygame.draw.rect(screen, BLACK, rect, 3)

#drawing the number buttons
def drawTextSquare(colours, colour, text, location):
    colour=checkSpot(location[0], location[1], location[2], location[3], colour)    
    pygame.draw.rect(screen, colours[colour], location)
    drawOutlines(location[0], location[1], location[2], location[3])
    toScreen(text, font37, BLACK, location[0]+location[2]//2, location[1]+location[3]/2)
    return colour

#creating the mazes' walls
def createMaze()-> list[Wall]:
    walls=[]
    widthV, heightH=5,5 
    
    #having a list of the possible x and y lines
    xList=[]
    yList=[]
    for i in range(0,12):
        xList.append(WIDTH//6-widthV+50*i)
        yList.append(25+50*i)
    
    colour=BLACK
    #if statement just so I can shrink it
    #horizontal walls starting at the top left
    if True:
        walls.append(Wall(xList[0], -20, 55, 5, colour))
        walls.append(Wall(xList[1], yList[0], 505, 5, colour))
        #new row
        walls.append(Wall(xList[2], yList[1], 255, 5, colour))
        walls.append(Wall(xList[8], yList[1], 55, 5, colour))
        #new row
        walls.append(Wall(xList[1], yList[2], 55, 5, colour))
        walls.append(Wall(xList[6], yList[2], 105, 5, colour))
        walls.append(Wall(xList[9], yList[2], 55, 5, colour))
        #new row
        walls.append(Wall(xList[2], yList[3], 55, 5, colour))
        walls.append(Wall(xList[4], yList[3], 155, 5, colour))
        walls.append(Wall(xList[10], yList[3], 55, 5, colour))
        #new row
        walls.append(Wall(xList[1], yList[4], 105, 5, colour))
        walls.append(Wall(xList[5], yList[4], 155, 5, colour))
        walls.append(Wall(xList[9], yList[4], 55, 5, colour))
        #new row
        walls.append(Wall(xList[2], yList[5], 105, 5, colour))
        walls.append(Wall(xList[9], yList[5], 105, 5, colour))
        #new row
        walls.append(Wall(xList[2], yList[6], 155, 5, colour))
        walls.append(Wall(xList[6], yList[6], 55, 5, colour))
        walls.append(Wall(xList[8], yList[6], 105, 5, colour))
        #new row
        walls.append(Wall(xList[1], yList[7], 55, 5, colour))
        walls.append(Wall(xList[3], yList[7], 155, 5, colour))
        walls.append(Wall(xList[7], yList[7], 55, 5, colour))
        walls.append(Wall(xList[9], yList[7], 55, 5, colour))
        #new row
        walls.append(Wall(xList[0], yList[8], 55, 5, colour))
        walls.append(Wall(xList[2], yList[8], 105, 5, colour))
        walls.append(Wall(xList[6], yList[8], 55, 5, colour))
        walls.append(Wall(xList[8], yList[8], 55, 5, colour))
        walls.append(Wall(xList[10], yList[8], 55, 5, colour))
        #new row
        walls.append(Wall(xList[5], yList[9], 55, 5, colour))
        walls.append(Wall(xList[9], yList[9], 105, 5, colour))
        #new row
        walls.append(Wall(xList[1], yList[10], 205, 5, colour))
        walls.append(Wall(xList[7], yList[10], 105, 5, colour))
        #walls.append(Wall(xList[11], yList[10], 205, 5, colour))
        #new row
        walls.append(Wall(xList[0], yList[11], 605, 5, colour))
        walls.append(Wall(xList[11], yList[10], 50, 5, colour))
    #veritcal walls
    if True:
        walls.append(Wall(xList[0], -20, 5, 600, colour))
        #new
        walls.append(Wall(xList[1], -20, 5, 145, colour))
        walls.append(Wall(xList[1], yList[3], 5, 200, colour))
        walls.append(Wall(xList[1], yList[8], 5, 50, colour))
        #new
        walls.append(Wall(xList[2], yList[5], 5, 50, colour))
        walls.append(Wall(xList[2], yList[7], 5, 100, colour))
        #new
        walls.append(Wall(xList[3], yList[2], 5, 100, colour))
        walls.append(Wall(xList[3], yList[9], 5, 50, colour))
        #new
        walls.append(Wall(xList[4], yList[1], 5, 50, colour))
        walls.append(Wall(xList[4], yList[3], 5, 100, colour))
        walls.append(Wall(xList[4], yList[8], 5, 100, colour))
        #new
        walls.append(Wall(xList[5], yList[2], 5, 50, colour))
        walls.append(Wall(xList[5], yList[5], 5, 50, colour))
        walls.append(Wall(xList[5], yList[7], 5, 150, colour))
        #new
        walls.append(Wall(xList[6], yList[5], 5, 100, colour))
        walls.append(Wall(xList[6], yList[9], 5, 100, colour))
        #new
        walls.append(Wall(xList[7], yList[0], 5, 50, colour))
        walls.append(Wall(xList[7], yList[2], 5, 50, colour))
        walls.append(Wall(xList[7], yList[4], 5, 50, colour))
        walls.append(Wall(xList[7], yList[6], 5, 150, colour))
        #new
        walls.append(Wall(xList[8], yList[1], 5, 50, colour))
        walls.append(Wall(xList[8], yList[3], 5, 200, colour))
        walls.append(Wall(xList[8], yList[8], 5, 100, colour))
        #new
        walls.append(Wall(xList[9], yList[0], 5, 50, colour))
        walls.append(Wall(xList[9], yList[2], 5, 150, colour))
        walls.append(Wall(xList[9], yList[7], 5, 50, colour))
        walls.append(Wall(xList[9], yList[9], 5, 50, colour))
        #new
        walls.append(Wall(xList[10], yList[1], 5, 50, colour))
        walls.append(Wall(xList[10], yList[10], 5, 50, colour))
        #new
        walls.append(Wall(xList[11], yList[0], 5, 505, colour))

    return walls

def createMaze2()->list[Wall]:
    walls=[]
    width=5
    gap=35
    colour=BLACK
    xList=[]
    yList=[]
    for i in range(0,16):
        xList.append(WIDTH//7-width+gap*i)
        yList.append(25+gap*i)
    
    #for i in range(0,16):
        #walls.append(Wall(xList[i], 25, 5, 525, BLACK))
        #walls.append(Wall(WIDTH//7, yList[i], 525, 5, BLACK))

    #horizontal
    if True:
        walls.append(Wall(xList[0], -20, gap*2+width, width, colour))
        walls.append(Wall(xList[1], yList[0], gap*14+width, width, colour))
        #new
        walls.append(Wall(xList[2], yList[1], gap*3+width, width, colour))
        walls.append(Wall(xList[7], yList[1], gap*3+width, width, colour))
        walls.append(Wall(xList[13], yList[1], gap*1+width, width, colour))
        #new
        walls.append(Wall(xList[3], yList[2], gap*3+width, width, colour))
        walls.append(Wall(xList[8], yList[2], gap*3+width, width, colour))
        walls.append(Wall(xList[14], yList[2], gap*1+width, width, colour))
        #new
        walls.append(Wall(xList[1], yList[3], gap*5+width, width, colour))
        walls.append(Wall(xList[7], yList[3], gap*5+width, width, colour))
        walls.append(Wall(xList[13], yList[3], gap*1+width, width, colour))
        #new
        walls.append(Wall(xList[3], yList[4], gap*4+width, width, colour))
        walls.append(Wall(xList[8], yList[4], gap*5+width, width, colour))
        walls.append(Wall(xList[14], yList[4], gap*1+width, width, colour))
        #new
        walls.append(Wall(xList[4], yList[5], gap*4+width, width, colour))
        walls.append(Wall(xList[9], yList[5], gap*5+width, width, colour))
        #new
        walls.append(Wall(xList[4], yList[6], gap*11+width, width, colour))
        #new
        walls.append(Wall(xList[0], yList[7], gap*2+width, width, colour))
        walls.append(Wall(xList[6], yList[7], gap*8+width, width, colour))
        #new
        walls.append(Wall(xList[1], yList[8], gap*2+width, width, colour))
        walls.append(Wall(xList[7], yList[8], gap*8+width, width, colour))
        #new
        walls.append(Wall(xList[2], yList[9], gap*2+width, width, colour))
        walls.append(Wall(xList[7], yList[9], gap*7+width, width, colour))
        #new
        walls.append(Wall(xList[6], yList[10], gap*5+width, width, colour))
        #new
        walls.append(Wall(xList[7], yList[11], gap*3+width, width, colour))
        #new
        walls.append(Wall(xList[6], yList[12], gap*3+width, width, colour))
        #new
        walls.append(Wall(xList[5], yList[13], gap*3+width, width, colour))
        walls.append(Wall(xList[13], yList[13], gap*2+width, width, colour))
        #new
        walls.append(Wall(xList[4], yList[14], gap*3+width, width, colour))
        walls.append(Wall(xList[11], yList[14], gap*3+width, width, colour))
        #new
        walls.append(Wall(xList[0], yList[15], gap*19+width, width, colour))
        walls.append(Wall(xList[15], yList[14], gap*4+width, width, colour))

    #vertical
    if True:
        walls.append(Wall(xList[1], -20, width, 50, colour))
        walls.append(Wall(xList[0], -20, width, gap*15+width+45, colour))
        #new
        walls.append(Wall(xList[1], yList[0], width, gap*2+width, colour))
        walls.append(Wall(xList[1], yList[3], width, gap*3+width, colour))
        walls.append(Wall(xList[1], yList[8], width, gap*6+width, colour))
        #new
        walls.append(Wall(xList[2], yList[1], width, gap*2+width, colour))
        walls.append(Wall(xList[2], yList[4], width, gap*3+width, colour))
        walls.append(Wall(xList[2], yList[9], width, gap*5+width, colour))
        #new
        walls.append(Wall(xList[3], yList[4], width, gap*4+width, colour))
        walls.append(Wall(xList[3], yList[10], width, gap*5+width, colour))
        #new
        walls.append(Wall(xList[4], yList[5], width, gap*9+width, colour))
        #new
        walls.append(Wall(xList[5], yList[7], width, gap*6+width, colour))
        #new
        walls.append(Wall(xList[6], yList[0], width, gap*3+width, colour))
        walls.append(Wall(xList[6], yList[7], width, gap*5+width, colour))
        #new
        walls.append(Wall(xList[7], yList[1], width, gap*3+width, colour))
        #new
        walls.append(Wall(xList[8], yList[4], width, gap*1+width, colour))
        walls.append(Wall(xList[8], yList[13], width, gap*2+width, colour))
        #new
        walls.append(Wall(xList[9], yList[12], width, gap*2+width, colour))
        #new
        walls.append(Wall(xList[10], yList[11], width, gap*4+width, colour))
        #new
        walls.append(Wall(xList[11], yList[0], width, gap*2+width, colour))
        walls.append(Wall(xList[11], yList[10], width, gap*4+width, colour))
        #new
        walls.append(Wall(xList[12], yList[0], width, gap*3+width, colour))
        walls.append(Wall(xList[12], yList[9], width, gap*5+width, colour))
        #new
        walls.append(Wall(xList[13], yList[1], width, gap*3+width, colour))
        walls.append(Wall(xList[13], yList[10], width, gap*3+width, colour))
        #new
        walls.append(Wall(xList[14], yList[4], width, gap*1+width, colour))
        walls.append(Wall(xList[14], yList[9], width, gap*3+width, colour))
        walls.append(Wall(xList[14], yList[14], width, gap*1+width, colour))
        #new
        walls.append(Wall(xList[15], yList[0], width, gap*14+width, colour))

    return walls

def createMaze3()->list[Wall]:
    walls=[]
    width=5
    gap=33
    colour=BLACK
    xList=[]
    yList=[]
    for i in range(0,18):
        xList.append(WIDTH//7-width+gap*i)
        yList.append(25+gap*i)
    
   # for i in range(0,18):
        #walls.append(Wall(xList[i], 25, 5, 560, BLACK))
        #walls.append(Wall(WIDTH//7, yList[i], 560, 5, BLACK))

    #horizontal
    if True:
        walls.append(Wall(xList[0], yList[0], gap*8+width, width, colour))
        walls.append(Wall(xList[9], yList[0], gap*8+width, width, colour))
        #new
        walls.append(Wall(xList[0], yList[1], gap*1+width, width, colour))
        walls.append(Wall(xList[4], yList[1], gap*2+width, width, colour))
        walls.append(Wall(xList[10], yList[1], gap*1+width, width, colour))
        walls.append(Wall(xList[15], yList[1], gap*1+width, width, colour))
        #new
        walls.append(Wall(xList[0], yList[2], gap*1+width, width, colour))
        walls.append(Wall(xList[4], yList[2], gap*1+width, width, colour))
        walls.append(Wall(xList[7], yList[2], gap*1+width, width, colour))
        walls.append(Wall(xList[9], yList[2], gap*4+width, width, colour))
        walls.append(Wall(xList[14], yList[2], gap*2+width, width, colour))
        #new
        walls.append(Wall(xList[2], yList[3], gap*2+width, width, colour))
        walls.append(Wall(xList[5], yList[3], gap*2+width, width, colour))
        walls.append(Wall(xList[9], yList[3], gap*1+width, width, colour))
        walls.append(Wall(xList[11], yList[3], gap*1+width, width, colour))
        walls.append(Wall(xList[13], yList[3], gap*1+width, width, colour))
        #new
        walls.append(Wall(xList[1], yList[4], gap*2+width, width, colour))
        walls.append(Wall(xList[5], yList[4], gap*1+width, width, colour))
        walls.append(Wall(xList[7], yList[4], gap*2+width, width, colour))
        #new
        walls.append(Wall(xList[3], yList[5], gap*1+width, width, colour))
        walls.append(Wall(xList[7], yList[5], gap*1+width, width, colour))
        walls.append(Wall(xList[9], yList[5], gap*1+width, width, colour))
        walls.append(Wall(xList[13], yList[5], gap*2+width, width, colour))
        walls.append(Wall(xList[16], yList[5], gap*1+width, width, colour))
        #new
        walls.append(Wall(xList[4], yList[6], gap*2+width, width, colour))
        walls.append(Wall(xList[11], yList[6], gap*2+width, width, colour))
        #new
        walls.append(Wall(xList[0], yList[7], gap*1+width, width, colour))
        walls.append(Wall(xList[2], yList[7], gap*1+width, width, colour))
        walls.append(Wall(xList[7], yList[7], gap*1+width, width, colour))
        walls.append(Wall(xList[10], yList[7], gap*4+width, width, colour))
        walls.append(Wall(xList[15], yList[7], gap*2+width, width, colour))
        #new
        walls.append(Wall(xList[0], yList[8], gap*1+width, width, colour))
        walls.append(Wall(xList[4], yList[8], gap*1+width, width, colour))
        walls.append(Wall(xList[8], yList[8], gap*2+width, width, colour))
        walls.append(Wall(xList[11], yList[8], gap*2+width, width, colour))
        walls.append(Wall(xList[14], yList[8], gap*1+width, width, colour))
        walls.append(Wall(xList[16], yList[8], gap*1+width, width, colour))
        #new
        walls.append(Wall(xList[1], yList[9], gap*3+width, width, colour))
        walls.append(Wall(xList[5], yList[9], gap*1+width, width, colour))
        walls.append(Wall(xList[7], yList[9], gap*5+width, width, colour))
        walls.append(Wall(xList[13], yList[9], gap*2+width, width, colour))
        #new
        walls.append(Wall(xList[0], yList[10], gap*1+width, width, colour))
        walls.append(Wall(xList[2], yList[10], gap*1+width, width, colour))
        walls.append(Wall(xList[6], yList[10], gap*2+width, width, colour))
        walls.append(Wall(xList[9], yList[10], gap*1+width, width, colour))
        walls.append(Wall(xList[13], yList[10], gap*2+width, width, colour))
        #new
        walls.append(Wall(xList[0], yList[11], gap*3+width, width, colour))
        walls.append(Wall(xList[6], yList[11], gap*4+width, width, colour))
        walls.append(Wall(xList[12], yList[11], gap*4+width, width, colour))
        #new
        walls.append(Wall(xList[1], yList[12], gap*2+width, width, colour))
        walls.append(Wall(xList[5], yList[12], gap*4+width, width, colour))
        walls.append(Wall(xList[10], yList[12], gap*2+width, width, colour))
        #new
        walls.append(Wall(xList[3], yList[13], gap*3+width, width, colour))
        walls.append(Wall(xList[7], yList[13], gap*1+width, width, colour))
        walls.append(Wall(xList[9], yList[13], gap*2+width, width, colour))
        walls.append(Wall(xList[14], yList[13], gap*1+width, width, colour))
        #new
        walls.append(Wall(xList[0], yList[14], gap*1+width, width, colour))
        walls.append(Wall(xList[2], yList[14], gap*4+width, width, colour))
        walls.append(Wall(xList[10], yList[14], gap*1+width, width, colour))
        walls.append(Wall(xList[12], yList[14], gap*1+width, width, colour))
        walls.append(Wall(xList[16], yList[14], gap*1+width, width, colour))
        #new
        walls.append(Wall(xList[1], yList[15], gap*2+width, width, colour))
        walls.append(Wall(xList[5], yList[15], gap*11+width, width, colour))
        #new
        walls.append(Wall(xList[1], yList[16], gap*2+width, width, colour))
        walls.append(Wall(xList[4], yList[16], gap*2+width, width, colour))
        walls.append(Wall(xList[10], yList[16], gap*2+width, width, colour))
        walls.append(Wall(xList[13], yList[16], gap*1+width, width, colour))
        walls.append(Wall(xList[15], yList[16], gap*1+width, width, colour))
        #new
        walls.append(Wall(xList[0], yList[17], gap*8+width, width, colour))
        walls.append(Wall(xList[9], yList[17], gap*8+width, width, colour))

    if True:
        walls.append(Wall(xList[0], yList[0], width, gap*17+width, colour))
        #new
        walls.append(Wall(xList[1], yList[3], width, gap*1+width, colour))
        walls.append(Wall(xList[1], yList[5], width, gap*2+width, colour))
        walls.append(Wall(xList[1], yList[11], width, gap*1+width, colour))
        walls.append(Wall(xList[1], yList[13], width, gap*1+width, colour))
        #new
        walls.append(Wall(xList[2], yList[0], width, gap*2+width, colour))
        walls.append(Wall(xList[2], yList[4], width, gap*1+width, colour))
        walls.append(Wall(xList[2], yList[6], width, gap*3+width, colour))
        walls.append(Wall(xList[2], yList[13], width, gap*1+width, colour))
        #new
        walls.append(Wall(xList[3], yList[1], width, gap*7+width, colour))
        walls.append(Wall(xList[3], yList[10], width, gap*1+width, colour))
        walls.append(Wall(xList[3], yList[14], width, gap*2+width, colour))
        #new
        walls.append(Wall(xList[4], yList[1], width, gap*2+width, colour))
        walls.append(Wall(xList[4], yList[4], width, gap*1+width, colour))
        walls.append(Wall(xList[4], yList[7], width, gap*1+width, colour))
        walls.append(Wall(xList[4], yList[9], width, gap*5+width, colour))
        walls.append(Wall(xList[4], yList[15], width, gap*1+width, colour))
        #new
        walls.append(Wall(xList[5], yList[3], width, gap*1+width, colour))
        walls.append(Wall(xList[5], yList[5], width, gap*6+width, colour))
        #new
        walls.append(Wall(xList[6], yList[1], width, gap*1+width, colour))
        walls.append(Wall(xList[6], yList[4], width, gap*3+width, colour))
        walls.append(Wall(xList[6], yList[8], width, gap*2+width, colour))
        walls.append(Wall(xList[6], yList[12], width, gap*1+width, colour))
        walls.append(Wall(xList[6], yList[15], width, gap*1+width, colour))
        #new
        walls.append(Wall(xList[7], yList[0], width, gap*4+width, colour))
        walls.append(Wall(xList[7], yList[5], width, gap*3+width, colour))
        walls.append(Wall(xList[7], yList[10], width, gap*1+width, colour))
        walls.append(Wall(xList[7], yList[13], width, gap*4+width, colour))
        #new
        walls.append(Wall(xList[8], yList[0], width, gap*1+width, colour))
        walls.append(Wall(xList[8], yList[2], width, gap*1+width, colour))
        walls.append(Wall(xList[8], yList[6], width, gap*3+width, colour))
        walls.append(Wall(xList[8], yList[13], width, gap*1+width, colour))
        walls.append(Wall(xList[8], yList[16], width, gap*1+width, colour))
        #new
        walls.append(Wall(xList[9], yList[0], width, gap*1+width, colour))
        walls.append(Wall(xList[9], yList[3], width, gap*4+width, colour))
        walls.append(Wall(xList[9], yList[12], width, gap*2+width, colour))
        walls.append(Wall(xList[9], yList[15], width, gap*1+width, colour))
        #new
        walls.append(Wall(xList[10], yList[3], width, gap*1+width, colour))
        walls.append(Wall(xList[10], yList[5], width, gap*2+width, colour))
        walls.append(Wall(xList[10], yList[10], width, gap*1+width, colour))
        #new
        walls.append(Wall(xList[11], yList[1], width, gap*1+width, colour))
        walls.append(Wall(xList[11], yList[3], width, gap*2+width, colour))
        walls.append(Wall(xList[11], yList[8], width, gap*6+width, colour))
        #new
        walls.append(Wall(xList[12], yList[0], width, gap*5+width, colour))
        walls.append(Wall(xList[12], yList[10], width, gap*1+width, colour))
        walls.append(Wall(xList[12], yList[12], width, gap*2+width, colour))
        walls.append(Wall(xList[12], yList[16], width, gap*1+width, colour))
        #new
        walls.append(Wall(xList[13], yList[1], width, gap*1+width, colour))
        walls.append(Wall(xList[13], yList[3], width, gap*1+width, colour))
        walls.append(Wall(xList[13], yList[5], width, gap*2+width, colour))
        walls.append(Wall(xList[13], yList[8], width, gap*1+width, colour))
        walls.append(Wall(xList[13], yList[12], width, gap*2+width, colour))
        walls.append(Wall(xList[13], yList[15], width, gap*1+width, colour))
        #new
        walls.append(Wall(xList[14], yList[1], width, gap*4+width, colour))
        walls.append(Wall(xList[14], yList[6], width, gap*1+width, colour))
        walls.append(Wall(xList[14], yList[10], width, gap*2+width, colour))
        walls.append(Wall(xList[14], yList[13], width, gap*2+width, colour))
        #new
        walls.append(Wall(xList[15], yList[2], width, gap*1+width, colour))
        walls.append(Wall(xList[15], yList[4], width, gap*1+width, colour))
        walls.append(Wall(xList[15], yList[6], width, gap*3+width, colour))
        walls.append(Wall(xList[15], yList[11], width, gap*2+width, colour))
        walls.append(Wall(xList[15], yList[14], width, gap*1+width, colour))
        #new
        walls.append(Wall(xList[16], yList[1], width, gap*1+width, colour))
        walls.append(Wall(xList[16], yList[3], width, gap*3+width, colour))
        walls.append(Wall(xList[16], yList[9], width, gap*2+width, colour))
        walls.append(Wall(xList[16], yList[12], width, gap*2+width, colour))
        walls.append(Wall(xList[16], yList[15], width, gap*1+width, colour))
        #new
        walls.append(Wall(xList[17], yList[0], width, gap*17+width, colour))


    return walls
        
#different displaying functions
def intro(gameState):
    global running
    #putting into groups
    button=Button(WIDTH//2-75, HEIGHT//2+75, 150, 150)
    introSprites=pygame.sprite.Group()
    introSprites.add(button)

    #screen
    screen.fill(BLUE)
    #text
    toScreen("Welcome to the a-maze-ing maze game!", font40, BLACK, WIDTH//2, 100)
    toScreen3("Try to find your way out of the maze as fast as posible", "You only have 60 seconds, then 75 seconds, then 90 seconds to escape for the 3 mazes so move quickly!", "Random silly background story stuff", font20, BLACK, WIDTH//2, HEIGHT//2)

    #button
    button.update()
    introSprites.draw(screen)

    #checking to allow the game to end
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            print("Pressed")
            if button.hoveredOver:
                screen.fill(GREEN)
                gameState="Playing"
    #end
    return gameState

#choosing the maze difficulty
def choose(maze):
    global running
    screen.fill(DARK_TEAL)
    toScreen("Please choose which level of difficulty you want.", font37, BLACK, WIDTH//2, 100)
    toScreen3("1. Easy, 1 minute to escape a maze", "2. Medium, 1:30 to escape a bigger maze", "3. 2 minutes to escape a hard maze", font30, BLACK, WIDTH//2, HEIGHT//2-75)

    #creating buttons
    colours=[RED, DARK_RED, ORANGE, DARK_ORANGE, YELLOW, DARK_YELLOW]
    one, two, three=0, 2, 4
    width, height=200,200
    oneButton=(100, HEIGHT//2+50, width, height)
    twoButton=(WIDTH//2-width//2, HEIGHT//2+50, width, height)
    threeButton=(WIDTH-100-width, HEIGHT//2+50, width, height)
    one=drawTextSquare(colours, one, "1.", oneButton)
    two=drawTextSquare(colours, two, "2.", twoButton)
    three=drawTextSquare(colours, three, "3.", threeButton)

    #checking for clicks and stopping
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            print("pressed!!!!")
            if one==1:
                maze=1
            elif two==3:
                maze=2
            elif three==5:
                maze=3
    
    return maze
    
#main normal playing scene
def playing(playingStuff: PlayingState):
    
    sprites=pygame.sprite.Group()
    sprites.add(playingStuff.pie)
    sprites.add(playingStuff.player)
    
    global running

    screen.fill((0,255,0,50))
    #checking to allow the game to end
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            print("Pressed")
            playingStuff.gameState="End"
        #moving
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                playingStuff.player.ySpeed-=playingStuff.player.speed
            elif event.key==pygame.K_DOWN:
                playingStuff.player.ySpeed+=playingStuff.player.speed
            elif event.key==pygame.K_LEFT:
                playingStuff.player.xSpeed-=playingStuff.player.speed
            elif event.key==pygame.K_RIGHT:
                playingStuff.player.xSpeed+=playingStuff.player.speed

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_UP or event.key==pygame.K_DOWN:
                playingStuff.player.ySpeed=0
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playingStuff.player.xSpeed=0

    
    #printing the time
    toScreen("Time: "+str(round(playingStuff.time)), font30, BLACK, 60, 20)

    #drawing tracking balls
    #trails.append(Ball(player.x+player.width//2, player.y+player.height//2, BLACK, 5))
    for ball in playingStuff.trails:
        ball.update()
        ball.draw()

    #drawing the player
    playingStuff.player.checkCollide(playingStuff.walls)
    playingStuff.player.update(playingStuff.player.xSpeed, playingStuff.player.ySpeed)
    sprites.draw(screen)
    
    #getting the maze
    for wall in playingStuff.walls:
        wall.draw()
    
    #stopping
    #losing after 60 seconds
    if playingStuff.time>playingStuff.maxTime:
        playingStuff.gameState="Loss"
    #winning
    elif playingStuff.player.x>WIDTH//2+250:
        if playingStuff.maze!=3:
            playingStuff.maze+=1
            playingStuff=PlayingState(playingStuff.maze)
            playingStuff.gameState="Playing"
            playingStuff.updateTimers()
        elif playingStuff.maze==3:
            playingStuff.gameState="Won"
    
    return playingStuff

def won(gameState, stats: PlayingState):
    global running

    screen.fill(DARK_MAGENTA)
    toScreen("Yay! You won!", font40, BLUE, WIDTH//2, 50)
    toScreen("It only took you "+str(round(stats.time))+" seconds to escape.", font20, GREEN, WIDTH//2, 100)
    
    #getting the game to be able to end
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            print("Pressed")
            gameState="End"

    return gameState

def loss(gameState):
    global running
    screen.fill(DARK_RED)
    toScreen("Aw, you lost.", font40, BLACK, WIDTH//2, 50)

    #getting the game to be able to end
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            print("Pressed")
            gameState="End"

    return gameState

#main function
def main():
    
    #stuff
    global running
    maze=1
    playingStuff=PlayingState(maze)


    #having the game actually run
    while running:
        if playingStuff.gameState=="Intro":
            playingStuff.gameState=intro(playingStuff.gameState)

        elif playingStuff.gameState=="Playing":
                
            playingStuff=playing(playingStuff)
            playingStuff.time+=1/FPS
        elif playingStuff.gameState=="Won":
            playingStuff.gameState=won(playingStuff)

        elif playingStuff.gameState=="Loss":
            playingStuff.gameState=loss(playingStuff.gameState, playingStuff)
        else:
            running=False

        #doing mandatory stuff
        clock.tick(FPS)
        pygame.display.flip()
        



#stuff
if __name__=="__main__":
    main()
    pygame.quit()
    