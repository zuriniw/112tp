'''
- Node
'''
from cmu_graphics import *

########################################################################################  
# NODE 
#       1 //  visualization & mouse-hit detect
#       2 //  manage data flow
#       3 //  broadcast
########################################################################################

class Node:
    def __init__(self, name, component, isOutput):
        self.name = name
        self.component = component
        self.isOutput = isOutput        
        self.value = None
        self.isHovering = False
        self.x, self.y = 0, 0
        self.r = 5
        self.connections = []

    ###### 1 // Visualization & Mouse-hit Detect ######
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
    
    
    ###### 2 // Manage Data Flow ######
    # endnode(inputnode) hear from outputnode
    def receiveValue(self, value):
        self.value = value
        self.component.updateValue(self.name, value)

    def addConnection(self, connection):
        # for inputNode
        if not self.isOutput:
            # clear old
            for existing_conn in self.connections[:]:
                existing_conn.deleteConnection(self.component.app)
            self.connections = []
            # add new
            self.connections.append(connection)
            if connection.isValid:
                self.value = connection.start_node.value
                self.component.updateValue(self.name, self.value)
        
        # for outputNode
        else:
            self.connections.append(connection)
            if connection.isValid and self.value is not None:
                connection.end_node.receiveValue(self.value)

    def removeConnection(self, connection):
        if connection in self.connections:
            self.connections.remove(connection)
            # 如果是输入节点，恢复默认值
            if not self.isOutput:
                default = self.component.getDefaultValue(self.name)
                self.value = default
                self.component.updateValue(self.name, default)

