from cmu_graphics import *
from Components import TypicleComponent

class Move(TypicleComponent):
    def __init__(self, app):
        inputs = ['geo', 'vector']
        outputs = ['moved']
        name = 'Move\nGeo\n↗'
        self.isGeo = True
        self.isDisplay = True
        super().__init__(app, inputs, outputs, name)
        
        self.inputDefaultValue = {
            'geo': None,
            'vector': (200, -200)
        }
        
        for node in self.inputNodes:
            node.value = self.inputDefaultValue[node.name]
            
        self.hasAllInputs = False
    
    def calculate(self):
        geo_val = self.inputNodes[0].value
        dx, dy = self.inputNodes[1].value
        
        if not geo_val or not isinstance(geo_val, list):
            return [None]
            
        currShape = geo_val[0]
        if currShape == 'cir':
            x, y = geo_val[1]
            r = geo_val[2]
            return [['cir', (x + dx, y + dy), r]]
        elif currShape == 'rect':
            x, y = geo_val[1]
            w = geo_val[2]
            h = geo_val[3]
            return [['rect', (x + dx, y + dy), w, h]]
        elif currShape == 'point':
            x, y = geo_val[1]
            #r = geo_val[2]
            return [['point', (x + dx, y + dy)]]
    
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
                if int(r) != 0:
                    drawCircle(x + dx, y + dy, r, fill=None, border='blue',visible=self.isDisplay)
            elif currShape == 'rect':
                w = geo_val[2]
                h = geo_val[3]
                if int(w) != 0 and int(h) != 0:
                    drawRect(x + dx - w/2, y + dy - h/2, w, h, fill=None, border='blue',visible=self.isDisplay)
            elif currShape == 'point':
                #r = geo_val[2]
                drawCircle(x + dx, y + dy, 4, fill='white', border='blue', borderWidth=2,visible=self.isDisplay)
            
            drawLine(x, y, x + dx, y + dy, fill='lightBlue', dashes=True,visible=self.isDisplay)

