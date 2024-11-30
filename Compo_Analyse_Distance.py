from cmu_graphics import *
from Components import *

class Distance(TypicleComponent):
    def __init__(self, app):
        inputs = ['shapeA', 'shapeB']
        outputs = ['distance']
        name = 'Distance\n⟷'
        
        self.isGeo = False
        self.isDisplay = False
        
        super().__init__(app, inputs, outputs, name)
        
        self.inputDefaultValue = {
            'shapeA': [['point', (app.x0, app.y0)]],
            'shapeB': [['point', (app.x0+200, app.y0)]]
        }
        
        for node in self.inputNodes:
            node.value = self.inputDefaultValue[node.name]
        
        self.hasAllInputs = True

    def calculate(self):
        shapeA_val = self.inputNodes[0].value
        shapeB_val = self.inputNodes[1].value
        
        distances = []
        
        # 处理不同形状的距离计算
        for a in shapeA_val:
            for b in shapeB_val:
                # 提取位置信息
                a_pos = a[1] if a[0] in ['point', 'rect', 'cir'] else None
                b_pos = b[1] if b[0] in ['point', 'rect', 'cir'] else None
                
                if a_pos and b_pos:
                    # 计算欧几里得距离
                    distance = ((a_pos[0] - b_pos[0])**2 + (a_pos[1] - b_pos[1])**2)**0.5
                    distances.append(distance)
        
        return distances if distances else [[0]]