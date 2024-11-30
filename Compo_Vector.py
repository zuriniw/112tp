from cmu_graphics import *
from Components import *

class Point(TypicleComponent):
    def __init__(self, app):
        inputs = ['x', 'y']
        outputs = ['point']
        name = 'Draw\nPoint\n•'
        self.isGeo = True
        self.isDisplay = True
        super().__init__(app, inputs, outputs, name)
        
        self.inputDefaultValue = {
            'x': 0,
            'y': 0
        }
        
        # Set initial values
        for node in self.inputNodes:
            node.value = self.inputDefaultValue[node.name]
            
        # 使用calculate方法计算初始输出值    
        self.outputNodes[0].value = self.calculate()
        self.hasAllInputs = True
        

    def calculate(self):
        x_val = self.inputNodes[0].value
        y_val = self.inputNodes[1].value
        
        # Case 1: Both x and y are single values (from sliders)
        if not isinstance(x_val, list) and not isinstance(y_val, list):
            world_x = x_val + self.app.x0
            world_y = self.app.y0 - y_val
            return [['point', (world_x, world_y)]]
        
        # Case 2: x from series [[20,40,60]], y from slider
        elif isinstance(x_val, list) and not isinstance(y_val, list):
            points = []
            values = x_val[0] if isinstance(x_val[0], list) else x_val
            for x in values[:2000]:
                world_x = x + self.app.x0
                world_y = self.app.y0 - y_val
                points.append(['point', (world_x, world_y)])
            return points
        
        # Case 3: x from slider, y from series [[20,40,60]]
        elif not isinstance(x_val, list) and isinstance(y_val, list):
            points = []
            values = y_val[0] if isinstance(y_val[0], list) else y_val
            for y in values[:2000]:
                world_x = x_val + self.app.x0
                world_y = self.app.y0 - y
                points.append(['point', (world_x, world_y)])
            return points
        
        # Case 4: Both x and y from series [[20,40,60]]
        else:
            points = []
            x_values = x_val[0] if isinstance(x_val[0], list) else x_val
            y_values = y_val[0] if isinstance(y_val[0], list) else y_val
            for x in x_values[:50]:
                for y in y_values[:40]:
                    world_x = x + self.app.x0
                    world_y = self.app.y0 - y
                    points.append(['point', (world_x, world_y)])
            return points
    

    def draw(self):
            points = self.calculate()
            for point in points:
                x, y = point[1]
                drawCircle(x, y, 4, fill='white',
                        border='blue',
                        visible=self.isDisplay)

    def getDefaultValue(self, nodeName):
        # 确保返回正确的默认值
        return self.inputDefaultValue.get(nodeName)

    def updateValue(self, name, value):
        # 处理series输入的嵌套数组格式
        if isinstance(value, list) and len(value) > 0 and isinstance(value[0], list):
            value = value[0]  # 取出内层数组
            
        # 更新节点值
        for node in self.inputNodes:
            if node.name == name:
                node.value = value
                break
                
        if self.hasAllInputs:
            output = self.calculate()
            if output:
                # 确保输出节点保持Node对象
                self.outputNodes[0].value = output
                # 通知所有连接的节点
                for connection in self.outputNodes[0].connections:
                    connection.end_node.receiveValue(output)
    


class Vector(TypicleComponent):
    def __init__(self, app):
        inputs = ['start', 'end']
        outputs = ['vector']
        name = 'vector\n< >'
        self.isGeo = False
        super().__init__(app, inputs, outputs, name)
        
        self.inputDefaultValue = {
            'start': (app.x0, app.y0),
            'end': (app.x0+200, app.y0-200)
        }
        
        for node in self.inputNodes:
            node.value = self.inputDefaultValue[node.name]
            
        self.hasAllInputs = True
    
    def calculate(self):
        start = self.inputNodes[0].value[1]
        end = self.inputNodes[1].value[1]
        
        # Add type checking and conversion
        if isinstance(start, tuple) and isinstance(end, tuple):
            try:
                dx = end[0] - start[0]
                dy = end[1] - start[1]
                return [(dx, dy)]
            except (ValueError, TypeError):
                return [(0, 0)]
        return [(0, 0)]


class VectorPreview(TypicleComponent):
    def __init__(self, app):
        inputs = ['vector', 'anchor']
        outputs = ['']  # Empty string for no output
        name = 'Vector\nPreview\n→'
        self.isGeo = True
        self.isDisplay = True
        super().__init__(app, inputs, outputs, name)
        
        self.inputDefaultValue = {
            'vector': (50, -50),
            'anchor': ['point',(app.x0, app.y0)]
        }
        
        for node in self.inputNodes:
            node.value = self.inputDefaultValue[node.name]
            
        self.hasAllInputs = True
    
    def calculate(self):
        return [None]
    
    def draw(self):
        vector_val = self.inputNodes[0].value
        anchor_val = self.inputNodes[1].value[1]
        if vector_val and anchor_val:
            dx, dy = vector_val
            x0, y0 = anchor_val
            x1, y1 = x0 + dx, y0 + dy
            drawLine(x0, y0, x1, y1, fill='pink', arrowEnd=True, visible=self.isDisplay)


