###



import os

os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (100, 100)

import pygame, sys, math, theme, datetime, random, time
from helper_functions.button import Button
from helper_functions.data import Data
from helper_functions.textBox import TextBox
from pygame.locals import QUIT
from network import Network
from distance_vector import dist_vec
from dijsktra import Dijsktra

pygame.init()

#Screen setup
height = 600
width = 1200

screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption('Connection Model')

### OBJECT ARRAYS ###
buttons = []
routers = []
connections = []
network = Network([], [])  #empty lists create empty Network
animationRouters = []
animationConnections = []

#Leftover style code: could be expanded to allow the user to change theme
#style: 1 = teal theme, network background, 2 = blue theme, spiral background
theme.style = 1
currentStyle = theme.currentTheme()

### OBJECTS ###
class RouterIcon():
    #depicts router on drawing screen, tracks connections
    def __init__(self, x, y, id):
        self.surface = screen
        self.colour = currentStyle.get("buttonColourDark")
        self.center = (x, y)
        self.radius = 20.0
        self.id = id
        self.connections = []

    def setCoordinates(self, x, y):
        self.center = (x, y)

    def setColour(self, colour):
        self.colour = currentStyle.get(colour)

class ConnectionIcon():
    #line between two router icons
    def __init__(self, x1, y1, x2, y2):
        self.surface = screen
        self.colour = (0, 0, 0)
        self.start = (x1, y1)
        self.startRouter = getRouterAt(x1, y1)
        self.end = (x2, y2)
        self.endRouter = getRouterAt(x2, y2)
        self.weight = 1

    def addIDs(self, a, b):
        self.a = a
        self.b = b

    def moveStart(self, x, y):
        self.start = (x, y)

    def moveEnd(self, x, y):
        self.end = (x, y)

    def setColour(self, colour):
        self.colour = currentStyle.get(colour)

    def turnBlack(self):
        self.colour = (0, 0, 0)


### BUTTON FUNCTIONS ###
def selectSendPort():
    if data.runAnimation:
        stopAnimation()
        data.refresh()
    data.selectingSendingPort = True

def selectAlgorithm():
    start = data.sendingPort
    end = data.recievingPort
    if data.selectedAlgorithm == "Dijsktra":
        data.refresh()
        data.toggleAlgorithm()
    else:
        data.refresh()
    data.sendingPort = start
    data.recievingPort = end
    darkenNetwork()

def selectRecievePort():
    if data.runAnimation:
        stopAnimation()
        data.refresh()
    data.selectingRecievingPort = True

def runAlgorithm():
    if data.sendingPort != 0 and data.recievingPort != 0:
        graph = network.toDictionary()
        if data.selectedAlgorithm == "Dijsktra":
            dInfo = Dijsktra(graph, data.sendingPort.id, data.recievingPort.id)
            data.traceList = dInfo[0]
            nodeList = dInfo[1]
            data.traceDescription = dInfo[2]
        else:
            #nodeList = dist_vec(network.toDictionary(), data.sendingPort.id,
            #                    data.recievingPort.id)
            bfInfo = dist_vec(network.toDictionary(), data.sendingPort.id, data.recievingPort.id)
            data.traceList = bfInfo[0]
            nodeList = data.traceList[-1]
            data.traceDescription = bfInfo[1]
        formAnimation(nodeList)
        data.algorithmDone = True
        toggleAnimationButtons()
        fontSize = int(width * 0.013)
        buttons.extend([Button(width * 0.75, height * 0.7, width * 0.1, height * 0.05, fontSize, 'NEXT', nextStep)])
        buttons.extend([Button(width * 0.15, height * 0.7, width * 0.1, height * 0.05, fontSize, 'PREVIOUS', lastStep)])

    else:
        text("Please select both a sending router and a receiving router",
             theme.boldFont, int(0.015 * width),
             currentStyle.get("buttonTextColour"), width * 0.04, height * 0.86)

def addRouter():
    if not data.choosingConnectionWeight:
        data.drawingRouter = True
        data.drawingConnection = False

