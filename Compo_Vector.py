from cmu_graphics import *
from Components import *

class Point(TypicleComponent):
    def __init__(self, app):
        inputs = ['x', 'y']
        outputs = ['point']
        name = 'point\n๏'
        self.isGeo = True
        super().__init__(app, inputs, outputs, name)
        self.x_val = None
        self.y_val = None
        self.cord = None
        self.hasAllInputs = (self.x_val is not None and 
                       self.y_val is not None)
    
    def updateValue(self, nodeName, value):
        if nodeName == 'x':
            self.x_val = value + app.x0
        elif nodeName == 'y':
            self.y_val = app.y0 - value

        self.hasAllInputs = (self.x_val is not None and 
                            self.y_val is not None)
        if self.hasAllInputs:
            self.cord = (self.x_val, self.y_val)

    def draw(self):
        if self.hasAllInputs:
            drawCircle(self.x_val, self.y_val, 4, fill='white', border='blue', borderWidth = 2)