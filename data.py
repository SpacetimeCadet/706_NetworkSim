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
        self.selectingSendingPort = False
        self.sendingPort = 0
        self.selectingRecievingPort = False
        self.recievingPort = 0
        self.selectedAlgorithm = "Dijsktra"
        self.runAnimation = False

    def toggleAlgorithm(self):
        if self.selectedAlgorithm == "Dijsktra":
            self.selectedAlgorithm = "Bellman-Ford"
        else:
            self.selectedAlgorithm = "Dijsktra"

    def refresh(self):
        self.state = True
        self.stateSetupDone = False
        self.drawingRouter = False
        self.drawingConnection = False
        self.routerSelected = False
        self.routerA = 0
        self.routerB = 0
        self.selectingSendingPort = False
        self.sendingPort = 0
        self.selectingRecievingPort = False
        self.recievingPort = 0
        self.runAnimation = False