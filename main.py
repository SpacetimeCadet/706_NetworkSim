import os

os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (100, 100)

import pygame, sys
import theme
from button import Button
from pygame.locals import QUIT
import string
import math

pygame.init()

#Screen setup
#original size: Height = 1120, Width = 2025

height = 600
width = 1200

screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption('Connection Model')

objects = []
routers = []
connections = []

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
        self.routerSelected = False
        self.routerA = 0
        self.routerB = 0


class RouterIcon():
    #depicts router on drawing screen, tracks connections
    def __init__(self, x, y):
        self.surface = screen
        self.color = currentStyle.get("buttonColourDark")
        self.center = (x, y)
        self.radius = 20
        self.connections = []


class ConnectionIcon():
    #line between two router icons
    def __init__(self, x1, y1, x2, y2):
        self.surface = screen
        self.color = (0, 0, 0)
        self.start = (x1, y1)
        self.end = (x2, y2)


def selectSendPort():
    print('Send pressed')


def selectAlgorithm():
    print('Algorithm pressed')


def selectRecievePort():
    print('Recieve pressed')


def addRouter():
    data.drawingRouter = True
    data.drawingConnection = False


def addConnection():
    data.drawingConnection = True
    data.drawingRouter = False


def clearData():
    connections.clear()
    routers.clear()


def onDrawingArea(x, y):
    #is the mouse over the drawing area?
    if x > width * 0.04 and x < width * 0.96 and y > height * 0.25 and y < height * 0.75:
        return True
    return False


def getClickedRouter():
    mx, my = pygame.mouse.get_pos()
    for router in routers:
        if mx > router.center[0] - router.radius and mx < router.center[
                0] + router.radius:
            if my > router.center[1] - router.radius and my < router.center[
                    1] + router.radius:
                return router


def getRouterAt(x, y):
    for router in routers:
        if x > router.center[0] - router.radius and x < router.center[
                0] + router.radius:
            if y > router.center[1] - router.radius and y < router.center[
                    1] + router.radius:
                return router


def isClickingRouter():
    mx, my = pygame.mouse.get_pos()
    for router in routers:
        if mx > router.center[0] - router.radius and mx < router.center[
                0] + router.radius:
            if my > router.center[1] - router.radius and my < router.center[
                    1] + router.radius:
                return True
    return False


def disconnectRouters(routerA, routerB):
    i = 0
    for neighbor in routerA.connections:
        if neighbor == routerB:
            routerA.connections.pop(i)
        i = i + 1
    j = 0
    for neighbor in routerB.connections:
        if neighbor == routerA:
            routerB.connections.pop(j)
        j = j + 1


def removeConnectionAtPoint(x, y):
    flexibility = 0.5
    i = -1
    for connection in connections:
        #only check connections that are in the same "hit box" rectangle as the point
        i = i + 1
        if (x < connection.start[0]
                and x > connection.end[0]) or (x > connection.start[0]
                                               and x < connection.end[0]):
            if (y < connection.start[1]
                    and y > connection.end[1]) or (y > connection.start[1]
                                                   and y < connection.end[1]):
                #refine for multiple connections in a "hit box"
                newPointx = x - connection.start[0]
                newPointy = y - connection.start[1]
                newEndx = connection.end[0] - connection.start[0]
                newEndy = connection.end[1] - connection.start[1]
                endHyp = math.sqrt(newEndx * newEndx + newEndy * newEndy)
                pointHyp = math.sqrt(newPointx * newPointx +
                                     newPointy * newPointy)
                endAngle = newEndx / endHyp
                pointAngle = newPointx / pointHyp
                if pointAngle > endAngle - flexibility and pointAngle < endAngle + flexibility:
                    routerA = getRouterAt(connection.start[0],
                                          connection.start[1])
                    routerB = getRouterAt(connection.end[0], connection.end[1])
                    disconnectRouters(routerA, routerB)
                    connections.pop(i)


def removeConnectionBetweenRouters(routerA, routerB):
    #removes from "connections", doesn't change router connection lists
    i = 0
    for connection in connections:
        if connection.start == routerA.center and connection.end == routerB.center:
            connections.pop(i)
            break
        elif connection.start == routerB.center and connection.end == routerA.center:
            connections.pop(i)
            break
        else:
            i = i + 1


def removeAllConnectionsOfRouter(routerA):
    for neighbour in routerA.connections:
        removeConnectionBetweenRouters(routerA, neighbour)
        i = 0
        for otherNeighbour in neighbour.connections:
            if otherNeighbour == routerA:
                neighbour.connections.pop(i)
                break
            i = i + 1
    routerA.connections.clear()


def toggleState():
    data.state = (not data.state)
    data.stateSetupDone = False
    objects.clear()
    data.drawingRouter = False
    data.drawingConnection = False
    data.routerSelected = False
    data.routerA = 0
    data.routerB = 0


