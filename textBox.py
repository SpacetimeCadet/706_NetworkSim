#coolcool
import pygame
import theme
pygame.init()

height = 600
width = 1200
size = [width, height]
screen = pygame.display.set_mode(size)
charLimit = 3
weightLimit = 100

class TextBox():

    def __init__(self, x, y, width, height, fontSize):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fontSize = fontSize
        self.text = ""
        self.currentStyle = theme.currentTheme()
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.textSurface = pygame.Surface((self.width, self.height))
        self.font = pygame.font.Font(theme.medFont, int(self.fontSize))
        
    def process(self):
        self.surface.fill(self.currentStyle.get("buttonTextColour"))
        self.surface.blit(self.font.render(self.text, True, self.currentStyle.get("buttonColourDark")), 
                                            [self.width / 5,
                                            self.height / 5 
                                            ])
        screen.blit(self.surface, self.rect)
    
    def appendChar(self, newChar):
        if len(self.text) < charLimit:
            self.text += newChar

    def backSpace(self):
        if len(self.text) > 0:
            self.text = self.text[:-1]
    
    def validateText(self):
        if len(self.text) > 0 and self.text.isnumeric and int(self.text) <= weightLimit:
            return int(self.text)
        return False
