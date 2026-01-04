import pygame
import asyncio

# pylint: disable=no-member

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
        image=pygame.image.load("ufo.png")
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
        
        #checking all of the walls
        for wall in walls:
            if playerRect.colliderect(wall.rect):
                #horizontal walls
                if (wall.isHorizontal):
                    if rightPosition(wall.x, wall.width, self.x, self.xSpeed):
                        if self.y+self.height//2>wall.y+2.5:
                            self.y+=knockback*FPSScaling
                        else:
                            self.y-=knockback*FPSScaling
                    else:
                        if self.x+self.width//2>wall.x+2.5:
                            self.x+=knockback*FPSScaling
                        else:
                            self.x-=knockback*FPSScaling
                #vertical walls
                else:
                    if rightPosition(wall.y, wall.length, self.y, self.ySpeed):
                        if self.x+self.width//2>wall.x+2.5:
                            self.x+=knockback*FPSScaling
                        else:
                            self.x-=knockback*FPSScaling
                    else:
                        print("hi")
                        if self.y+self.height//2>wall.y+2.5:
                            self.y+=knockback*FPSScaling
                        else:
                            self.y-=knockback*FPSScaling
                #break

    def teleport(self, teleporters):
        rect=self.image.get_rect()
        rect.x=self.x
        rect.y=self.y
        
        for teleporterHit in teleporters:
            if rect.colliderect(teleporterHit.rect):
                for teleportDestination in teleporters:
                    if teleportDestination.number==teleporterHit.partner:
                        self.x=teleportDestination.x
                        self.y=teleportDestination.y


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
        self.radius-=0.005/FPSScaling

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

