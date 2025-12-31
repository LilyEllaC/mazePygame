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
        for wall in walls:
            if playerRect.colliderect(wall.rect):#pygame.Rect.colliderect(self.get_rect(), wall.getRect()):
                if (wall.isHorizontal):
                    if rightPosition(wall.x, wall.width, self.x, self.xSpeed):
                        if self.y>wall.y:
                            self.y+=5
                        else:
                            self.y-=5
                    else:
                        if self.x>wall.x:
                            self.x+=5
                        else:
                            self.x-=5
                #vertical paddles
                else:
                    if rightPosition(wall.y, wall.length, self.y, self.ySpeed):
                        if self.x>wall.x:
                            self.x+=5
                        else:
                            self.x-=5
                    else:
                        if self.y>wall.y:
                            self.y+=5
                        else:
                            self.y-=5                

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

#creating the maze walls
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
        walls.append(Wall(xList[0], yList[11], 555, 5, colour))
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
    toScreen3("Try to find your way out of the maze as fast as posible", "You only have XXXX minutes to escape so act fast!", "Random silly background story stuff", font20, BLACK, WIDTH//2, HEIGHT//2)

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
                gameState="Playing"
    #end
    return gameState

#main normal playing scene
def playing(gameState, walls, sprites, player):
    global running

    screen.fill(GREEN)
    #checking to allow the game to end
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            print("Pressed")
            gameState="end"
        #moving
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                player.ySpeed-=player.speed
            elif event.key==pygame.K_DOWN:
                player.ySpeed+=player.speed
            elif event.key==pygame.K_LEFT:
                player.xSpeed-=player.speed
            elif event.key==pygame.K_RIGHT:
                player.xSpeed+=player.speed

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_UP or event.key==pygame.K_DOWN:
                player.ySpeed=0
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                player.xSpeed=0
                
    player.checkCollide(walls)
    player.update(player.xSpeed, player.ySpeed)


    sprites.draw(screen)
    #getting the maze
    for wall in walls:
        wall.draw()
    return gameState

#main function
def main():
    #creating the sprites
    player=Player(WIDTH//6+10, 10, 25, 25, 4)
    walls=createMaze()
    playingSprites=pygame.sprite.Group()
    playingSprites.add(player)
    
    #stuff
    global running
    gameState="Intro"

    #having the game actually run
    while running:
        if gameState=="Intro":
            gameState=intro(gameState)
        elif gameState=="Playing":
            gameState=playing(gameState, walls, playingSprites, player)
        elif gameState=="Won":
            won()

        elif gameState=="Loss":
            loss()
        else:
            running=False

        #doing mandatory stuff
        clock.tick(FPS)
        pygame.display.flip()
        



#stuff
if __name__=="__main__":
    main()
    pygame.quit()
    