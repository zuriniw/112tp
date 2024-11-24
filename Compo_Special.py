'''
[special components] that have unique interaction and GUI, 
not belong to [typical components]
include:
    - Slider
    - 
'''

from Components import Component
from cmu_graphics import *
from Node import *

class Slider(Component):
    def __init__(self, app, name='Slider\n--->', min_val=-200, max_val=200):
        inputs = []
        outputs = ['value']
        super().__init__(app)
        
        self.name = name
        self.outputs = outputs
        self.outputNodes = [Node(output, self, True) for output in outputs]
        
        self.min_val = min_val
        self.max_val = max_val
        # 只在输出节点中存储值
        self.outputNodes[0].value = (min_val + max_val) / 2
        
        self.width = 120
        self.height = 32
        self.handleWidth = 12
        self.isDraggingHandle = False
        self.outputHeight = app.textHeight
        self.updateNodePositions()
    
    def getValue(self):
        # 直接从输出节点获取值
        return self.outputNodes[0].value
    
    def updateValue(self, value):
        # 更新输出节点的值并传递
        self.outputNodes[0].value = value
        # 通过输出节点传递值给所有连接的节点
        for connection in self.outputNodes[0].connections:
            connection.end_node.receiveValue(value)

    
    def hitTestHandle(self, mouseX, mouseY):
        # 计算手柄的中心位置，考虑手柄宽度
        handleX = self.x + ((self.getValue() - self.min_val) / (self.max_val - self.min_val)) * (self.width - self.handleWidth)
        # 检查鼠标是否在手柄的范围内
        return (handleX <= mouseX <= handleX + self.handleWidth) and (self.y <= mouseY <= self.y + self.height)

    def drawUI(self):
        # Draw node
        for node in self.outputNodes:
            node.drawNode()
        # Draw background
        drawRect(self.x, self.y, self.width, self.height, fill='white' if not self.isSelected else 'lightGrey', border='black')
        # Draw handle
        handleX = self.x + ((self.getValue() - self.min_val) / (self.max_val - self.min_val)) * (self.width-self.handleWidth)
        drawRect(handleX, self.y, self.handleWidth, self.height, fill='black')
        # Draw value label
        drawLabel(f'{self.getValue():.0f}', handleX, self.y - 10)

