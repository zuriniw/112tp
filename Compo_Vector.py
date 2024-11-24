from cmu_graphics import *
from Components import *

class Point(TypicleComponent):
    def __init__(self, app):
        inputs = ['x', 'y']
        outputs = ['point']
        name = 'point\n๏'
        self.isGeo = True
        self.x_val = app.x0
        self.y_val = app.y0
        super().__init__(app, inputs, outputs, name)
        
        self.hasAllInputs = True
    
    def updateValue(self, nodeName, value):
        if nodeName == 'x':
            self.x_val = value + app.x0
        elif nodeName == 'y':
            self.y_val = app.y0 - value
        
        for node in self.outputNodes:
            if node.name == 'point':
                node.value = (self.x_val, self.y_val)
                for connection in node.connections:
                    connection.end_node.receiveValue(node.value)

    def draw(self):
        drawCircle(self.x_val, self.y_val, 4, fill='white', border='blue', borderWidth = 2)