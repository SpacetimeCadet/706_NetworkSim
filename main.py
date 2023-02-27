import pygame, sys
import theme
from button import Button
from pygame.locals import QUIT

pygame.init()

#Screen setup
height = 1120
width = 2025
size = [width, height]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Connection Model')

objects = []

#style: 1 = teal theme, network background, 2 = blue theme, spiral background
theme.style = 2
currentStyle = theme.currentTheme()

class Data():
    #keep track of central variables
    def __init__(self):
        self.state = True
        self.stateSetupDone = False


def selectSendPort():
    print('Send pressed')


def selectAlgorithm():
    print('Algorithm pressed')


def selectRecievePort():
    print('Recieve pressed')


def addRouter():
    print('Add Router pressed')


def addConnection():
    print('Add Connection pressed')


def toggleState():
    data.state = (not data.state)
    data.stateSetupDone = False
    objects.clear()


def setupState():
    #get user input on routers, state=True
    if not data.stateSetupDone:
        objects.extend([
            Button(75, 200, 250, 60, 'ADD ROUTER', addRouter),
            Button(375, 200, 250, 60, 'ADD CONNECTION', addConnection),
            #probably remove "add connection" button, trigged by draging from one router to another
            Button(1000, 900, 400, 60, 'USE THIS DATA', toggleState)
            ])
        data.stateSetupDone = True


def traceState():
    #main state, algoritms performed on router data, state=False
    if not data.stateSetupDone:
        objects.extend([
            Button(75, 200, 250, 60, 'SENDING PORT', selectSendPort),
            Button(375, 200, 250, 60, 'ALGORITHM', selectAlgorithm),
            Button(675, 200, 250, 60, 'RECIEVING PORT', selectRecievePort),
            Button(1000, 900, 400, 60, 'CHANGE ROUTER DATA', toggleState)
            ])
        data.stateSetupDone = True


def draw(size):
    screen.blit(currentStyle.get("background"), (0, 0))
    centreText("CPS706 PROJECT", theme.medFont, 100, currentStyle.get("titleColour"), 100)
    text("BY [GROUP MEMBERS]", theme.medFont, 25, currentStyle.get("titleColour"), 575, 150)
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
    draw(size)
    pygame.display.update()
    #fpsClock.tick(fps)
