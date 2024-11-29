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
            
        self.outputNodes[0].value = ['point', (app.x0, app.y0)]
        self.hasAllInputs = True
        
    def calculate(self):
        x_val = self.inputNodes[0].value
        y_val = self.inputNodes[1].value
        
        # Case 1: Both x and y are single values
        if not isinstance(x_val, list) and not isinstance(y_val, list):
            world_x = x_val + self.app.x0
            world_y = self.app.y0 - y_val
            return [['point', (world_x, world_y)]]
            
        # Case 2: x is list, y is single value
        elif isinstance(x_val, list) and not isinstance(y_val, list):
            points = [['point', (self.app.x0 + x, self.app.y0 - y_val)] for x in x_val[:2000]]
            return points
            
        # Case 3: x is single value, y is list
        elif not isinstance(x_val, list) and isinstance(y_val, list):
            points = [['point', (self.app.x0 + x_val, self.app.y0 - y)] for y in y_val[:2000]]
            return points
            
        # Case 4: Both x and y are lists
        else:
            points = []
            # Limit total points to 2000
            for x in x_val[:50]:  # Limit x points
                for y in y_val[:40]:  # Limit y points
                    points.append(['point', (self.app.x0 + x, self.app.y0 - y)])
            return points

    def draw(self):
        if self.hasAllInputs:
            points = self.calculate()  # 不需要[0]，因为calculate直接返回点列表
            if isinstance(points, list):
                for point in points:
                    if point[0] == 'point':
                        x, y = point[1]
                        drawCircle(x, y, 4, fill='white', 
                                border='blue',
                                visible=self.isDisplay)

    def getDefaultValue(self, nodeName):
        # 确保返回正确的默认值
        return self.inputDefaultValue.get(nodeName)


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


