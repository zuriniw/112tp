from cmu_graphics import *

class Components:
    def __init__(self, app):
        self.width, self.height = 160, 200
        self.x = app.width/2
        self.y = app.height/2
        self.inputNodes = []
        self.outputNodes = []
        self.isDragging = False
        self.updateNodePositions()

    def updateNodePositions(self):
        for node in self.inputNodes + self.outputNodes:
            node.updatePosition()

    def hitTest(self, mouseX, mouseY):
        return (self.x <= mouseX <= self.x + self.width) and (self.y <= mouseY <= self.y + self.height)

class Node:
    def __init__(self, name, component, isOutput, data):
        self.name = name
        self.component = component
        self.isOutput = isOutput
        self.data = data
        self.isHovering = False
        self.x, self.y = 0, 0  # Initialize with default values
        self.r = 5

    def updatePosition(self):
        if self.isOutput:
            index = self.component.outputNodes.index(self)
            self.x = self.component.x + self.component.width
            self.y = self.component.y + self.component.height / 2 - self.component.outputHeight / 2 + index * (self.component.paddingY + self.component.textHeight) + self.component.textHeight
        else:
            index = self.component.inputNodes.index(self)
            self.x = self.component.x
            self.y = self.component.y + self.component.borderY + index * (self.component.paddingY + self.component.textHeight)

    def drawNode(self):
        drawCircle(self.x, self.y, self.r, fill='black' if self.isHovering else 'white', border='black')

    def hitTest(self, mouseX, mouseY):
        return (self.x - self.r <= mouseX <= self.x + self.r) and (self.y - self.r <= mouseY <= self.y + self.r)

class TypicleComponent(Components):
    def __init__(self, app, inputs, outputs, name):
        super().__init__(app)
        self.inputs = inputs
        self.outputs = outputs
        self.name = name
        self.paddingX, self.paddingY, self.borderX, self.borderY, self.textHeight, self.textWidth = app.paddingX, app.paddingY, app.borderX, app.borderY, app.textHeight, app.textWidth 
        self.centerLabelWidth = app.centerLabelWidth
        self.inputWidth = self.textWidth * max(len(inp) for inp in self.inputs)
        self.outputWidth = self.textWidth * max(len(output) for output in self.outputs)
        self.inputHeight = (self.textHeight + self.paddingY) * len(self.inputs) - self.paddingY
        self.outputHeight = (self.textHeight + self.paddingY) * len(self.outputs) - self.paddingY
        self.width = self.paddingX * 2 + self.borderX * 2 + self.centerLabelWidth + self.inputWidth + self.outputWidth
        self.height = max(self.inputHeight, self.outputHeight) + self.paddingY
        self.inputNodes = [Node(input, self, False, None) for input in self.inputs]
        self.outputNodes = [Node(output, self, True, None) for output in self.outputs]
        self.updateNodePositions()

    def drawUI(self):
        # Draw nodes
        for node in self.inputNodes + self.outputNodes:
            node.drawNode()

        # Draw background
        drawRect(self.x, self.y, self.width, self.height, fill='white', border='black')

        # Draw inputs
        y_input = self.y + self.borderY
        for i, inputLabel in enumerate(self.inputs):
            x_input = self.x + self.borderX + self.inputWidth / 2
            drawLabel(inputLabel, x_input, y_input)
            y_input += self.textHeight + self.paddingY

        # Draw center label
        labelLines = self.name.split('\n')
        labelHeight = len(labelLines) * (self.textHeight + self.paddingY / 2) - self.paddingY / 2
        labelStartX = self.x + self.borderX + self.inputWidth + self.paddingX
        drawRect(labelStartX, self.y + self.borderY, self.centerLabelWidth, self.height - self.borderY * 2, border='black')
        labelX = labelStartX + self.centerLabelWidth / 2
        labelY = self.y + self.height / 2 - labelHeight / 2
        for line in labelLines:
            drawLabel(line, labelX, labelY, fill='white')
            labelY += self.textHeight + self.paddingY / 2

        # Draw outputs
        y_output = self.y + (self.height - self.outputHeight) / 2 + self.textHeight
        for outputLabel in self.outputs:
            outputX = self.x + (self.borderX + self.inputWidth + self.paddingX + self.centerLabelWidth + self.paddingX) + self.outputWidth / 2
            drawLabel(outputLabel, outputX, y_output)
            y_output += self.textHeight + self.paddingY

class CircleCreator(TypicleComponent):
    def __init__(self, app):
        inputs = ['x', 'y', 'radius', '1', '2', '3']
        outputs = ['theCircle', '1']
        name = 'Draw\nCirc\n●'
        super().__init__(app, inputs, outputs, name)

class RectCreator(TypicleComponent):
    def __init__(self, app):
        inputs = ['x', 'y', 'width', 'height', '1', '2', '3']
        outputs = ['theRect']
        name = 'Draw\nRect\n█'
        super().__init__(app, inputs, outputs, name)


class InteractablePart:
    def __init__(self, app, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h

    def hitTest(self, mouseX, mouseY):
        return (self.x <= mouseX <= self.x + self.width) and (self.y <= mouseY <= self.y + self.height)
    
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

