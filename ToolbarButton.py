from cmu_graphics import *
class ToolbarButton:
    def __init__(self, app, x, y, component):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 60
        self.component = component
        self.isHovering = False
        self.isSelected = False
        
        # Create preview instance
        self.preview = component(app)
    
    def drawUI(self):
        # Set colors based on state
        bgColor = 'black' if self.isHovering else 'white'
        textColor = 'white' if self.isHovering else 'black'
        if self.isSelected:
            bgColor = 'grey'
            textColor = 'black'
            
        # Draw background
        drawRect(self.x, self.y, self.width, self.height, 
                border='black', fill=bgColor)
        
        # Draw label using preview's name
        labelLines = self.preview.name.split('\n')
        dy = 0
        for line in labelLines:
            drawLabel(line, 
                     self.x + self.width/2, 
                     self.y + dy + app.borderY, 
                     font='symbols', 
                     fill=textColor)
            dy += app.textHeight + app.paddingY / 4
    
    def hitTest(self, mouseX, mouseY):
        return (self.x <= mouseX <= self.x + self.width) and (self.y <= mouseY <= self.y + self.height)
