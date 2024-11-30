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

        # 确保x和y都是列表
        x_val = [x_val] if not isinstance(x_val, list) else x_val
        y_val = [y_val] if not isinstance(y_val, list) else y_val

        # 展开x和y的列表，生成笛卡尔积
        points = []
        for x in x_val:
            for y in y_val:
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

    


class Vector(TypicleComponent):
    def __init__(self, app):
        inputs = ['start', 'end']
        outputs = ['vector']
        name = 'vector\n< >'
        
        self.isGeo = False
        self.isDisplay = False  # 添加显示标志
        
        super().__init__(app, inputs, outputs, name)
        
        self.inputDefaultValue = {
            'start': [['point', (app.x0, app.y0)]],
            'end': [['point', (app.x0+200, app.y0-200)]]
        }
        
        for node in self.inputNodes:
            node.value = self.inputDefaultValue[node.name]
        
        # 计算并设置初始输出值
        self.outputNodes[0].value = self.calculate()
        
        self.hasAllInputs = True

    def calculate(self):
        start_val = self.inputNodes[0].value
        end_val = self.inputNodes[1].value
        
        vectors = []
        
        # 处理起点和终点的不同输入情况
        if (isinstance(start_val[0], list) and start_val[0][0] == 'point' and 
            isinstance(end_val[0], list) and end_val[0][0] == 'point'):
            
            # 支持多点组合
            for start in start_val:
                for end in end_val:
                    dx = end[1][0] - start[1][0]
                    dy = end[1][1] - start[1][1]
                    vectors.append((dx, dy))
        
        elif start_val[0] == 'point' and end_val[0] == 'point':
            # 单点情况
            dx = end_val[1][0] - start_val[1][0]
            dy = end_val[1][1] - start_val[1][1]
            vectors.append((dx, dy))
        
        return vectors if vectors else [(0, 0)]


class VectorPreview(TypicleComponent):
    def __init__(self, app):
        inputs = ['vector', 'anchor']
        outputs = ['']  # Empty string for no output
        name = 'Vector\nPreview\n→'
        self.isGeo = True
        self.isDisplay = True
        super().__init__(app, inputs, outputs, name)
        
        self.inputDefaultValue = {
            'vector': [(50, -50)],
            'anchor': [['point',(app.x0, app.y0)]]
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
            for vector in vector_val:
                for anchor in anchor_val:
                    dx, dy = vector
                    x0, y0 = anchor[1]
                    x1, y1 = x0 + dx, y0 + dy
                    drawLine(x0, y0, x1, y1, fill='pink', arrowEnd=True, visible=self.isDisplay)


