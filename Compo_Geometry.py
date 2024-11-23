from cmu_graphics import *
from Components import TypicleComponent

class CircleCreator(TypicleComponent):
    def __init__(self, app):
        inputs = ['x', 'y', 'radius']
        outputs = ['theCircle']
        name = 'Draw\nCirc\nO'
        self.isGeo = True
        super().__init__(app, inputs, outputs, name)
        self.x_val = None
        self.y_val = None
        self.radius_val = None
        self.hasAllInputs = (self.x_val is not None and 
                       self.y_val is not None and 
                       self.radius_val is not None)
    
    def updateValue(self, nodeName, value):
        if nodeName == 'x':
            self.x_val = value + app.x0
        elif nodeName == 'y':
            self.y_val = app.y0 - value
        elif nodeName == 'radius':
            self.radius_val = abs(value)
        self.hasAllInputs = (self.x_val is not None and 
                            self.y_val is not None and 
                            self.radius_val is not None)
    
    def draw(self):
        if self.hasAllInputs and self.radius_val!=0:
            drawCircle(self.x_val, self.y_val, self.radius_val, 
                      fill=None, border='blue')
                      
class RectCreator(TypicleComponent):
    def __init__(self, app):
        inputs = ['x', 'y', 'width', 'height']
        outputs = ['theRect']
        name = 'Draw\nRect\n⬚'
        self.isGeo = True
        super().__init__(app, inputs, outputs, name)
        self.x_val = None
        self.y_val = None
        self.width_val = None
        self.height_val = None
        self.hasAllInputs = (self.x_val is not None and 
                            self.y_val is not None and 
                            self.width_val is not None and 
                            self.height_val is not None)
    
    def updateValue(self, nodeName, value):
        if nodeName == 'x':
            self.x_val = value + app.x0
        elif nodeName == 'y':
            self.y_val = app.y0 - value
        elif nodeName == 'width':
            self.width_val = max(0, value) if value is not None else None
        elif nodeName == 'height':
            self.height_val = max(0, value) if value is not None else None

        self.hasAllInputs = (self.x_val is not None and 
                            self.y_val is not None and 
                            self.width_val is not None and
                            self.height_val is not None)

    def draw(self):
        if self.hasAllInputs and self.width_val*self.height_val != 0 :
            drawRect(self.x_val, self.y_val, self.width_val, self.height_val, 
                    fill=None, border='blue')

