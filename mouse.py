import pygame
pygame.init()

class Mouse:
    #debouncing. Basically a "on mouse button up" controller
    def __init__(self):
        self.lastLeftState = False
        self.currentLeftState = False
        self.lastRightState = False
        self.currentRightState = False
        self.isLeftClicking = False
        self.isRightClicking = False
    
    def update(self):
        self.lastLeftState = self.currentLeftState
        self.currentLeftState = pygame.mouse.get_pressed()[0]
        self.lastRightState = self.currentRightState
        self.currentRightState = pygame.mouse.get_pressed()[2]
        
        self.isLeftClicking = self.lastLeftState and not self.currentLeftState
        self.isRightClicking = self.lastRightState and not self.currentRightState