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
    
class Vector(TypicleComponent):
    def __init__(self, app):
        inputs = ['start', 'end']
        outputs = ['vector']
        name = 'vector\n<>'
        self.isGeo = False
        self.start_val = (app.x0, app.y0)
        self.end_val = (app.x0, app.y0)

        super().__init__(app, inputs, outputs, name)
        
        self.hasAllInputs = self.end_val is not None
    
    def updateValue(self, nodeName, value):
        # the value here should be a point cordinate tuple
        if nodeName == 'start':
            self.start_val = value
        elif nodeName == 'end':
            self.end_val = value

        for node in self.outputNodes:
            if node.name == 'vector':
                #用一个tuple储存向量的值
                xA,yA = self.start_val
                xB,yB = self.end_val
                dx,dy = xB-xA, yB-yA
                node.value = (dx, dy)
                for connection in node.connections:
                    connection.end_node.receiveValue(node.value)

    # def draw(self):
    #     xA,yA = self.start
    #     xB,yB = self.end
    #     dx,dy = xB-xA, yB-yA
    #     x0,y0 = self.anchor_val
    #     x1,y1 = x0+dx, y0+dy
    #     drawLine(x0,y0,x1,y1, fill='lightBlue', lineWidth = 1, dashes = True, arrowEnd = True)

    