def addConnection():
    if len(network.nodes) > 1 and not data.choosingConnectionWeight:
        data.drawingConnection = True
        data.drawingRouter = False

def randomizeNetwork():
    clearData()
    network.randomizeNetwork(random.randint(2, 12))
    numNodes = len(network.nodes)
    radius = height * 0.2
    num = math.pi * 2 / numNodes
    for i in range(numNodes):
        x = math.cos(num * i) * radius + (width / 2)
        y = math.sin(num * i) * radius + (height / 2)
        routers.append(RouterIcon(x, y, network.nodes[i]))
    for link in network.links:
        startID = link[0]
        endID = link[1]
        weight = link[2]
        connections.append(
            ConnectionIcon(routers[startID].center[0],
                           routers[startID].center[1],
                           routers[endID].center[0], routers[endID].center[1]))
        routers[startID].connections.append(routers[endID])
        routers[endID].connections.append(routers[startID])
        connections[-1].weight = weight

def clearData():
    network.clear()
    connections.clear()
    routers.clear()
    data.refresh()

def printDebug():
    print("- - -")
    print(datetime.datetime.now())
    print("nodes:", network.nodes)
    print("links:", network.links)
    print("dictionary:", network.toDictionary())

def toggleState():
    if not data.choosingConnectionWeight:
        #add check for a connected network when switching from setup to trace
        #send drawn graph to network
        data.state = (not data.state)
        data.stateSetupDone = False
        darkenNetwork()
        buttons.clear()
        if data.runAnimation:
            stopAnimation()
        data.refresh()

def toggleAnimation():
    data.runAnimation = not data.runAnimation
    toggleAnimationButtons()
    darkenNetwork()
    data.step = len(data.traceDescription) + 1
    
def toggleAnimationButtons():
    if data.runAnimation:
            fontSize = int(width * 0.013)
            buttons.extend([Button(width * 0.75, height * 0.18, width * 0.15, height * 0.05, fontSize, 'STOP ANIMATION', toggleAnimation)])
    else:
            fontSize = int(width * 0.013)
            buttons.extend([Button(width * 0.75, height * 0.18, width * 0.15, height * 0.05, fontSize, 'RUN ANIMATION', toggleAnimation)])

def nextStep():
    if data.step < len(data.traceDescription) - 1:
        data.step = data.step + 1
    if data.step == len(data.traceDescription) - 1:
        darkenNetwork()
        toggleAnimationButtons()
        data.runAnimation = True
               
def lastStep():
    data.runAnimation = False
    if data.step >= len(data.traceDescription):
        data.step = 0
    if data.step > 0:
        data.step = data.step - 1


### UI HELPER METHODS ###
def onDrawingArea(x, y):
    #is the mouse over the drawing area?
    if x > width * 0.04 and x < width * 0.96 and y > height * 0.25 and y < height * 0.75:
        return True
    return False

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

def getConnectionAt(x, y):
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
                return connection;
    return False

def removeConnectionAtPoint(x, y):
    flexibility = 0.01
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
                    network.removeLink([
                        routerA.id, routerB.id,
                        network.getWeight(routerA.id, routerB.id)
                    ])

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

def findClickedButton():
    for button in buttons:
        if button.mouseHover:
            button.onclickFunction()
            return True
    return False

def handleSetupLDown(mx, my):
    #add new router
    if data.drawingRouter:
        routers.append(RouterIcon(mx, my, network.assignNode()))
        network.addNode(network.assignNode())
    #add new connection
    elif data.drawingConnection:
        if not data.routerSelected and isClickingRouter():
            data.routerA = getRouterAt(mx, my)
            data.routerSelected = True
        elif data.routerSelected and isClickingRouter():
            data.routerB = getRouterAt(mx, my)
            if (data.routerB != 0 
                and not data.routerB is data.routerA 
                and not data.routerB in data.routerA.connections):
                    data.drawingConnection = False
                    data.choosingConnectionWeight = True
        else:
            data.drawingConnection = False
            data.routerSelected = False
    elif isClickingRouter():
        data.draggingRouter = getRouterAt(mx, my)
    else:
        conn = getConnectionAt(mx, my)
        if not conn is False:
            data.choosingConnectionWeight = True
            data.reassigningWeight = True
            data.routerA = conn.startRouter
            data.routerB = conn.endRouter
            data.connectionA = conn

