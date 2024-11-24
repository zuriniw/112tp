from Components import TypicleComponent, Component, Node
from cmu_graphics import *

class Slider(Component):
    def __init__(self, app, name='Slider\n--->', min_val=-200, max_val=200):
        inputs = []
        outputs = ['value']
        super().__init__(app)

        self.name = name
        self.outputs = outputs
        self.outputNodes = [Node(output, self, True, None) for output in outputs]
        
        self.min_val = min_val
        self.max_val = max_val
        
        # 初始值存储在输出节点中
        self.outputNodes[0].value = (min_val + max_val) / 2

        self.width = 120
        self.height = 32
        self.handleWidth = 12
        self.isDraggingHandle = False
        self.outputHeight = app.textHeight
        
        self.updateNodePositions()
    
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

    def getValue(self):
        return self.outputNodes[0].value

    def updateValue(self, value):
        self.outputNodes[0].value = value
        # 当值改变时，通知所有连接的节点
        for connection in self.outputNodes[0].connections:
            connection.end_node.receiveValue(value)

class Reverse(TypicleComponent):
    def __init__(self, app):
        inputs = ['n']
        outputs = ['opposite']
        name = 'Reverse\nNumber'
        self.isGeo = False
        super().__init__(app, inputs, outputs, name)
        self.n_val = None
        self.hasAllInputs = False
    
    def updateValue(self, nodeName, value):
        if nodeName == 'n':
            self.n_val = value
            self.hasAllInputs = (self.n_val is not None)
            
            # 如果有输入值，计算并更新输出节点的值
            if self.hasAllInputs:
                opposite_val = -self.n_val
                # 更新输出节点的值
                for node in self.outputNodes:
                    if node.name == 'opposite':
                        node.value = opposite_val
                        # 通过输出节点传递值
                        for connection in node.connections:
                            connection.end_node.receiveValue(opposite_val)

class Add(TypicleComponent):
    def __init__(self, app):
        inputs = ['n_1', 'n_2']
        outputs = ['sum']
        name = 'Add\nNumber\n+'
        self.isGeo = False
        super().__init__(app, inputs, outputs, name)

        # 没有input的时候默认为0
        self.n_1_val = 0
        self.n_2_val = 0
        self.hasAllInputs = True
    
    def updateValue(self, nodeName, value):
        if nodeName == 'n_1':
            self.n_1_val = value
        elif nodeName == 'n_2':
            self.n_2_val = value

        sum_val = self.n_1_val + self.n_2_val

        # 更新输出节点的值
        for node in self.outputNodes:
            if node.name == 'sum':
                node.value = sum_val
                # 通过输出节点传递值
                for connection in node.connections:
                    connection.end_node.receiveValue(sum_val)   
                      
class Subtract(TypicleComponent):
    def __init__(self, app):
        inputs = ['n_1', 'n_2']
        outputs = ['difference']
        name = 'Sub\nNumber\n-'
        self.isGeo = False
        super().__init__(app, inputs, outputs, name)
        
        self.n_1_val = 0
        self.n_2_val = 0
        self.hasAllInputs = True
    
    def updateValue(self, nodeName, value):
        if nodeName == 'n_1':
            self.n_1_val = value
        elif nodeName == 'n_2':
            self.n_2_val = value

        diff_val = self.n_1_val - self.n_2_val

        for node in self.outputNodes:
            if node.name == 'difference':
                node.value = diff_val
                for connection in node.connections:
                    connection.end_node.receiveValue(diff_val)

class Multiply(TypicleComponent):
    def __init__(self, app):
        inputs = ['n_1', 'n_2']
        outputs = ['product']
        name = 'Mul\nNumber\n×'
        self.isGeo = False
        super().__init__(app, inputs, outputs, name)
        
        self.n_1_val = 0
        self.n_2_val = 0
        self.hasAllInputs = True
    
    def updateValue(self, nodeName, value):
        if nodeName == 'n_1':
            self.n_1_val = value
        elif nodeName == 'n_2':
            self.n_2_val = value

        product_val = self.n_1_val * self.n_2_val

        for node in self.outputNodes:
            if node.name == 'product':
                node.value = product_val
                for connection in node.connections:
                    connection.end_node.receiveValue(product_val)

class Divide(TypicleComponent):
    def __init__(self, app):
        inputs = ['n_1', 'n_2']
        outputs = ['quotient']
        name = 'Div\nNumber\n÷'
        self.isGeo = False
        super().__init__(app, inputs, outputs, name)
        
        self.n_1_val = 0
        self.n_2_val = 1  # 默认除数为1避免除零
        self.hasAllInputs = True
    
    def updateValue(self, nodeName, value):
        if nodeName == 'n_1':
            self.n_1_val = value
        elif nodeName == 'n_2':
            # 避免除零
            self.n_2_val = value if value != 0 else 1

        quotient_val = self.n_1_val / self.n_2_val

        for node in self.outputNodes:
            if node.name == 'quotient':
                node.value = quotient_val
                for connection in node.connections:
                    connection.end_node.receiveValue(quotient_val)
