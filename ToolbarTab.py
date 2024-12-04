from cmu_graphics import *

class ToolbarTab:
    def __init__(self, x, y, category, isActive=False):
        self.x = x
        self.y = y
        self.width = 180
        self.height = 30
        self.category = category
        self.isActive = isActive
        self.isHovering = False
        
    def drawUI(self):
        if self.isActive:
            bgColor, textColor = 'black', 'white'
        else:
            if self.isHovering:
                bgColor, textColor = rgb(78,78,78), 'white'
            else:
                bgColor, textColor = 'white', 'black'
        
        drawRect(self.x, self.y, self.width, self.height, 
                fill=bgColor,
                border='black')
        drawLabel(self.category, 
                 self.x + self.width/2, 
                 self.y + self.height/2, 
                 fill=textColor)
    
    def hitTest(self, mouseX, mouseY):
        return (self.x <= mouseX <= self.x + self.width and 
                self.y <= mouseY <= self.y + self.height)