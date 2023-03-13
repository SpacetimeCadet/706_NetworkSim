import pygame, sys
import theme
from button import Button
from pygame.locals import QUIT
import string

pygame.init()

#Screen setup
#original size: Height = 1120, Width = 2025
height = 800
width = 800
size = [width, height]
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption('Connection Model')

objects = []
routers = []

#style: 1 = teal theme, network background, 2 = blue theme, spiral background
theme.style = 1
currentStyle = theme.currentTheme()

class Data():
    #keep track of central variables
    def __init__(self):
        self.state = True
        self.stateSetupDone = False
        self.drawingRouter = False
        self.drawingConnection = False

class RouterIcon():
  def __init__(self,x,y):
    self.surface = screen
    self.color = currentStyle.get("buttonColourDark")
    self.center = (x,y)
    self.radius = 20

class ConnectionIcon():
  def __init(self,x,y):
    self.surface = screen
    self.color = (0,0,0)
    self.x = x
    self.y = y


def selectSendPort():
    print('Send pressed')


def selectAlgorithm():
    print('Algorithm pressed')


def selectRecievePort():
    print('Recieve pressed')


def addRouter():
    data.drawingRouter = True

def addConnection():
    data.drawingConnection = True


def onDrawingArea(x,y):
  if x > width*0.04 and x < width*0.96 and y > height*0.25 and y < height *0.75:  
    return True
  return False
def toggleState():
    data.state = (not data.state)
    data.stateSetupDone = False
    objects.clear()


def setupState():
    #get user input on routers, state=True
    #Start by adding buttons
    if not data.stateSetupDone:
        fontSize = int(width*0.013)
        objects.extend([
            Button(width*0.04, height*0.18, width*0.12, height*0.05, fontSize, 'ADD ROUTER', addRouter),
            Button(width*0.19, height*0.18, width*0.13, height*0.05, fontSize, 'ADD CONNECTION', addConnection),
            Button(width*0.34, height*0.18, width*0.13, height*0.05, fontSize, 'RANDOMIZE DATA', addConnection),
            Button(width*0.4, height*0.8, width*0.2, height*0.05, fontSize, 'USE THIS DATA', toggleState)
            ])
        data.stateSetupDone = True

    #drawing panel  
    pygame.draw.rect(screen, (255,255,255), (width*0.04,height*0.25,width*0.92,height*0.5))
  
    #add new router
    if pygame.mouse.get_pressed()[0] and data.drawingRouter:
        mx, my = pygame.mouse.get_pos()
        if onDrawingArea(mx,my):
          routers.append(RouterIcon(mx,my))
          data.drawingRouter = False
    
    #draw all routers
    i = 0
    for router in routers:
        pygame.draw.circle(router.surface, router.color, router.center, router.radius)
        text(list(string.ascii_uppercase)[i%26], theme.lightFont, 15, currentStyle.get("titleColour"), router.center[0]-5, router.center[1]-5)
        i = i+1


def traceState():
    #main state, algoritms performed on router data, state=False
    if not data.stateSetupDone:
        fontSize = int(width*0.013)
        objects.extend([
            Button(width*0.04, height*0.18, width*0.12, height*0.05, fontSize, 'SENDING PORT', selectSendPort),
            Button(width*0.19, height*0.18, width*0.12, height*0.05, fontSize, 'ALGORITHM', selectAlgorithm),
            Button(width*0.34, height*0.18, width*0.12, height*0.05, fontSize, 'RECIEVING PORT', selectRecievePort),
            Button(width*0.4, height*0.8, width*0.2, height*0.05, fontSize, 'CHANGE ROUTER DATA', toggleState)
            ])
        data.stateSetupDone = True


def draw(size):
    screen.blit(currentStyle.get("background"), (0, 0))
    centreText("CPS706 PROJECT", theme.medFont, int(width*0.05), currentStyle.get("titleColour"), height*0.1)
    text("BY [GROUP MEMBERS]", theme.medFont, int(0.01*width), currentStyle.get("titleColour"), width*0.3, height*0.14)
  
    if data.state:
        setupState()
    else:
        traceState()
      
    for object in objects:
        object.process()


def text(words, font, size, colour, x, y):
    # add text on screen
    myfont = pygame.font.Font(font, size)
    textA = myfont.render(words, False, colour)
    screen.blit(textA, (x, y))


def centreText(words, font, size, colour, y):
    #add centred text on screen
    myfont = pygame.font.Font(font, size)
    textA = myfont.render(words, False, colour)
    text_rect = textA.get_rect(center=(width / 2, y))
    screen.blit(textA, text_rect)


#Game loop
data = Data()
while True:
    event = pygame.event.wait()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            # There's some code to add back window content here.
            screen = pygame.display.set_mode((event.w, event.h),
                                              pygame.RESIZABLE)
    draw(size)
    pygame.display.update()
    #fpsClock.tick(fps)




        