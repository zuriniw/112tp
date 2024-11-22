from cmu_graphics import *

class Toggle:
    def __init__(self, app, x, y, name, isOn):
        self.x, self.y = x, y
        self.name = name
        self.isOn = isOn
        self.toggleX, self.toggleY = x, y + app.textHeight + app.paddingY/4
    
    def drawUI(self):
        drawRect(self.toggleX, self.toggleY, app.toggleWidth, app.toggleHeight, border = 'black', fill = 'white')
        drawLabel(self.name, self.x+ app.toggleWidth / 2, self.y )
        toggleHandlerWidth = 20
        if not self.isOn:
            for i in range(app.toggleWidth // 5):
                x0 = self.toggleX + i * 5
                drawLine(x0,self.toggleY,x0,self.toggleY + app.toggleHeight)
            drawRect(self.toggleX, self.toggleY-3, toggleHandlerWidth, app.toggleHeight+6, border = 'black', fill = 'white') 
        else:
            drawRect(self.toggleX + app.toggleWidth - toggleHandlerWidth, self.toggleY-3, toggleHandlerWidth, app.toggleHeight+6, border = 'black', fill = 'black')
            
            
    def hitTest(self, mouseX, mouseY):
        return self.toggleX < mouseX < self.toggleX + app.toggleWidth and self.toggleY < mouseY < self.toggleY + app.toggleHeight