#having there be a fog so it is harder to see the maze
class Fog(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        x+=WIDTH
        y+=HEIGHT
        self.x=x
        self.y=y
        image=pygame.image.load("fog.png").convert_alpha()
        self.image=pygame.transform.scale(image, (WIDTH*2, HEIGHT*2))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

    def move(self, x, y):
        self.rect.x=x
        self.rect.y=y

#having eleporters around the map
class Teleporter(pygame.sprite.Sprite):
    def __init__(self, x, y, partner, number, width, height):
        super().__init__()
        self.x=x
        self.y=y
        self.partner=partner
        self.number=number
        image=pygame.image.load("button.png")
        self.image=pygame.transform.scale(image, (width, height))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

#having the important stats and stuff for the playing in one class so it saves
class PlayingState:
    def __init__(self, maze):
        #dealing with stuff when the maze changes
        pieXPos=WIDTH//2+250
        maxTime=60
        walls=createMaze()
        playerXPos=WIDTH//6+10
        playerSize=30
        pieYPos=HEIGHT-70
        
        
        self.trails=[]
        #creating the sprites
        self.player=Player(playerXPos, 10, playerSize, playerSize, 4)
        self.sprites=pygame.sprite.Group()
        self.pie=Pie(pieXPos, pieYPos, 50)
        

        #dealing with other stuff
        self.gameState="Intro"
        self.walls=walls
        self.maxTime=maxTime
        self.maze=maze
        self.time=0
        #stat stuff
        self.maze1Time=1000
        self.maze2Time=1000
        self.maze3Time=1000
        self.maze1Fastest=1000
        self.maze2Fastest=1000
        self.maze3Fastest=1000
        self.fastest=1000
    
    def makeLevelsWork(self, level):
        if level==3 or level==4:
            self.fog=Fog(self.player.x, 10)
        if level==2 or level==3:
            self.teleporters=getMaze1Teleporters()
        self.level=level

    def changeMaze(self, maze):
        #dealing with stuff when the maze changes
        pieXPos=WIDTH//2+250
        if maze==1:
            maxTime=60
            walls=createMaze()
            playerXPos=WIDTH//6+10
            playerSize=33
            pieYPos=HEIGHT-70
            self.teleporters=getMaze1Teleporters()
        elif maze==2:
            maxTime=120
            walls=createMaze2()
            playerXPos=WIDTH//6-25
            playerSize=23
            pieYPos=HEIGHT-90
            self.teleporters=getMaze2Teleporters()
        elif maze==3:
            maxTime=90
            walls=createMaze3()
            playerXPos=WIDTH//2-34
            playerSize=21
            pieYPos=HEIGHT-45
            pieXPos=WIDTH//2-47
            self.teleporters=getMaze3Teleporters()
            
        self.trails=[]
        #creating the sprites
        self.player=Player(playerXPos, 10, playerSize, playerSize, 4)
        self.sprites=pygame.sprite.Group()
        self.pie=Pie(pieXPos, pieYPos, 50)
        self.sprites.add(self.pie)
        self.sprites.add(self.player)

        #dealing with other stuff
        self.gameState="Won"
        self.walls=walls
        self.maxTime=maxTime
        self.maze=maze
        self.time=0
        
    def updateTimers(self):
        if self.maze==1:
            self.maze1Time=round(self.time*100)/100
            self.time=0
            #update self records
            if self.maze1Time<self.maze1Fastest:
                self.maze1Fastest=round(self.maze1Time*100)/100
        elif self.maze==2:
            self.maze2Time=round(self.time*100)/100
            self.time=0
            #update self records
            if self.maze2Time<self.maze2Fastest:
                self.maze2Fastest=round(self.maze2Time*100)/100
        elif self.maze==3:
            self.maze3Time=round(self.time*100)/100
            #update self records
            if self.maze3Time<self.maze3Fastest:
                self.maze3Fastest=round(self.maze3Time*100)/100
            replaceTimes(self)        

#getting from and pushing to files
def getFromFile(fileName):
    with open(fileName, 'r') as file:
        timeAndName=file.read()
    return timeAndName

#push name to file
def pushToFile(words, fileName):
    with open(fileName, 'w') as file:
        file.write(words)

#check if the time is fastest
def checkIfFastest(time, fileName):
    #checking which is fastest
    if time<float(getFromFile(fileName)):
        newFastestTime=True
    else:
        newFastestTime=False

    return newFastestTime

#replacing the fastest time
def replaceTimes(stats:PlayingState):
    if checkIfFastest(stats.maze1Time, "maze1TopTime"):
        pushToFile(str(stats.maze1Time), "maze1TopTime")
    if checkIfFastest(stats.maze2Time, "maze2TopTime"):
        pushToFile(str(stats.maze2Time), "maze2TopTime")
    if checkIfFastest(stats.maze3Time, "maze3TopTime"):
        pushToFile(str(stats.maze3Time), "maze3TopTime")
    if checkIfFastest(stats.time, "totalTopTime"):
        pushToFile(str(stats.time), "totalTopTime")

#showing their best times
def showBestTimes(stats:PlayingState):
    #showing both the personal best and he total bes (with total best not working yet)
    toScreen2("Personal Best:", str(stats.maze1Fastest), font25, BLUE, 200, HEIGHT//2+200)
    toScreen2("The Best:", getFromFile("maze1TopTime"), font25, BLUE, 200, HEIGHT//2+100)
    if stats.maze1Time!=1000:
        toScreen2("Personal Best:", str(stats.maze2Fastest), font25, BLUE, WIDTH//2, HEIGHT//2+200)
        toScreen2("The Best:", getFromFile("maze2TopTime"), font25, BLUE, WIDTH//2, HEIGHT//2+100)
        if stats.maze2Time!=1000:
            toScreen2("Personal Best:", str(stats.maze3Fastest), font25, BLUE, WIDTH-200, HEIGHT//2+200)
            toScreen2("Total Personal Best:", str(stats.fastest), font25, BLACK, WIDTH//4, HEIGHT//2)
            toScreen2("The Best:", getFromFile("maze3TopTime"), font25, BLUE, WIDTH-200, HEIGHT//2+100)
            toScreen2("Total Best:", getFromFile("totalTopTime"), font25, BLACK, WIDTH//4*3, HEIGHT//2)
    #showin if there is a record
    if checkIfFastest(stats.maze1Time, "maze1TopTime"):
        toScreen("New Fastest Time!", font30, PURPLE, 100, HEIGHT//2+100)
    if checkIfFastest(stats.maze2Time, "maze2TopTime"):
        toScreen("New Fastest Time!", font30, PURPLE, WIDTH//2-100, HEIGHT//2+100)
    if checkIfFastest(stats.maze3Time, "maze3TopTime"):
        toScreen("New Fastest Time!", font30, PURPLE, WIDTH-200, HEIGHT//2+100)
    if checkIfFastest(stats.time, "totalTopTime"):
        toScreen("New Fastest Time!", font30, PURPLE, WIDTH//2, HEIGHT//2+250)

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

#winnng/losing buttons
def buttons(stats:PlayingState):
    global running

    loss=stats.maze1Time==1000 or stats.maze2Time==1000 or stats.maze3Time==1000

    #setting up the variables for the buttons
    colours=[RED, DARK_RED, ORANGE, DARK_ORANGE, YELLOW, DARK_YELLOW]
    one, two, three=0, 2, 4
    width, height=200,200
    oneButton=(100, HEIGHT//2+50, width, height)
    twoButton=(WIDTH//2-width//2, HEIGHT//2+50, width, height)
    threeButton=(WIDTH-100-width, HEIGHT//2+50, width, height)
    #drawing the boxes
    one=drawTextSquare(colours, one, "1.", oneButton)
    if stats.maze1Time!=1000:
        two=drawTextSquare(colours, two, "2.", twoButton)
        if stats.maze2Time!=1000:
            three=drawTextSquare(colours, three, "3.", threeButton)

    #replaceTimes(stats)
    #showing personal best
    showBestTimes(stats) 

    #getting the game to be able to end
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            print("Pressed")
            if one==1 and (not loss or stats.maze1Time==1000):
                stats.changeMaze(1)
                stats.gameState="Playing"
            elif two==3 and (not loss or stats.maze2Time==1000):
                stats.changeMaze(2)
                stats.gameState="Playing"
            elif three==5 and (not loss or stats.maze3Time==1000):
                stats.changeMaze(3)
                stats.gameState="Playing"
            else:
                print("Whoops")
                #stats.gameState="End"

#creating the locations of the teleporters
def getMaze1Teleporters():
    width, height=45,45
    teleporter1=Teleporter(300, 480, 2, 1, width, height)
    teleporter2=Teleporter(WIDTH-300, 230, 1, 2, width, height)
    teleporter3=Teleporter(250, 280, 4, 3, width, height)
    teleporter4=Teleporter(WIDTH//2, HEIGHT//2+30, 3, 4, width, height)
    return[teleporter1, teleporter2, teleporter3, teleporter4]

def getMaze2Teleporters():
    width, height=30,30
    teleporter1=Teleporter(302.5, 100, 2, 1, width, height)
    teleporter2=Teleporter(WIDTH-282.5, 135, 1, 2, width, height)
    teleporter3=Teleporter(WIDTH//2-7.5, 480, 4, 3, width, height)
    teleporter4=Teleporter(WIDTH-282.5, HEIGHT-80, 3, 4, width, height)
    return[teleporter1, teleporter2, teleporter3, teleporter4]

def getMaze3Teleporters():
    width, height=28,28
    teleporter1=Teleporter(WIDTH-222, 175, 2, 1, width, height)
    teleporter2=Teleporter(282, 207, 1, 2, width, height)
    teleporter3=Teleporter(WIDTH//2-135, 505, 4, 3, width, height)
    teleporter4=Teleporter(WIDTH-257, HEIGHT-95, 3, 4, width, height)
    return[teleporter1, teleporter2, teleporter3, teleporter4]

#creating the mazes' walls
def createMaze()-> list[Wall]:
    walls=[]
    width=5
    gap=50
    
    #having a list of the possible x and y lines
    xList=[]
    yList=[]
    for i in range(0,12):
        xList.append(WIDTH//6-width+gap*i)
        yList.append(25+gap*i)
    
    colour=BLACK
    #if statement just so I can shrink it
    #horizontal walls starting at the top left
    if True:
        walls.append(Wall(xList[0], -20, gap*1+width, width, colour))
        walls.append(Wall(xList[1], yList[0], gap*10+width, width, colour))
        #new row
        walls.append(Wall(xList[2], yList[1], gap*5+width, width, colour))
        walls.append(Wall(xList[8], yList[1], gap*1+width, width, colour))
        #new row
        walls.append(Wall(xList[1], yList[2], gap*1+width, width, colour))
        walls.append(Wall(xList[6], yList[2], gap*2+width, width, colour))
        walls.append(Wall(xList[9], yList[2], gap*1+width, width, colour))
        #new row
        walls.append(Wall(xList[2], yList[3], gap*1+width, width, colour))
        walls.append(Wall(xList[4], yList[3], gap*3+width, width, colour))
        walls.append(Wall(xList[10], yList[3], gap*1+width, width, colour))
        #new row
        walls.append(Wall(xList[1], yList[4], gap*2+width, width, colour))
        walls.append(Wall(xList[5], yList[4], gap*3+width, width, colour))
        walls.append(Wall(xList[9], yList[4], gap*1+width, width, colour))
        #new row
        walls.append(Wall(xList[2], yList[5], gap*2+width, width, colour))
        walls.append(Wall(xList[9], yList[5], gap*2+width, width, colour))
        #new row
        walls.append(Wall(xList[2], yList[6], gap*3+width, width, colour))
        walls.append(Wall(xList[6], yList[6], gap*1+width, width, colour))
        walls.append(Wall(xList[8], yList[6], gap*2+width, width, colour))
        #new row
        walls.append(Wall(xList[1], yList[7], gap*1+width, width, colour))
        walls.append(Wall(xList[3], yList[7], gap*3+width, width, colour))
        walls.append(Wall(xList[7], yList[7], gap*1+width, width, colour))
        walls.append(Wall(xList[9], yList[7], gap*1+width, width, colour))
        #new row
        walls.append(Wall(xList[0], yList[8], gap*1+width, width, colour))
        walls.append(Wall(xList[2], yList[8], gap*2+width, width, colour))
        walls.append(Wall(xList[6], yList[8], gap*1+width, width, colour))
        walls.append(Wall(xList[8], yList[8], gap*1+width, width, colour))
        walls.append(Wall(xList[10], yList[8], gap*1+width, width, colour))
        #new row
        walls.append(Wall(xList[5], yList[9], gap*1+width, width, colour))
        walls.append(Wall(xList[9], yList[9], gap*2+width, width, colour))
        #new row
        walls.append(Wall(xList[1], yList[10], gap*4+width, width, colour))
        walls.append(Wall(xList[7], yList[10], gap*2+width, width, colour))
        #walls.append(Wall(xList[11], yList[10], 205, 5, colour))
        #new row
        walls.append(Wall(xList[0], yList[11], gap*12+width, width, colour))
        walls.append(Wall(xList[11], yList[10], gap*1+width, width, colour))
    addedWidth=0
    #veritcal walls
    if True:
        walls.append(Wall(xList[0], -20, width, 600, colour))
        #new
        walls.append(Wall(xList[1], -20, width, 145, colour))
        walls.append(Wall(xList[1], yList[3], width, gap*4+addedWidth, colour))
        walls.append(Wall(xList[1], yList[8], width, gap*1+addedWidth, colour))
        #new
        walls.append(Wall(xList[2], yList[5], width, gap*1+addedWidth, colour))
        walls.append(Wall(xList[2], yList[7], width, gap*2+addedWidth, colour))
        #new
        walls.append(Wall(xList[3], yList[2], width, gap*2+addedWidth, colour))
        walls.append(Wall(xList[3], yList[9], width, gap*1+addedWidth, colour))
        #new
        walls.append(Wall(xList[4], yList[1], width, gap*1+addedWidth, colour))
        walls.append(Wall(xList[4], yList[3], width, gap*2+addedWidth, colour))
        walls.append(Wall(xList[4], yList[8], width, gap*2+addedWidth, colour))
        #new
        walls.append(Wall(xList[5], yList[2], width, gap*1+addedWidth, colour))
        walls.append(Wall(xList[5], yList[5], width, gap*1+addedWidth, colour))
        walls.append(Wall(xList[5], yList[7], width, gap*3+addedWidth, colour))
        #new
        walls.append(Wall(xList[6], yList[5], width, gap*2+addedWidth, colour))
        walls.append(Wall(xList[6], yList[9], width, gap*2+addedWidth, colour))
        #new
        walls.append(Wall(xList[7], yList[0], width, gap*1+addedWidth, colour))
        walls.append(Wall(xList[7], yList[2], width, gap*1+addedWidth, colour))
        walls.append(Wall(xList[7], yList[4], width, gap*1+addedWidth, colour))
        walls.append(Wall(xList[7], yList[6], width, gap*3+addedWidth, colour))
        #new
        walls.append(Wall(xList[8], yList[1], width, gap*1+addedWidth, colour))
        walls.append(Wall(xList[8], yList[3], width, gap*4+addedWidth, colour))
        walls.append(Wall(xList[8], yList[8], width, gap*2+addedWidth, colour))
        #new
        walls.append(Wall(xList[9], yList[0], width, gap*1+addedWidth, colour))
        walls.append(Wall(xList[9], yList[2], width, gap*3+addedWidth, colour))
        walls.append(Wall(xList[9], yList[7], width, gap*1+addedWidth, colour))
        walls.append(Wall(xList[9], yList[9], width, gap*1+addedWidth, colour))
        #new
        walls.append(Wall(xList[10], yList[1], width, gap*1+addedWidth, colour))
        walls.append(Wall(xList[10], yList[10], width, gap*1+addedWidth, colour))
        #new
        walls.append(Wall(xList[11], yList[0], width, gap*10+addedWidth, colour))

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
        xList.append(WIDTH//6-width+gap*i)
        yList.append(5+gap*i)
    
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

    #vertical
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
        walls.append(Wall(xList[8], -20, width, 25+gap+width, colour))
        walls.append(Wall(xList[8], yList[2], width, gap*1+width, colour))
        walls.append(Wall(xList[8], yList[6], width, gap*3+width, colour))
        walls.append(Wall(xList[8], yList[13], width, gap*1+width, colour))
        walls.append(Wall(xList[8], yList[16], width, gap*1+width, colour))
        #new
        walls.append(Wall(xList[9], -20, width, 25+gap+width, colour))
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
    toScreen3("Try to find your way out of the maze as fast as posible", "You have a maximum of 60 seconds for the first maze, 75 seconds for the second, ", "and 90 seconds for the third so try not to get lost", font20, BLACK, WIDTH//2, HEIGHT//2)
    toScreen3("There will be multiple choices for the difficulty level.", "Fog mean you can only see a radius of roughly 200 pixels around you", "Teleporters will teleport you to another teleporter if you click space while touching it.", font15, WHITE, WIDTH//2, HEIGHT//2+50)
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
                gameState="Choose"
    #end
    return gameState

#choosing the maze difficulty
def choose(stats:PlayingState):
    global running
    screen.fill(DARK_TEAL)
    toScreen("Please choose which level of difficulty you want.", font37, BLACK, WIDTH//2, 100)
    toScreen2("1. No fog, no teleporters, 2. No fog, yes teleporters", "3. Yes fog, yes teleporters, 4. Yes fog, no teleporters", font30, BLACK, WIDTH//2, HEIGHT//2-75)

    #creating buttons
    colours=[RED, DARK_RED, ORANGE, DARK_ORANGE, YELLOW, DARK_YELLOW, GREEN, DARK_GREEN]
    one, two, three, four=0, 2, 4, 6
    width, height=175,175
    oneButton=(40, HEIGHT//2+50, width, height)
    twoButton=(WIDTH//2-20-width, HEIGHT//2+50, width, height)
    threeButton=(WIDTH//2+20, HEIGHT//2+50, width, height)
    fourButton=(WIDTH-40-width, HEIGHT//2+50, width, height)
    one=drawTextSquare(colours, one, "1.", oneButton)
    two=drawTextSquare(colours, two, "2.", twoButton)
    three=drawTextSquare(colours, three, "3.", threeButton)
    four=drawTextSquare(colours, four, "4.", fourButton)

    #checking for clicks and stopping
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            if one==1:
                level=1
            elif two==3:
                level=2
            elif three==5:
                level=3
            elif four==7:
                level=4
            if one==1 or two==3 or three==5 or four==7:
                stats.gameState="Playing"
                stats.makeLevelsWork(level)

    
    return stats
    
#main normal playing scene
def playing(playingStuff: PlayingState):    
    sprites=pygame.sprite.Group()
    sprites.add(playingStuff.player)
    
    if playingStuff.level==3 or  playingStuff.level==4:
        sprites.add(playingStuff.fog)
    if playingStuff.level==2 or playingStuff.level==3:
        for teleporter in playingStuff.teleporters:
            sprites.add(teleporter)
    sprites.add(playingStuff.pie)

    
    global running

    screen.fill(GREEN)
    #checking to allow the game to end
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.MOUSEBUTTONDOWN and playingStuff.maze1Time!=1000 and playingStuff.maze2Time!=1000 and playingStuff.maze3Time!=1000:
            print("Pressed")
            playingStuff.gameState="Won"
        #moving
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                playingStuff.player.ySpeed-=playingStuff.player.speed*FPSScaling
            elif event.key==pygame.K_DOWN:
                playingStuff.player.ySpeed+=playingStuff.player.speed*FPSScaling
            elif event.key==pygame.K_LEFT:
                playingStuff.player.xSpeed-=playingStuff.player.speed*FPSScaling
            elif event.key==pygame.K_RIGHT:
                playingStuff.player.xSpeed+=playingStuff.player.speed*FPSScaling
            if event.key==pygame.K_SPACE:
                playingStuff.player.teleport(playingStuff.teleporters)

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_UP or event.key==pygame.K_DOWN:
                playingStuff.player.ySpeed=0
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playingStuff.player.xSpeed=0
            if event.key==pygame.K_SPACE:
                playingStuff.player.speed=4
        
    
    #drawing tracking balls
    playingStuff.trails.append(Ball(playingStuff.player.x+playingStuff.player.width//2, playingStuff.player.y+playingStuff.player.height//2, BLACK, 5))
    for ball in playingStuff.trails:
        ball.update()
        ball.draw()
    
    #getting the maze
    for wall in playingStuff.walls:
        wall.draw()

    #drawing the player and pie and fog
    playingStuff.player.checkCollide(playingStuff.walls)
    playingStuff.player.update(playingStuff.player.xSpeed, playingStuff.player.ySpeed)
    if playingStuff.level==3 or playingStuff.level==4:
        playingStuff.fog.move(playingStuff.player.x-WIDTH, playingStuff.player.y-HEIGHT)
    sprites.draw(screen)
    
    #printing the time
    colour=BLACK
    if playingStuff.maxTime-playingStuff.time<10:
        colour=RED
    toScreen("Time: "+str(round(playingStuff.time)), font30, colour, WIDTH-100, 30)
    toScreen("Max time: "+str(playingStuff.maxTime), font30, BLACK, WIDTH-100, 60)

    
    #stopping
    #losing after the max time seconds
    if playingStuff.time>playingStuff.maxTime:
        playingStuff.gameState="Loss"
    #going back to the end screen if they have returned
    elif playingStuff.maze1Time!=1000 and playingStuff.maze2Time!=1000 and playingStuff.maze3Time!=1000 and (playingStuff.player.x>WIDTH//2+250 and playingStuff.maze!=3 or playingStuff.maze==3 and playingStuff.player.y>HEIGHT-30):
        playingStuff.gameState="Won"
        playingStuff.updateTimers()
        replaceTimes(playingStuff)
        playingStuff.time=round((playingStuff.maze1Fastest+playingStuff.maze2Fastest+playingStuff.maze3Fastest)*100)/100
        if playingStuff.time<playingStuff.fastest:
            playingStuff.fastest=round((playingStuff.time)*100)/100
    #winning
    elif playingStuff.player.x>WIDTH//2+250:
        playingStuff.updateTimers()
        playingStuff.maze+=1
        playingStuff.changeMaze(playingStuff.maze)
        playingStuff.gameState="Playing"
    #third maze ending
    elif playingStuff.maze==3 and playingStuff.player.y>HEIGHT-30:
        playingStuff.gameState="Won"
        playingStuff.updateTimers()
        playingStuff.time=round((playingStuff.maze1Fastest+playingStuff.maze2Fastest+playingStuff.maze3Fastest)*100)/100
        if playingStuff.time<playingStuff.fastest:
            playingStuff.fastest=round((playingStuff.time)*100)/100
    
    return playingStuff

#won screen
def won(stats: PlayingState):
    global running

    screen.fill(DARK_MAGENTA)
    toScreen("Yay! You won!", font40, BLUE, WIDTH//2, 50)
    toScreen("It only took you a total of "+str(stats.time)+" seconds to escape.", font20, GREEN, WIDTH//2, 100)
    toScreen3("It took you "+str(stats.maze1Time)+" seconds to escape the first maze", "It took you "+str(stats.maze2Time)+" seconds to escape the second maze", "It took you "+str(stats.maze3Time)+" seconds to escape the third maze", font30, BLACK, WIDTH//2, HEIGHT//2-100)
    
    #showing the buttons to replay
    buttons(stats)

    return stats

def loss(stats:PlayingState):
    global running
    screen.fill(DARK_RED)
    toScreen("Aw, you lost.", font40, BLACK, WIDTH//2, 50)
    toScreen2("The 1000 just means that you haven't finished the maze yet,", "please click on the button and try that maze again", font30, BLACK, WIDTH//2, HEIGHT//2-150)
    buttons(stats)

    return stats.gameState

#main function
async def main():
    #stuff
    global running
    maze=1
    playingStuff=PlayingState(maze)

    #having the game actually run
    while running:
        if playingStuff.gameState=="Intro":
            playingStuff.gameState=intro(playingStuff.gameState)
        elif playingStuff.gameState=="Choose":
            playingStuff=choose(playingStuff)
        elif playingStuff.gameState=="Playing":
            playingStuff=playing(playingStuff)
            playingStuff.time+=1/FPS

        elif playingStuff.gameState=="Won":
            playingStuff=won(playingStuff)
        elif playingStuff.gameState=="Loss":
            playingStuff.gameState=loss(playingStuff)
        else:
            running=False

        #doing mandatory stuff
        clock.tick(FPS)
        pygame.display.flip()
    await asyncio.sleep(0)



#stuff
if __name__=="__main__":
    asyncio.run(main())
    pygame.quit()
    