#this file defines the routerNode class

class routerNode:
    def __init__(self):
        """
        () -> object with set attributes
        
        This function is a constructor for the class. We use built in function
        "__init__" to set the attributes for objects of the class routerNode.
        
        So the class routerNode has the attributes cost and pred and it is 
        setting them with default values infinity for the cost and an empty list
        for pred.
        
        """
        self.cost = float('inf')
        self.pred = []
        
        
    def updateCost(self, givenCost):
        """
        Sets the cost attribute for an object of the routerNode class. 
        """
        self.cost = givenCost
        
    def updatePred(self, givenPred):
        """
        Sets the cost attribute for an object of the routerNode class. 
        """
        self.pred = givenPred
        
    def getCost (self):
        """
        Return the value of the cost attribute of the object
        """
        return self.cost
    
    def getPred(self):
        """
        Return the value of the predessor attribute of the object
        """
        return self.pred
       
