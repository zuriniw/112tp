from cmu_graphics import *
from Components import *

class Point(TypicleComponent):
    def __init__(self, app):
        inputs = ['x', 'y']
        outputs = ['point']
        name = 'point\n๏'
        self.isGeo = True
        super().__init__(app, inputs, outputs, name)
        
        # 设置默认值字典，使用相对坐标
        self.inputDefaultValue = {
            'x': app.x0,
            'y': app.y0
        }
        
        # 为输入节点设置默认值
        for node in self.inputNodes:
            node.value = self.inputDefaultValue[node.name]
        
        # 初始化输出节点值，使用绝对坐标
        self.outputNodes[0].value = (app.x0, app.y0)
        self.hasAllInputs = True
    
    def getDefaultValue(self, nodeName):
        # 确保返回正确的默认值
        return self.inputDefaultValue.get(nodeName)
    
    def updateValue(self, nodeName, value):
        # 从输入节点直接获取值
        x_val = self.inputNodes[0].value
        y_val = self.inputNodes[1].value
        
        # 更新输出节点的值
        for node in self.outputNodes:
            if node.name == 'point':
                node.value = (x_val + app.x0, app.y0 - y_val)
                # 传递值给连接的节点
                for connection in node.connections:
                    connection.end_node.receiveValue(node.value)


    def draw(self):
    # Get values directly from output node
        point_val = self.outputNodes[0].value
        if point_val:
            x, y = point_val
            drawCircle(x, y, 4, fill='white', border='blue', borderWidth=2)



class Vector(TypicleComponent):
    def __init__(self, app):
        inputs = ['start', 'end']
        outputs = ['vector']
        name = 'vector\n< >'
        self.isGeo = False
        super().__init__(app, inputs, outputs, name)
        
        # 设置输入节点的默认值
        for node in self.inputNodes:
            if node.name == 'start':
                node.value = (app.x0, app.y0)
            elif node.name == 'end':
                node.value = (app.x0+200, app.y0-200)
        
        self.hasAllInputs = True
    
    def updateValue(self, nodeName, value):
        # 直接从节点获取值
        start_val = self.inputNodes[0].value
        end_val = self.inputNodes[1].value
        
        if start_val and end_val:
            xA, yA = start_val
            xB, yB = end_val
            dx, dy = xB-xA, yA-yB
            
            # 更新输出节点值
            for node in self.outputNodes:
                if node.name == 'vector':
                    node.value = (dx, dy)
                    for connection in node.connections:
                        connection.end_node.receiveValue(node.value)



    
class VectorPreview(TypicleComponent):
    def __init__(self, app):
        inputs = ['vector', 'anchor']
        outputs = ['']  # 改为空字符串而不是空列表，避免max()错误
        name = 'Vector\nPreview\n→'
        self.isGeo = True
        super().__init__(app, inputs, outputs, name)
        
        # 设置默认值
        self.inputDefaultValue = {
            'vector': (0, 0),
            'anchor': (app.x0, app.y0)
        }
        
        # 初始化输入节点的默认值
        for node in self.inputNodes:
            node.value = self.inputDefaultValue[node.name]
        
        self.hasAllInputs = True
    
    def updateValue(self, nodeName, value):
        # 直接从节点获取值，不需要额外存储
        if nodeName == 'vector':
            self.inputNodes[0].value = value
        elif nodeName == 'anchor':
            self.inputNodes[1].value = value
            
        self.hasAllInputs = (self.inputNodes[0].value is not None and 
                            self.inputNodes[1].value is not None)
    
    def draw(self):
        if self.hasAllInputs:
            vector_val = self.inputNodes[0].value
            anchor_val = self.inputNodes[1].value
            
            if vector_val and anchor_val:
                dx, dy = vector_val
                x0, y0 = anchor_val
                x1, y1 = x0 + dx, y0 + dy
                drawLine(x0, y0, x1, y1, fill='pink', arrowEnd=True)




