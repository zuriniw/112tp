from cmu_graphics import *
from Components import *

class Move(TypicleComponent):
    def __init__(self, app):
        inputs = ['geo', 'vector']
        outputs = ['moved']
        name = 'Move\nGeo\n↗'
        self.isGeo = True
        self.geo_val = None
        self.vector_val = None
        self.hasAllInputs = False
        super().__init__(app, inputs, outputs, name)

    
    def updateValue(self, nodeName, value):
        if nodeName == 'geo':
            self.geo_val = value
        elif nodeName == 'vector':
            self.vector_val = value
            
        self.hasAllInputs = (self.geo_val is not None and 
                            self.vector_val is not None)
        
        # If we have both inputs, calculate and output the moved geometry
        if self.hasAllInputs:
            # Get the vector displacement
            dx, dy = self.vector_val
            
            # Create new geometry with updated position
            for node in self.outputNodes:
                if node.name == 'moved':
                    currShape = self.geo_val[0]
                    if currShape == 'cir':  # For circle
                        x, y = self.geo_val[1]  # Get center point
                        r = self.geo_val[2]     # Get radius
                        node.value = ((x + dx, y + dy), r)
                    elif currShape == 'rect':
                        x, y = self.geo_val[1]  # Get center point
                        w = self.geo_val[2]     # Get width
                        h = self.geo_val[3]     # Get height
                        node.value = ((x + dx, y + dy), w, h)
                        
                    # Propagate the value
                    for connection in node.connections:
                        connection.end_node.receiveValue(node.value)
    
    def draw(self):
        if self.hasAllInputs:
            dx, dy = self.vect_val
            currShape = self.geo_val[0]
            if currShape == 'cir':
                # 如果是圆形
                x, y = self.geo_val[1]  # Get center point
                r = self.geo_val[2]     # Get radius
                # 绘制移动后的圆
                drawCircle(x + dx, y + dy, r,
                        fill=None, border='blue')
                # 绘制移动指示线
                drawLine(x, y, x + dx, y + dy,
                        fill='lightBlue', dashes=True)
            elif currShape == 'rect':
                # 如果是矩形
                x, y = self.geo_val[1]  # Get center point
                w = self.geo_val[2]     # Get width
                h = self.geo_val[3]     # Get height
                # 绘制移动后的矩形
                drawRect(x + dx - w/2, y + dy - h/2,
                        w, h,
                        fill=None, border='blue')
                # 绘制移动指示线
                drawLine(x, y, x + dx, y + dy,
                        fill='lightBlue', dashes=True)

