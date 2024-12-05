'''
- Component
    - TypicleComponent
        - CircleCreator
        - RectCreator
'''
from cmu_graphics import *
from Components import TypicleComponent

## HELPER: take in world cdnt and give back drawing cdnt for drawing
def getDrawingPoint(x0,y0,worldPoint):
    wx, wy = worldPoint
    dx = wx + x0
    dy = y0 - wy
    drawingPoint = (dx, dy)
    return drawingPoint

## HELPER: takes in 2 symmentric lists and align the len of them
def alignLists(L, M, default_value=None):
    L = [L] if not isinstance(L, list) else L
    M = [M] if not isinstance(M, list) else M
    # L shorter, extend it
    if len(L) < len(M):
        last_item = L[-1] if L else default_value
        L.extend([last_item] * (len(M) - len(L)))
    # M shorter, extend it
    elif len(M) < len(L):
        last_item = M[-1] if M else default_value
        M.extend([last_item] * (len(L) - len(M)))
    return L, M

########################################################################################
# CIRCLE CREATOR
# output representation: ['cir', (x, y), r]
########################################################################################

class CircleCreator(TypicleComponent):
    def __init__(self, app):
        inputs = ['point', 'radius','isGradFill']
        outputs = ['circle']
        name = 'Draw\nCirc\nO'
        self.isGeo = True
        self.isDisplay = True
        super().__init__(app, inputs, outputs, name)
        
        self.inputDefaultValue = {
            'point': [['point', (0, 0)]],
            'radius': 40,
            'isGradFill':False
        }
        
        for node in self.inputNodes:
            node.value = self.inputDefaultValue[node.name]
            
        self.outputNodes[0].value = self.calculate()
        self.hasAllInputs = True

        self.isGradFill = False
        self.x0, self.y0 = app.x0, app.y0
        
    def calculate(self):
        point_val = self.inputNodes[0].value
        radius_val = self.inputNodes[1].value
        isGradFill = True if self.inputNodes[2].value == 1 else False

        point_val, radius_val = alignLists(point_val, radius_val, default_value=['point', (self.app.x0, self.app.y0)])
        
        circles = []
        for point, radius in zip(point_val, radius_val):
            if point[0] == 'point' and int(radius) != 0:
                circles.append(['cir', point[1], abs(radius)])
        
        self.isGradFill = isGradFill
        return circles
        
    def draw(self):
        if self.hasAllInputs:
            circles = self.calculate()
            if not circles:
                return
            for circle in circles:
                    x, y = getDrawingPoint(self.x0, self.y0, circle[1])
                    radius = circle[2]
                    drawCircle(x, y, radius, border=None if self.isGradFill else 'blue',
                                fill=gradient('blue', 'white') if self.isGradFill else None,
                                visible=self.isDisplay)
                              
########################################################################################
# RECT CREATOR
# output representation: ['rect', (x, y), w, h]
########################################################################################
                  
class RectCreator(TypicleComponent):
    def __init__(self, app):
        inputs = ['point', 'width', 'height']
        outputs = ['rect']
        name = 'Draw\nRect\n□'
        
        self.isGeo = True
        self.isDisplay = True
        
        super().__init__(app, inputs, outputs, name)
        
        self.inputDefaultValue = {
            'point': [['point', (0, 0)]],
            'width': 40,
            'height': 40
        }
        
        for node in self.inputNodes:
            node.value = self.inputDefaultValue[node.name]
        
        self.outputNodes[0].value = self.calculate()
        
        self.hasAllInputs = True
        self.x0, self.y0 = app.x0, app.y0

    def calculate(self):
        point_val = self.inputNodes[0].value
        width_val = abs(self.inputNodes[1].value) if self.inputNodes[1].value is not None else None
        height_val = abs(self.inputNodes[2].value) if self.inputNodes[2].value is not None else None
        
        rects = []
        if isinstance(point_val[0], list) and point_val[0][0] == 'point':
            for point in point_val:
                rects.append(['rect', point[1], width_val, height_val])
        return rects

    def draw(self):
        if self.hasAllInputs:
            rects = self.calculate()
            if not rects:
                return
            for rect in rects:
                x, y = getDrawingPoint(self.x0, self.y0,rect[1])
                width = rect[2]
                height = rect[3]
                
                if int(width) != 0 and int(height) != 0:
                    drawRect(x, y, width, height, fill=None, border='blue', visible=self.isDisplay)