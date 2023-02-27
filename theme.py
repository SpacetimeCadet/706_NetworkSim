import pygame

pygame.init()

#style: 1 = teal theme, network background, 2 = blue theme, spiral background
style = 1

#fonts (may cut down, depending on final design)
lightFont = 'NeueMachina-Light.otf'
medFont = 'NeueMachina-Regular.otf'
boldFont = 'NeueMachina-Ultrabold.otf'

def currentTheme():
#Colours
    if style == 1:
        return { 
            "buttonColourDark" : (7, 13, 41),
            "buttonColourLight" : (15, 31, 90),
            "titleColour" : (243, 244, 244),
            "buttonTextColour" : (18, 255, 185),
            "tableHeaderColour" : (18, 255, 185),
            "tableContentColour" : (18, 255, 185),
            "background" : pygame.image.load("tealBackground.png")
        }

    else:
        return {
            "buttonColourDark" : (8, 15, 43),
            "buttonColourLight" : (17, 32, 89),
            "titleColour" : (243, 244, 244),
            "buttonTextColour" : (65, 184, 213),
            "tableHeaderColour" : (65, 184, 213),
            "tableContentColour" : (88, 135, 255),
            "background" : pygame.image.load("blueBackground.png")
        }