def handleTraceLDown(mx, my):
    if data.selectingSendingPort:
        if isClickingRouter():
            #if a sending port has already been selected, change it back to a regular router
            if data.sendingPort != 0:
                data.sendingPort.setColour("buttonColourDark")
            #sending port cannot be the recieving port
            if data.recievingPort == getRouterAt(mx, my):
                data.recievingPort = 0
            data.sendingPort = getRouterAt(mx, my)
            data.sendingPort.setColour("buttonTextColour")
        data.selectingSendingPort = False
    elif data.selectingRecievingPort:
        if isClickingRouter():
            #if a sending port has already been selected, change it back to a regular router
            if data.recievingPort != 0:
                data.recievingPort.setColour("buttonColourDark")
            #recieving port cannot be the sending port
            if data.sendingPort == getRouterAt(mx, my):
                data.sendingPort = 0
            data.recievingPort = getRouterAt(mx, my)
            data.recievingPort.setColour("buttonTextColour")
        data.selectingRecievingPort = False


### VISUALS ###
def centreNetwork():
    #aesthetic method to move the network to the centre of the screen
    farthestLeft = width
    farthestRight = 0
    lowest = height
    highest = 0
    for router in routers:
        if router.center[0] < farthestLeft:
            farthestLeft = router.center[0]
        if router.center[0] > farthestRight:
            farthestRight = router.center[0]
        if router.center[1] < lowest:
            lowest = router.center[1]
        if router.center[1] > highest:
            highest = router.center[1]
    screenCentreX = width / 2
    screenCentreY = height / 2
    xOffset = (farthestRight + farthestLeft) / 2 - screenCentreX
    yOffset = (highest + lowest) / 2 - screenCentreY
    for router in routers:
        router.setCoordinates(router.center[0] - xOffset,
                              router.center[1] - yOffset)

    for connection in connections:
        connection.moveStart(connection.start[0] - xOffset,
                             connection.start[1] - yOffset)
        connection.moveEnd(connection.end[0] - xOffset,
                           connection.end[1] - yOffset)

def darkenNetwork():
    for router in routers:
        router.setColour("buttonColourDark")
        
    for connection in connections:
        connection.turnBlack()

def highlight(nodeList):
    darkenNetwork()
    for node in nodeList:
        for router in routers:
            if node == router.id:
                router.setColour("buttonTextColour")
    for connection in connectionsFromNodes(nodeList):
        connection.setColour("buttonTextColour")
    
def drawNetwork():
    #draw all lines
    for connection in connections:
        pygame.draw.line(screen, connection.colour, connection.start,
                         connection.end, 2)
        ### TODO: use Network function:
        #                   getWeight(connection.a, connection.b)
        text(str(connection.weight), theme.lightFont, 15,
             currentStyle.get("buttonColourLight"),
             (connection.start[0] + connection.end[0]) / 2,
             (connection.start[1] + connection.end[1]) / 2)

    #draw all routers
    i = 0
    for router in routers:
        pygame.draw.circle(router.surface, router.colour, router.center,
                           router.radius)
        text(str(router.id), theme.lightFont, 15,
             currentStyle.get("titleColour"), router.center[0] - 5,
             router.center[1] - 5)
        i = i + 1

    #draw unfinished connection line
    if data.drawingConnection and data.routerSelected and data.routerA != 0:
        pygame.draw.line(screen, (100, 100, 100), data.routerA.center,
                         pygame.mouse.get_pos())

    if data.choosingConnectionWeight:
        if not data.reassigningWeight:
            pygame.draw.line(screen, (0, 0, 0), data.routerA.center,
                         data.routerB.center, 2)
        if data.weightTextBox is False:
            data.weightTextBox = TextBox(
                (data.routerA.center[0] + data.routerB.center[0]) // 2,
                (data.routerA.center[1] + data.routerB.center[1]) // 2, 40, 30,
                20)

        data.weightTextBox.process()

