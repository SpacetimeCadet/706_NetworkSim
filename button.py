import pygame
import theme
pygame.init()

height = 600
width = 1200
size = [width, height]
screen = pygame.display.set_mode(size)

class Button():

    def __init__(self, x, y, width, height, fontSize, buttonText, onclickFunction):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.currentStyle = theme.currentTheme()
        self.buttonSurf = pygame.font.Font(theme.medFont, fontSize).render(buttonText, True, self.currentStyle.get("buttonTextColour"))
        self.mouseHover = False

    def process(self):
        mousePos = pygame.mouse.get_pos()
        #self.buttonOutline.fill(buttonTextColour)
        
        if self.buttonRect.collidepoint(mousePos):
            self.mouseHover = True
            self.buttonSurface.fill( self.currentStyle.get("buttonColourLight"))
        else:
            self.mouseHover = False
            self.buttonSurface.fill(self.currentStyle.get("buttonColourDark"))

        #outline -needs fixing
        pygame.draw.rect(self.buttonSurface,  self.currentStyle.get("buttonTextColour"),
                         (self.x, self.y, self.width, self.height), 3)

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)
