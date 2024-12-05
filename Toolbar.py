'''
- Component
    - TypicleComponent
        - Distance
'''
from cmu_graphics import *

########################################################################################  
# TOOLBAR
#   1. shelf of toolbar button
########################################################################################

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
        
        drawRect(self.x, self.y, self.width, self.height, fill=bgColor,border='black')
        drawLabel(self.category, self.x + self.width/2, self.y + self.height/2, fill=textColor)
    
    def hitTest(self, mouseX, mouseY):
        return (self.x <= mouseX <= self.x + self.width and self.y <= mouseY <= self.y + self.height)
    
########################################################################################  
# TOOLBAR BUTTON
#   1. make component Drag-&-Drop creating
########################################################################################

class ToolbarButton:
    def __init__(self, app, x, y, component):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 60
        self.component = component
        self.isHovering = False
        self.isSelected = False
        
        # Create preview instance
        self.preview = component(app)
    
    def drawUI(self):
        # Set colors based on state
        bgColor = rgb(78,78,78) if self.isHovering else 'white'
        textColor = 'white' if self.isHovering else 'black'
        if self.isSelected:
            bgColor = 'grey'
            textColor = 'black'
            
        # Draw background
        drawRect(self.x, self.y, self.width, self.height, border='black', fill=bgColor)
        
        # Draw label using preview's name
        labelLines = self.preview.name.split('\n')
        dy = 0
        for line in labelLines:
            drawLabel(line, self.x + self.width/2, self.y + dy + app.borderY, font='symbols', fill=textColor)
            dy += app.textHeight + app.paddingY / 4
    
    def hitTest(self, mouseX, mouseY):
        return (self.x <= mouseX <= self.x + self.width) and (self.y <= mouseY <= self.y + self.height)