def displayTrace(nodes, description):
    highlight(nodes)
    text("Step " + str(data.step + 1) + ". " + description, theme.medFont, int(0.015 * width), currentStyle.get("buttonColourDark"), width * 0.2, height * 0.25)
    
### ANIMATION ###
def formAnimation(nodeIDs):
    #turns list of node id's into an animation
    #Get router object references from ids
    animationRouters.clear()
    animationConnections.clear()
    for nodeID in nodeIDs:
        for router in routers:
            if router.id == nodeID:
                animationRouters.append(router)
                break

    #get connection object references from routers, count weight totals
    for i in range(1, len(animationRouters)):
        for connection in connections:
            if connection.start == animationRouters[
                    i -
                    1].center or connection.end == animationRouters[i -
                                                                    1].center:
                if connection.start == animationRouters[
                        i].center or connection.end == animationRouters[
                            i].center:
                    animationConnections.append(connection)
                    data.stepByStepWeight.append(data.stepByStepWeight[-1] +
                                                 connection.weight)
                    #duplicate each step's weight for the animation
                    data.stepByStepWeight.append(data.stepByStepWeight[-1])
                    break

def animate():
    #run animation with 1s per stage
    #at each stage, light up the next step, darken the last
    length = len(animationConnections) + len(animationRouters)
    if length > 1:
        stage = int(time.time()) % length
        if stage == 0:
            animationRouters[len(animationRouters) -
                             1].setColour("buttonColourDark")
            animationConnections[-1].turnBlack()
        if stage % 2 == 0:
            animationRouters[int(stage / 2)].setColour("buttonTextColour")
            animationConnections[(int(stage / 2)) - 1].turnBlack()
        else:
            animationRouters[int(
                (stage - 1) / 2)].setColour("buttonColourDark")
            animationConnections[int(
                (stage - 1) / 2)].setColour("buttonTextColour")
        text("Current total weight: " + str(data.stepByStepWeight[stage]),
             theme.medFont, int(0.015 * width),
             currentStyle.get("buttonColourLight"), width * 0.6, height * 0.25)
        
def stopAnimation():
    for router in routers:
            router.setColour("buttonColourDark")
    for connection in connections:
            connection.turnBlack()
    data.runAnimation = False


### NETWORK METHODS ###
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

def removeRouter(r):
    removeAllConnectionsOfRouter(r)
    i = 0
    for node in routers:
        if node == r:
            network.removeNode(r.id)
            routers.pop(i)
            if data.sendingPort == r:
                data.sendingPort = 0
            if data.recievingPort == r:
                data.recievingPort = 0
            break
        i = i + 1

def connectionsFromNodes(nodeList):
    routerList = []
    for nodeID in nodeList:
        for router in routers:
            if router.id == nodeID:
                routerList.append(router)
                break
            
    connectionList = []
    for i in range(1, len(nodeList)):
        for connection in connections:
            if connection.start == routerList[i-1].center or connection.end == routerList[i - 1].center:
                if connection.start == routerList[i].center or connection.end == routerList[i].center:
                    connectionList.append(connection)
                    break
    return connectionList

def finalizeNewConnection(connWeight):
    conIcon = ConnectionIcon(data.routerA.center[0], data.routerA.center[1],
                             data.routerB.center[0], data.routerB.center[1])
    conIcon.weight = connWeight
    connections.append(conIcon)
    conIcon.addIDs(data.routerA.id, data.routerB.id)
    ### ADD CONNECTIONS ###
    data.routerA.connections.append(data.routerB)
    data.routerB.connections.append(data.routerA)

    if data.routerA.id < data.routerB.id:
        network.addLink([data.routerA.id, data.routerB.id, connWeight])
    else:
        network.addLink([data.routerB.id, data.routerA.id, connWeight])
    data.refresh()

