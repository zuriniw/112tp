from cmu_graphics import *
from Components import TypicleComponent

class CircleCreator(TypicleComponent):
    def __init__(self, app):
        inputs = ['point', 'radius']
        outputs = ['circle']
        name = 'Draw\nCirc\nO'
        self.isGeo = True
        super().__init__(app, inputs, outputs, name)
        self.point_val = None
        self.radius_val = None
        self.hasAllInputs = (self.point_val is not None and self.radius_val is not None)
    
    def updateValue(self, nodeName, value):
        if nodeName == 'point':
            self.point_val = value
        elif nodeName == 'radius':
            self.radius_val = abs(value) if self.radius_val != 0 else None
        self.hasAllInputs = (self.point_val is not None and
                            self.radius_val is not None)
    
    def draw(self):
        if self.hasAllInputs and self.radius_val!=0:
            x, y = self.point_val
            drawCircle(x, y, self.radius_val, 
                      fill=None, border='blue')
                      
class RectCreator(TypicleComponent):
    def __init__(self, app):
        inputs = ['point', 'width', 'height']
        outputs = ['rect']
        name = 'Draw\nRect\n⬚'
        self.isGeo = True
        super().__init__(app, inputs, outputs, name)
        self.point_val = None
        self.width_val = None
        self.height_val = None
        self.hasAllInputs = (self.point_val is not None and 
                            self.width_val is not None and 
                            self.height_val is not None)
    
    def updateValue(self, nodeName, value):
        if nodeName == 'point':
            self.point_val = value
        elif nodeName == 'width':
            self.width_val = max(0, value) if value is not None else None
        elif nodeName == 'height':
            self.height_val = max(0, value) if value is not None else None

        self.hasAllInputs = (self.point_val is not None and 
                            self.width_val is not None and
                            self.height_val is not None)

    def draw(self):
        if self.hasAllInputs and self.width_val*self.height_val != 0:
            x, y = self.point_val
            drawRect(x - self.width_val/2, y - self.height_val/2, 
                    self.width_val, self.height_val, 
                    fill=None, border='blue')
