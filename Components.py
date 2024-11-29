from cmu_graphics import *
from Node import *
########################################################################################
# COMPONENT is the most basic class of compo: 
#       - set the birthplace
#       - detect mouse hit
########################################################################################
class Component:
    def __init__(self, app):  # Added default width and height
        self.app = app
        self.x = app.width / 2
        self.y = app.height / 2
        self.inputNodes = []
        self.outputNodes = []
        self.isDragging = False
        self.isSelected = False
        self.isPinned = False
        self.updateNodePositions()

    def updateNodePositions(self):
        for node in self.inputNodes + self.outputNodes:
            node.updatePosition()

    def hitTest(self, mouseX, mouseY):
        return (self.x <= mouseX <= self.x + self.width) and (self.y <= mouseY <= self.y + self.height)

    def deleteComponent(self, app):
        # 1. clear connections
        for node in self.inputNodes + self.outputNodes:
            for conn in node.connections[:]:
                conn.deleteConnection(app)
        
        # 2. remove compo from app
        if self in app.components:
            app.components.remove(self)
        
        if self.isPinned:
            for s in app.pinnedSliders:
                if s.original_slider == self:
                    app.pinnedSliders.remove(s)



########################################################################################
# TYPICAL COMPONENT 
#       template typical component UI drawing, with input, centered label, and output    
#       initialize input and output Nodes as lists
########################################################################################

class TypicleComponent(Component):
    def __init__(self, app, inputs, outputs, name):
        super().__init__(app)
        self.name = name

        self.inputs = inputs
        self.outputs = outputs
        self.inputNodes = [Node(inputName, self, False) for inputName in self.inputs]
        self.outputNodes = [Node(outputName, self, True) for outputName in self.outputs]
        
        self.centerLabelWidth = app.centerLabelWidth
        self.inputWidth = app.textWidth * max(len(inp) for inp in self.inputs) if inputs else 0
        self.outputWidth = app.textWidth * max(len(output) for output in self.outputs) if outputs else 0
        self.inputHeight = (app.textHeight + app.paddingY) * len(self.inputs) - app.paddingY
        self.outputHeight = (app.textHeight + app.paddingY) * len(self.outputs) - app.paddingY
        self.height = max(self.inputHeight, self.outputHeight) + app.paddingY * 2 + app.borderY * 2
        self.width = app.paddingX * 2 + app.borderX * 2 + self.centerLabelWidth + self.inputWidth + self.outputWidth
        self.updateNodePositions()
        self.inputDefaultValue = {}
        
    def drawUI(self):
        ###### Draw Nodes ######
        for node in self.inputNodes + self.outputNodes:
            if node.name != '':
                node.drawNode()

        ####### Draw Background #######
        drawRect(self.x, self.y, self.width, self.height, fill='white' if not self.isSelected else 'lightGrey', border='black')

        ####### Draw Input Label #######
        y_input = self.y + (self.height - self.inputHeight) / 2 + app.borderY/2
        for i, inputLabel in enumerate(self.inputs):
            x_input = self.x + app.borderX + self.inputWidth / 2
            drawLabel(inputLabel, x_input, y_input)
            y_input += app.textHeight + app.paddingY

        ####### Draw Center Label #######
        centerColor = 'darkGrey' if self.isGeo and not self.isDisplay else 'black'

        labelLines = self.name.split('\n')
        labelHeight = len(labelLines) * (app.textHeight + app.paddingY / 2) - app.paddingY / 2
        labelStartX = self.x + app.borderX + self.inputWidth + app.paddingX
        drawRect(labelStartX, self.y + app.borderY/2, app.centerLabelWidth, self.height - app.borderY, border='black', fill = centerColor)
        labelX = labelStartX + app.centerLabelWidth / 2
        labelY = self.y + self.height / 2 - labelHeight / 2 + app.borderY/2
        for line in labelLines:
            drawLabel(line, labelX, labelY, fill='white', font = 'symbols')
            labelY += app.textHeight + app.paddingY / 8



        ###### Draw Output Label ######
        y_output = self.y + (self.height - self.outputHeight) / 2 + app.borderY/2
        for outputLabel in self.outputs:
            outputX = self.x + (app.borderX + self.inputWidth + app.paddingX + app.centerLabelWidth + app.paddingX) + self.outputWidth / 2
            drawLabel(outputLabel, outputX, y_output)
            y_output += app.textHeight + app.paddingY


    def getDefaultValue(self, nodeName):
        return self.inputDefaultValue.get(nodeName)

    def updateValue(self, nodeName, value):
        for node in self.inputNodes:
            if node.name == nodeName:
                node.value = value
                break
        
        self.hasAllInputs = all(node.value is not None for node in self.inputNodes)
        if self.hasAllInputs:
            output_values = self.calculate()
            if output_values:
                for node, value in zip(self.outputNodes, output_values):
                    node.value = value