def assignWeight(connWeight):
    data.connectionA.weight = connWeight
    network.setWeight(data.routerA.id, data.routerB.id, connWeight)
    data.refresh()

### STATES ###
def setupState():
    #get user input on routers, state=True
    #Start by adding buttons
    if not data.stateSetupDone:
        fontSize = int(width * 0.013)
        buttons.extend([
            Button(width * 0.04, height * 0.18, width * 0.12, height * 0.05,
                   fontSize, 'ADD ROUTER', addRouter),
            Button(width * 0.19, height * 0.18, width * 0.13, height * 0.05,
                   fontSize, 'ADD CONNECTION', addConnection),
            Button(width * 0.34, height * 0.18, width * 0.13, height * 0.05,
                   fontSize, 'RANDOMIZE DATA', randomizeNetwork),
            Button(width * 0.49, height * 0.18, width * 0.13, height * 0.05,
                   fontSize, 'CLEAR NETWORK', clearData),
            Button(width * 0.64, height * 0.18, width * 0.13, height * 0.05,
                   fontSize, 'PRINT DEBUG', printDebug),
            Button(width * 0.4, height * 0.8, width * 0.2, height * 0.05,
                   fontSize, 'USE THIS DATA', toggleState)
        ])
        data.stateSetupDone = True

    #drawing panel
    pygame.draw.rect(screen, (255, 255, 255),
                     (width * 0.04, height * 0.25, width * 0.92, height * 0.5))

    #Tell user if they're drawing router/connection, otherwise display default text
    if data.drawingRouter:
        text("DRAWING ROUTERS - click anywhere. Escape to cancel", theme.medFont,
             int(0.015 * width), currentStyle.get("buttonColourDark"),
             width * 0.04, height * 0.25)
    elif data.drawingConnection:
        text("DRAWING CONNECTION - click the source then the destination",
             theme.medFont, int(0.015 * width),
             currentStyle.get("buttonColourDark"), width * 0.04, height * 0.25)
    elif data.choosingConnectionWeight:
        text(
            "type in connection weight (0-100 allowed), then press enter to confirm. Press escape to cancel",
            theme.medFont, int(0.015 * width),
            currentStyle.get("buttonColourDark"), width * 0.04, height * 0.25)
    else:
        text("hint: right-click to remove a router/connection", theme.medFont,
             int(0.015 * width), currentStyle.get("buttonColourDark"),
             width * 0.04, height * 0.25)
    drawNetwork()
    
def traceState():
    #main state, algoritms performed on router data, state=False
    if not data.stateSetupDone:
        fontSize = int(width * 0.013)
        buttons.extend([
            Button(width * 0.04, height * 0.18, width * 0.12, height * 0.05,
                   fontSize, 'SENDING PORT', selectSendPort),
            Button(width * 0.19, height * 0.18, width * 0.14, height * 0.05,
                   fontSize, 'TOGGLE ALGORITHM', selectAlgorithm),
            Button(width * 0.36, height * 0.18, width * 0.12, height * 0.05,
                   fontSize, 'RECIEVING PORT', selectRecievePort),
            Button(width * 0.51, height * 0.18, width * 0.2, height * 0.05,
                   fontSize, 'CHANGE ROUTER DATA', toggleState),
            Button(width * 0.6, height * 0.8, width * 0.2, height * 0.05,
                   fontSize, 'RUN ALGORITHM', runAlgorithm)
        ])
        centreNetwork()
        data.stateSetupDone = True
        
            

    #drawing panel
    pygame.draw.rect(screen, (255, 255, 255),
                     (width * 0.04, height * 0.25, width * 0.92, height * 0.5))

    #display selected ports, algorithm
    if data.sendingPort == 0:
        sendID = "not selected"
    else:
        sendID = str(data.sendingPort.id)
    if data.recievingPort == 0:
        recieveID = "not selected"
    else:
        recieveID = str(data.recievingPort.id)
    text("Sending port: " + sendID, theme.medFont, int(0.015 * width),
         currentStyle.get("buttonTextColour"), width * 0.04, height * 0.77)
    text("Recieving port: " + recieveID, theme.medFont, int(0.015 * width),
         currentStyle.get("buttonTextColour"), width * 0.04, height * 0.8)
    text("Algorithm: " + data.selectedAlgorithm, theme.medFont,
         int(0.015 * width), currentStyle.get("buttonTextColour"),
         width * 0.04, height * 0.83)
    if data.selectingSendingPort:
        text("SELECTING SENDING PORT - click on a router", theme.medFont,
             int(0.015 * width), currentStyle.get("buttonColourDark"),
             width * 0.04, height * 0.25)
    if data.selectingRecievingPort:
        text("SELECTING RECIEVING PORT - click on a router", theme.medFont,
             int(0.015 * width), currentStyle.get("buttonColourDark"),
             width * 0.04, height * 0.25)
        
    if data.algorithmDone and data.step < len(data.traceDescription) -1:
        #Issue: traceDescription = []
        displayTrace(data.traceList[data.step], data.traceDescription[data.step])

    if data.runAnimation:
        animate()

    drawNetwork()

