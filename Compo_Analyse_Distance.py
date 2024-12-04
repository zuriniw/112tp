from cmu_graphics import *
from Components import *

class Distance(TypicleComponent):
    def __init__(self, app):
        inputs = ['shapeA', 'shapeB']
        outputs = ['distance']
        name = 'Measure\nDistance\n⟷'
        
        self.isGeo = False
        self.isDisplay = False
        
        super().__init__(app, inputs, outputs, name)
        
        self.inputDefaultValue = {
            'shapeA': [['point', (app.x0, app.y0)]],
            'shapeB': [['point', (app.x0+200, app.y0)]]
        }
        
        for node in self.inputNodes:
            node.value = self.inputDefaultValue[node.name]
        self.outputNodes[0].value = self.calculate()
        
        self.hasAllInputs = True

    def calculate(self):
        shapeA_val = self.inputNodes[0].value
        shapeB_val = self.inputNodes[1].value        
        distances = []
        for a in shapeA_val:
            for b in shapeB_val:
                # extract position info
                a_pos = a[1] if a[0] in ['point', 'rect', 'cir'] else None
                b_pos = b[1] if b[0] in ['point', 'rect', 'cir'] else None
                
                if a_pos and b_pos:
                    distance = ((a_pos[0] - b_pos[0])**2 + (a_pos[1] - b_pos[1])**2)**0.5
                    distances.append(distance)
        
        return distances if distances else [[0]]