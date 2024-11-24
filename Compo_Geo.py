from cmu_graphics import *
from Components import TypicleComponent

class CircleCreator(TypicleComponent):
    def __init__(self, app):
        inputs = ['point', 'radius']
        outputs = ['circle']
        name = 'Draw\nCirc\nO'
        self.isGeo = True
        super().__init__(app, inputs, outputs, name)
        
        # 设置默认值
        self.inputDefaultValue = {
            'point': (app.x0, app.y0),
            'radius': 40
        }
        
        # 为输入节点设置默认值
        for node in self.inputNodes:
            node.value = self.inputDefaultValue[node.name]
            
        # 初始化输出节点值
        self.outputNodes[0].value = ['cir', (app.x0, app.y0), 40]
        self.hasAllInputs = True
    
    def updateValue(self, nodeName, value):
        # 更新输入节点的值
        for node in self.inputNodes:
            if node.name == nodeName:
                node.value = value
                
        self.hasAllInputs = (self.inputNodes[0].value is not None and
                            self.inputNodes[1].value is not None)
        
        # 如果所有输入都有值，更新输出
        if self.hasAllInputs:
            point_val = self.inputNodes[0].value
            radius_val = abs(self.inputNodes[1].value) if self.inputNodes[1].value is not None else None
            
            for node in self.outputNodes:
                if node.name == 'circle':
                    node.value = ['cir', point_val, radius_val]
                    for connection in node.connections:
                        connection.end_node.receiveValue(node.value)
    
    def draw(self):
        if self.hasAllInputs and self.inputNodes[1].value != 0:
            x, y = self.inputNodes[0].value
            radius = abs(self.inputNodes[1].value)
            drawCircle(x, y, radius, fill=None, border='blue')

class RectCreator(TypicleComponent):
    def __init__(self, app):
        inputs = ['point', 'width', 'height']
        outputs = ['rect']
        name = 'Draw\nRect\n⬚'
        self.isGeo = True
        super().__init__(app, inputs, outputs, name)
        
        # 设置默认值
        self.inputDefaultValue = {
            'point': (app.x0, app.y0),
            'width': 40,
            'height': 40
        }
        
        # 为输入节点设置默认值
        for node in self.inputNodes:
            node.value = self.inputDefaultValue[node.name]
            
        # 初始化输出节点值，与 CircleCreator 保持一致
        self.outputNodes[0].value = ['rect', (app.x0, app.y0), 40, 40]
        self.hasAllInputs = True
    
    def updateValue(self, nodeName, value):
        # 更新输入节点的值
        for node in self.inputNodes:
            if node.name == nodeName:
                node.value = value
                
        self.hasAllInputs = all(node.value is not None for node in self.inputNodes)
        
        # 如果所有输入都有值，更新输出
        if self.hasAllInputs:
            point_val = self.inputNodes[0].value
            width_val = abs(self.inputNodes[1].value)
            height_val = abs(self.inputNodes[2].value)
            
            for node in self.outputNodes:
                if node.name == 'rect':
                    # 修改：使用与 CircleCreator 相同的列表格式
                    node.value = ['rect', point_val, width_val, height_val]
                    for connection in node.connections:
                        connection.end_node.receiveValue(node.value)

    
    def draw(self):
        if self.hasAllInputs and self.inputNodes[1].value != 0 and self.inputNodes[2].value != 0:
            x, y = self.inputNodes[0].value
            width = abs(self.inputNodes[1].value)
            height = abs(self.inputNodes[2].value)
            drawRect(x - width/2, y - height/2, width, height,
                    fill=None, border='blue')
