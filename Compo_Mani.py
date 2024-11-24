from cmu_graphics import *
from Components import *

class Move(TypicleComponent):
    def __init__(self, app):
        inputs = ['geo','vect']
        outputs = ['moved']
        name = 'Move\nGeo\n↗'
        self.isGeo = True
        super().__init__(app, inputs, outputs, name)
        self.geo_val = None
        self.vect_val = None
        self.hasAllInputs = False
    
    def updateValue(self, nodeName, value):
        if nodeName == 'geo':
            self.n_val = value
            self.hasAllInputs = (self.n_val is not None and self.vect_val is not None)
            
            # 如果有输入值，计算并更新输出节点的值
            if self.hasAllInputs:
                opposite_val = -self.n_val
                # 更新输出节点的值
                for node in self.outputNodes:
                    if node.name == 'opposite':
                        node.value = opposite_val
                        # 通过输出节点传递值
                        for connection in node.connections:
                            connection.end_node.receiveValue(opposite_val)