def setupState():
    #get user input on routers, state=True
    #Start by adding buttons
    if not data.stateSetupDone:
        fontSize = int(width * 0.013)
        objects.extend([
            Button(width * 0.04, height * 0.18, width * 0.12, height * 0.05,
                   fontSize, 'ADD ROUTER', addRouter),
            Button(width * 0.19, height * 0.18, width * 0.13, height * 0.05,
                   fontSize, 'ADD CONNECTION', addConnection),
            Button(width * 0.34, height * 0.18, width * 0.13, height * 0.05,
                   fontSize, 'RANDOMIZE DATA', addConnection),
            Button(width * 0.49, height * 0.18, width * 0.13, height * 0.05,
                   fontSize, 'CLEAR NETWORK', clearData),
            Button(width * 0.4, height * 0.8, width * 0.2, height * 0.05,
                   fontSize, 'USE THIS DATA', toggleState)
        ])
        data.stateSetupDone = True

    #drawing panel
    pygame.draw.rect(screen, (255, 255, 255),
                     (width * 0.04, height * 0.25, width * 0.92, height * 0.5))

    if pygame.mouse.get_pressed()[0]:
        #add new router
        if data.drawingRouter:
            mx, my = pygame.mouse.get_pos()
            if onDrawingArea(mx, my):
                routers.append(RouterIcon(mx, my))
                data.drawingRouter = False
        #add new connection
        if data.drawingConnection:
            if not data.routerSelected and isClickingRouter():
                data.routerA = getClickedRouter()
                data.routerSelected = True
            elif data.routerSelected and isClickingRouter():
                data.routerB = getClickedRouter()
                connections.append(
                    ConnectionIcon(data.routerA.center[0],
                                   data.routerA.center[1],
                                   data.routerB.center[0],
                                   data.routerB.center[1]))
                data.routerA.connections.append(data.routerB)
                data.routerB.connections.append(data.routerA)
                data.drawingConnection = False
                data.routerSelected = False
            else:
                data.drawingConnection = False
                data.routerSelected = False

    #deletion
    if pygame.mouse.get_pressed()[2]:
        mx, my = pygame.mouse.get_pos()
        removeConnectionAtPoint(mx, my)
        if isClickingRouter():
            r = getClickedRouter()
            removeAllConnectionsOfRouter(r)
            i = 0
            for node in routers:
                if node == r:
                    routers.pop(i)
                    break
                i = i + 1

    #Tell user if they're drawing router/connection
    if data.drawingRouter:
      text("Drawing Router", theme.medFont, int(0.015 * width),
         currentStyle.get("buttonColourDark"), width * 0.04, height * 0.25)
    if data.drawingConnection:
      text("Drawing Connection", theme.medFont, int(0.015 * width),
         currentStyle.get("buttonColourDark"), width * 0.04, height * 0.25)
      
    
    #draw all lines
    for connection in connections:
        pygame.draw.line(screen, (0, 0, 0), connection.start, connection.end,
                         2)

    #draw all routers
    i = 0
    for router in routers:
        pygame.draw.circle(router.surface, router.color, router.center,
                           router.radius)
        text(
            list(string.ascii_uppercase)[i % 26], theme.lightFont, 15,
            currentStyle.get("titleColour"), router.center[0] - 5,
            router.center[1] - 5)
        i = i + 1

    #draw unfinished connection line
    if data.drawingConnection and data.routerSelected:
        pygame.draw.line(screen, (100, 100, 100), data.routerA.center,
                         pygame.mouse.get_pos())


def traceState():
    #main state, algoritms performed on router data, state=False
    if not data.stateSetupDone:
        fontSize = int(width * 0.013)
        objects.extend([
            Button(width * 0.04, height * 0.18, width * 0.12, height * 0.05,
                   fontSize, 'SENDING PORT', selectSendPort),
            Button(width * 0.19, height * 0.18, width * 0.12, height * 0.05,
                   fontSize, 'ALGORITHM', selectAlgorithm),
            Button(width * 0.34, height * 0.18, width * 0.12, height * 0.05,
                   fontSize, 'RECIEVING PORT', selectRecievePort),
            Button(width * 0.4, height * 0.8, width * 0.2, height * 0.05,
                   fontSize, 'CHANGE ROUTER DATA', toggleState)
        ])
        data.stateSetupDone = True


def draw():
    screen.blit(
        pygame.transform.smoothscale(currentStyle.get("background"),
                                     (width, height)), (0, 0))
    centreText("CPS706 PROJECT", theme.medFont, int(width * 0.05),
               currentStyle.get("titleColour"), height * 0.1)
    text("BY [GROUP MEMBERS]", theme.medFont, int(0.01 * width),
         currentStyle.get("titleColour"), width * 0.3, height * 0.14)

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

            if event.w < 600 or event.h < 300:
                width = 600
                height = 300
            elif event.w != width:
                width = event.w
                height = width // 2
            else:
                height = event.h
                width = 2 * height
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            data.stateSetupDone = False
            objects.clear()

    draw()
    pygame.display.update()
    #fpsClock.tick(fps)
