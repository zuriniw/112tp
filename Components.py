from cmu_graphics import *

class Components:
    def __init__(self, app):
        self.width, self.height = 40, 200
        self.x = app.nodeZoneMidX
        self.y = app.height/2
        self.isDragging = False

    def hitTest(self, mouseX, mouseY):
        return (self.x <= mouseX <= self.x + self.width) and (self.y <= mouseY <= self.y + self.height)

class TypicleComponent(Components):
    def __init__(self, app):
        super().__init__(app)

    def drawUI(self):
        drawRect(self.x, self.y, self.width, self.height, fill='lightgrey')
        for input in self.inputs:
            dy = 10
            drawLabel(input, self.x, self.y + dy)
            dy += 50
        for output in self.outputs:
            dy = 10
            drawLabel(output, self.x + self.width - 50, self.y + dy)
            dy += 50

class CircleCreator(TypicleComponent):
    def __init__(self, app):
        super().__init__(app)
        self.inputs = ['x', 'y', 'radius']
        self.outputs = ['theCircle']

class Slider(Components):
    def __init__(self, app):
        super().__init__(app)
        self.value = 50  # Initial slider value
        self.width = 200
        self.height = 40

    def drawUI(self):
        drawRect(self.x, self.y, self.width, self.height, fill='lightgrey')
        handleX = self.x + (self.value / 100) * self.width
        drawRect(handleX - 5, self.y, 10, self.height, fill='darkgrey')
