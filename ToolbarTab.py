from cmu_graphics import *

class ToolbarTab:
    def __init__(self, x, y, category, isActive=False):
        self.x = x
        self.y = y
        self.width = 180
        self.height = 30
        self.category = category
        self.isActive = isActive
        
    def drawUI(self):
        drawRect(self.x, self.y, self.width, self.height, 
                fill='black' if self.isActive else 'white',
                border='black')
        drawLabel(self.category, 
                 self.x + self.width/2, 
                 self.y + self.height/2, 
                 fill='white' if self.isActive else 'black')
    
    def hitTest(self, mouseX, mouseY):
        return (self.x <= mouseX <= self.x + self.width and 
                self.y <= mouseY <= self.y + self.height)