from cmu_graphics import *
from Components import TypicleComponent

class CircleCreator(TypicleComponent):
    def __init__(self, app):
        inputs = ['point', 'radius']
        outputs = ['circle']
        name = 'Draw\nCirc\nO'
        self.isGeo = True
        self.isDisplay = True
        super().__init__(app, inputs, outputs, name)
        
        self.inputDefaultValue = {
            'point': [['point', (app.x0, app.y0)]],
            'radius': 40
        }
        
        for node in self.inputNodes:
            node.value = self.inputDefaultValue[node.name]
            
        self.outputNodes[0].value = [['cir', (app.x0, app.y0), 40]]
        self.hasAllInputs = True
        
    def calculate(self):
        point_val = self.inputNodes[0].value
        radius_val = abs(self.inputNodes[1].value) if self.inputNodes[1].value is not None else None
        
        circles = []
        if isinstance(point_val[0],list) and point_val[0][0] == 'point':
            for point in point_val:
                circles.append(['cir', point[1], radius_val])
        else:
            if point_val[0] == 'point':
                circles.append(['cir', point_val[1], radius_val])
        return circles
        
    def draw(self):
        if self.hasAllInputs:
            circles = self.calculate()
            if not circles:
                return
            for circle in circles:
                    x, y = circle[1]
                    radius = circle[2]
                    if int(radius) != 0:
                        drawCircle(x, y, radius,
                                 fill=None,
                                 border='blue',
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
            'point': [['point', (app.x0, app.y0)]],
            'width': 40,
            'height': 40
        }
        
        for node in self.inputNodes:
            node.value = self.inputDefaultValue[node.name]
        
        self.outputNodes[0].value = [['rect', (app.x0, app.y0), 40, 40]]
        
        self.hasAllInputs = True

    def calculate(self):
        point_val = self.inputNodes[0].value
        width_val = abs(self.inputNodes[1].value) if self.inputNodes[1].value is not None else None
        height_val = abs(self.inputNodes[2].value) if self.inputNodes[2].value is not None else None
        
        rects = []
        
        if isinstance(point_val[0], list) and point_val[0][0] == 'point':
            for point in point_val:
                rects.append(['rect', point[1], width_val, height_val])
        else:
            if point_val[0] == 'point':
                rects.append(['rect', point_val[1], width_val, height_val])
        
        return rects

    def draw(self):
        if self.hasAllInputs:
            rects = self.calculate()
            
            if not rects:
                return
            
            for rect in rects:
                x, y = rect[1]
                width = rect[2]
                height = rect[3]
                
                if int(width) != 0 and int(height) != 0:
                    drawRect(x, y, width, height,
                             fill=None, 
                             border='blue', 
                             visible=self.isDisplay)