from cmu_graphics import *

class Component:
    def __init__(self, app):
        self.width, self.height = 160, 200
        self.x = app.width/2
        self.y = app.height/2
        self.inputNodes = []
        self.outputNodes = []
        self.isDragging = False
        self.isSelected = False
        self.updateNodePositions()

    def updateNodePositions(self):
        for node in self.inputNodes + self.outputNodes:
            node.updatePosition()
            if hasattr(self, 'preview'):  # For preview components
                self.preview.x = self.x
                self.preview.y = self.y
                self.preview.updateNodePositions()

    def hitTest(self, mouseX, mouseY):
        return (self.x <= mouseX <= self.x + self.width) and (self.y <= mouseY <= self.y + self.height)

class TypicleComponent(Component):
    def __init__(self, app, inputs, outputs, name):
        super().__init__(app)
        self.inputs = inputs
        self.outputs = outputs
        self.name = name
    
        self.centerLabelWidth = app.centerLabelWidth
        self.inputWidth = app.textWidth * max(len(inp) for inp in self.inputs)
        self.outputWidth = app.textWidth * max(len(output) for output in self.outputs)
        self.inputHeight = (app.textHeight + app.paddingY) * len(self.inputs) - app.paddingY
        self.outputHeight = (app.textHeight + app.paddingY) * len(self.outputs) - app.paddingY
        self.height = max(self.inputHeight, self.outputHeight) + app.paddingY * 2 + app.borderY * 2
        self.width = app.paddingX * 2 + app.borderX * 2 + self.centerLabelWidth + self.inputWidth + self.outputWidth
        self.inputNodes = [Node(input, self, False, None) for input in self.inputs]
        self.outputNodes = [Node(output, self, True, None) for output in self.outputs]
        self.updateNodePositions()

    def drawUI(self):
        # Draw nodes
        for node in self.inputNodes + self.outputNodes:
            if node.name != '':
                node.drawNode()

        # Draw background
        drawRect(self.x, self.y, self.width, self.height, fill='white' if not self.isSelected else 'lightGrey', border='black')

        # 调整输入标签的绘制位置以居中
        y_input = self.y + (self.height - self.inputHeight) / 2 + app.borderY/2
        for i, inputLabel in enumerate(self.inputs):
            x_input = self.x + app.borderX + self.inputWidth / 2
            drawLabel(inputLabel, x_input, y_input)
            y_input += app.textHeight + app.paddingY

        # Draw center label
        labelLines = self.name.split('\n')
        labelHeight = len(labelLines) * (app.textHeight + app.paddingY / 2) - app.paddingY / 2
        labelStartX = self.x + app.borderX + self.inputWidth + app.paddingX
        drawRect(labelStartX, self.y + app.borderY/2, app.centerLabelWidth, self.height - app.borderY, border='black')
        labelX = labelStartX + app.centerLabelWidth / 2
        labelY = self.y + self.height / 2 - labelHeight / 2 + app.borderY/2
        for line in labelLines:
            drawLabel(line, labelX, labelY, fill='white', font = 'symbols')
            labelY += app.textHeight + app.paddingY / 8

        # 调整输出标签的绘制位置以居中
        y_output = self.y + (self.height - self.outputHeight) / 2 + app.borderY/2
        for outputLabel in self.outputs:
            outputX = self.x + (app.borderX + self.inputWidth + app.paddingX + app.centerLabelWidth + app.paddingX) + self.outputWidth / 2
            drawLabel(outputLabel, outputX, y_output)
            y_output += app.textHeight + app.paddingY

        
class Node:
    def __init__(self, name, component, isOutput, data):
        self.name = name
        self.component = component
        self.isOutput = isOutput
        self.value = data
        self.isHovering = False
        self.x, self.y = 0, 0
        self.r = 5
        self.connection = None  # For input nodes
        self.connections = []   # For output nodes

    def updatePosition(self):
        if self.isOutput:
            index = self.component.outputNodes.index(self)
            self.x = self.component.x + self.component.width
            self.y = self.component.y + (self.component.height - self.component.outputHeight) / 2 + index * (app.textHeight + app.paddingY) + app.textHeight / 2
        else:
            index = self.component.inputNodes.index(self)
            self.x = self.component.x
            self.y = self.component.y + (self.component.height - self.component.inputHeight) / 2  + index * (app.textHeight + app.paddingY) + app.textHeight / 2
    
    def drawNode(self):
        drawCircle(self.x, self.y, self.r, fill='black' if self.isHovering else 'white', border='black')

    def hitTest(self, mouseX, mouseY):
        return (self.x - self.r <= mouseX <= self.x + self.r) and (self.y - self.r <= mouseY <= self.y + self.r)
    
    def addConnection(self, connection):
        if self.isOutput:
            self.connections.append(connection)
            # 如果输出节点有值，立即传递
            if self.value is not None:
                for conn in self.connections:
                    conn.end_node.receiveValue(self.value)
        else:
            if self.connection is not None:
                for conn in app.connections:
                    if conn.end_node == self:
                        app.connections.remove(conn)
                        break
            self.connection = connection
    
    def receiveValue(self, value):
        # 接收值并更新组件
        self.component.updateValue(self.name, value)

    def removeConnection(self, connection):
        if self.isOutput:
            if connection in self.connections:
                self.connections.remove(connection)
        else:
            if self.connection == connection:
                self.connection = None