### ADD ALL VISUALS TO SCREEN ###
def draw():
    screen.blit(
        pygame.transform.smoothscale(currentStyle.get("background"),
                                     (width, height)), (0, 0))
    centreText("CPS706 PROJECT", theme.medFont, int(width * 0.05),
               currentStyle.get("titleColour"), height * 0.1)
    centreText("BY SEAN ADLAM, MAEVE FITZGERALD, RACHELLE RODIN, GRAHAM ROEBUCK AND RUDABA SYED", theme.medFont, int(0.013 * width),
         currentStyle.get("titleColour"), height * 0.16)

    if data.state:
        setupState()
    else:
        traceState()

    for object in buttons:
        object.process()


### GAME LOOP ###
data = Data()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            # There's some code to add back window content here.
            oldwidth = width
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
            windowScaleRatio = width / oldwidth
            for router in routers:
                router.radius *= windowScaleRatio
                router.center = (router.center[0]*windowScaleRatio, router.center[1]*windowScaleRatio)
            for connection in connections:
                connection.start = connection.startRouter.center
                connection.end = connection.endRouter.center
            data.stateSetupDone = False
            buttons.clear()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  #left click
                if findClickedButton():  #try regardless of state. Advance to next event if true.
                    continue
                mx, my = event.pos  #mouse position
                if data.state and onDrawingArea(mx, my):  #case: setup state
                    handleSetupLDown(mx, my)
                elif not data.state:  #case: trace state
                    handleTraceLDown(mx, my)
            elif (event.button == 3 and data.state 
                and not data.choosingConnectionWeight):  #right click only used in setup state
                mx, my = event.pos
                removeConnectionAtPoint(mx, my)
                if isClickingRouter():
                    r = getRouterAt(mx, my)
                    removeRouter(r)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                data.draggingRouter = False
        if event.type == pygame.MOUSEMOTION and not data.draggingRouter is False:
            mx, my = event.pos
            if onDrawingArea(mx, my):
                data.draggingRouter.center = event.pos
                for connection in connections:
                    if data.draggingRouter is connection.startRouter:
                        connection.start = data.draggingRouter.center
                    elif data.draggingRouter is connection.endRouter:
                        connection.end = data.draggingRouter.center
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and data.state: #undo any in progess setup action
                data.refresh()
            elif not data.weightTextBox is False:
                if event.key == pygame.K_RETURN:
                    if data.weightTextBox.validateText():
                        if data.reassigningWeight:
                            assignWeight(int(data.weightTextBox.text))
                        else:
                            finalizeNewConnection(int(data.weightTextBox.text))
                elif event.key == pygame.K_BACKSPACE:
                    data.weightTextBox.backSpace()
                else:
                    data.weightTextBox.appendChar(event.unicode)
            
    draw()
    pygame.display.update()
    #fpsClock.tick(fps)