from cmu_graphics import *
from Components import *

class Point(TypicleComponent):
    def __init__(self, app):
        inputs = ['x', 'y']
        outputs = ['point']
        name = 'point\n๏'
        self.isGeo = True
        super().__init__(app, inputs, outputs, name)
        
        self.inputDefaultValue = {
            'x': 0,
            'y': 0
        }
        
        # Initialize nodes with default values
        for node in self.inputNodes:
            node.value = self.inputDefaultValue[node.name]
            
        # Initialize output with world coordinates
        self.outputNodes[0].value = ['point', (app.x0, app.y0)]
        
    def calculate(self):
        x_val = self.inputNodes[0].value
        y_val = self.inputNodes[1].value
        world_pos = (x_val + app.x0, app.y0 - y_val)
        return [['point', world_pos]]


    
    def getDefaultValue(self, nodeName):
        # 确保返回正确的默认值
        return self.inputDefaultValue.get(nodeName)


    def draw(self):
        point_val = self.outputNodes[0].value
        if point_val and isinstance(point_val, list):
            _, pos = point_val  # 解包几何数据格式 ['point', (x,y)]
            x, y = pos           # 解包坐标元组
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

        self.inputDefaultValue = {
        'start': (app.x0, app.y0),
        'end': (app.x0+200, app.y0-200)
        }
    
    def calculate(self):
        start = self.inputNodes[0].value
        end = self.inputNodes[1].value
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        return [(dx, dy)]  # 返回输出值列表



    
class VectorPreview(TypicleComponent):
    def __init__(self, app):
        inputs = ['vector', 'anchor']
        outputs = ['']  # Empty string for no output
        name = 'Vector\nPreview\n→'
        self.isGeo = True
        super().__init__(app, inputs, outputs, name)
        
        self.inputDefaultValue = {
            'vector': (50, -50),
            'anchor': (app.x0, app.y0)
        }
        
        for node in self.inputNodes:
            node.value = self.inputDefaultValue[node.name]
            
        self.hasAllInputs = True
    
    def calculate(self):
        return [None]
    
    def draw(self):
        vector_val = self.inputNodes[0].value
        anchor_val = self.inputNodes[1].value
        if vector_val and anchor_val:
            dx, dy = vector_val
            x0, y0 = anchor_val
            x1, y1 = x0 + dx, y0 + dy
            drawLine(x0, y0, x1, y1, fill='pink', arrowEnd=True)


