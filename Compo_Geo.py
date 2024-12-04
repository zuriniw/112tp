from cmu_graphics import *
from Components import TypicleComponent

## take in world cdnt and give back drawing cdnt for drawing
def getDrawingPoint(x0,y0,worldPoint):
    wx, wy = worldPoint
    dx = wx + x0
    dy = y0 - wy
    drawingPoint = (dx, dy)
    return drawingPoint

def align_lists(list1, list2, default_value=None):
    # ensure the input is a lsit
    list1 = [list1] if not isinstance(list1, list) else list1
    list2 = [list2] if not isinstance(list2, list) else list2
    
    # list1 shorter, extend it
    if len(list1) < len(list2):
        last_item = list1[-1] if list1 else default_value
        list1.extend([last_item] * (len(list2) - len(list1)))
    
    # list 2 shorter, extend it
    elif len(list2) < len(list1):
        last_item = list2[-1] if list2 else default_value
        list2.extend([last_item] * (len(list1) - len(list2)))
    
    return list1, list2


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

        point_val, radius_val = align_lists(point_val, radius_val, 
                                            default_value=['point', (self.app.x0, self.app.y0)])
        
        
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
                    drawCircle(x, y, radius,
                                border=None if self.isGradFill else 'blue',
                                fill=gradient('blue', 'white') if self.isGradFill else None,
                                visible=self.isDisplay)
                              
                        
class RectCreator(TypicleComponent):
    def __init__(self, app):
        inputs = ['point', 'width', 'height']
        outputs = ['rect']
        name = 'Draw\nRect\nO'
        
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
                    drawRect(x, y, width, height,
                             fill=None, 
                             border='blue', 
                             visible=self.isDisplay)