from cmu_graphics import *
from Components import TypicleComponent

class Move(TypicleComponent):
    def __init__(self, app):
        inputs = ['geo', 'vector']
        outputs = ['moved']
        name = 'Move\nGeo\n↗'
        self.isGeo = True
        super().__init__(app, inputs, outputs, name)
        
        self.inputDefaultValue = {
            'geo': None,
            'vector': (200, -200)
        }
        
        for node in self.inputNodes:
            node.value = self.inputDefaultValue[node.name]
            
        self.hasAllInputs = False
    
    def draw(self):
        if self.hasAllInputs:
            geo_val = self.inputNodes[0].value
            vector_val = self.inputNodes[1].value
            
            if not geo_val or not vector_val or len(geo_val) < 2:
                return
                
            currShape = geo_val[0]
            x, y = geo_val[1]
            dx, dy = vector_val
            
            if currShape == 'cir':
                r = geo_val[2]
                drawCircle(x + dx, y + dy, r, fill=None, border='blue')
            elif currShape == 'rect':
                w = geo_val[2]
                h = geo_val[3]
                drawRect(x + dx - w/2, y + dy - h/2, w, h, fill=None, border='blue')
            
            # 绘制移动指示线
            drawLine(x, y, x + dx, y + dy, fill='lightBlue', dashes=True)

    
    def updateValue(self, nodeName, value):
        # Update input node value
        for node in self.inputNodes:
            if node.name == nodeName:
                node.value = value
        
        self.hasAllInputs = all(node.value is not None for node in self.inputNodes)
        
        if self.hasAllInputs:
            geo_val = self.inputNodes[0].value
            dx, dy = self.inputNodes[1].value
            
            if not geo_val or not isinstance(geo_val, list):
                return
                
            for node in self.outputNodes:
                if node.name == 'moved':
                    currShape = geo_val[0]
                    if currShape == 'cir':
                        x, y = geo_val[1]
                        r = geo_val[2]
                        # 直接使用 dx, dy，不需要改变 dy 的符号
                        node.value = ['cir', (x + dx, y + dy), r]
                    elif currShape == 'rect':
                        x, y = geo_val[1]
                        w = geo_val[2]
                        h = geo_val[3]
                        # 直接使用 dx, dy，不需要改变 dy 的符号
                        node.value = ['rect', (x + dx, y + dy), w, h]
                    
                    for connection in node.connections:
                        connection.end_node.receiveValue(node.value)
