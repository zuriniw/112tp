'''
- Component
    - TypicleComponent
        - Point
        - Vector
        - VectorPreview
'''
from cmu_graphics import *
from Components import *

## HELPER: take in world cdnt and give back drawing cdnt for drawing
def getDrawingPoint(x0,y0,worldPoint):
    wx, wy = worldPoint
    dx = wx + x0
    dy = y0 - wy
    drawingPoint = (dx, dy)
    return drawingPoint

########################################################################################
# POINT
# output representation: ['point', (x, y)]
########################################################################################
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
        
        for node in self.inputNodes:
            node.value = self.inputDefaultValue[node.name]
              
        self.outputNodes[0].value = self.calculate()
        self.hasAllInputs = True

    def calculate(self):
        x_val = self.inputNodes[0].value
        y_val = self.inputNodes[1].value

        x_val = [x_val] if not isinstance(x_val, list) else x_val
        y_val = [y_val] if not isinstance(y_val, list) else y_val

        points = []
        for x in x_val:
            for y in y_val:
                points.append(['point', (x, y)])

        return points
    
    def draw(self):
            points = self.calculate()
            for point in points:
                x, y = point[1]
                worldX = x + self.app.x0
                worldY = self.app.y0 - y
                drawCircle(worldX, worldY, 4, fill='white', border='blue', visible=self.isDisplay)

    def getDefaultValue(self, nodeName):
        return self.inputDefaultValue.get(nodeName)

########################################################################################
# VECTOR
# output representation: ['vector', (x, y)]
# note: vector is invisible
########################################################################################

class Vector(TypicleComponent):
    def __init__(self, app):
        inputs = ['start', 'end']
        outputs = ['vector']
        name = 'Create\nVector\n< >'
        
        self.isGeo = False
        self.isDisplay = False
        
        super().__init__(app, inputs, outputs, name)
        
        self.inputDefaultValue = {
            'start': [['point', (0, 0)]],
            'end': [['point', (200, 200)]]
        }
        
        for node in self.inputNodes:
            node.value = self.inputDefaultValue[node.name]
        
        self.outputNodes[0].value = self.calculate()
        
        self.hasAllInputs = True

    def calculate(self):
        start_val = self.inputNodes[0].value
        end_val = self.inputNodes[1].value
        
        vectors = []
        
        if (isinstance(start_val[0], list) and start_val[0][0] == 'point' and 
            isinstance(end_val[0], list) and end_val[0][0] == 'point'):
            
            for start in start_val:
                for end in end_val:
                    dx = end[1][0] - start[1][0]
                    dy = end[1][1] - start[1][1]
                    vectors.append(['vector',(dx, dy)])
        
        return vectors if vectors else [[vectors,(0, 0)]]

########################################################################################
# VECTOR PREVIEW
#       1.reveal the vector by providing an anchor point
########################################################################################

class VectorPreview(TypicleComponent):
    def __init__(self, app):
        inputs = ['vector', 'anchor']
        outputs = ['']  # Empty string for no output
        name = 'Vector\nPreview\n~'
        self.isGeo = True
        self.isDisplay = True
        super().__init__(app, inputs, outputs, name)
        self.x0, self.y0 = app.x0, app.y0
        
        self.inputDefaultValue = {
            'vector': [['vector', (50, -50)]],
            'anchor': [['point',(0, 0)]]
        }
        
        for node in self.inputNodes:
            node.value = self.inputDefaultValue[node.name]
            
        self.hasAllInputs = True
    
    def calculate(self):
        return None
    
    def draw(self):
        vector_val = self.inputNodes[0].value
        anchor_val = self.inputNodes[1].value
        if vector_val and anchor_val:
            for vector in vector_val:
                for anchor in anchor_val:
                    dx, dy = vector[1]
                    x0, y0 = getDrawingPoint(self.x0, self.y0,anchor[1])
                    x1, y1 = x0 + dx, y0 + dy
                    drawLine(x0, y0, x1, y1, fill=rgb(218, 231, 231), arrowEnd=True, visible=self.isDisplay)


