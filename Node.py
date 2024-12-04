from cmu_graphics import *

########################################################################################  
# NODE 
#       1 //  visualization & mouse-hit detect
#       2 //  manage data flow
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
        print(f'{self.component} update value of {self.name} to {value}')

    def addConnection(self, connection):
        # 如果是输入节点
        if not self.isOutput:
            # 删除现有的所有连接
            for existing_conn in self.connections[:]:
                existing_conn.deleteConnection(self.component.app)
            
            # 清空连接列表
            self.connections = []
            
            # 重置值为None，等待新的值传入
            self.value = None
            
            # 添加新连接
            self.connections.append(connection)
            
            # 从新的输出节点获取值
            self.value = connection.start_node.value
            
            # 触发组件的值更新
            self.component.updateValue(self.name, self.value)
        
        # 如果是输出节点，保持原有逻辑
        else:
            self.connections.append(connection)
            if self.value is not None:
                connection.end_node.receiveValue(self.value)


    def removeConnection(self, connection):
        if connection in self.connections:
            self.connections.remove(connection)
            # 如果是输入节点，恢复默认值
            if not self.isOutput:
                default = self.component.getDefaultValue(self.name)
                self.value = default
                self.component.updateValue(self.name, default)

