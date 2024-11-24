from Components import TypicleComponent
from cmu_graphics import *

class Reverse(TypicleComponent):
    def __init__(self, app):
        inputs = ['n']
        outputs = ['opposite']
        name = 'Reverse\nNumber'
        self.isGeo = False
        super().__init__(app, inputs, outputs, name)
        self.n_val = None
        self.hasAllInputs = False
    
    def updateValue(self, nodeName, value):
        if nodeName == 'n':
            self.n_val = value
            self.hasAllInputs = (self.n_val is not None)
            
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

class BinaryOperator(TypicleComponent):
    def __init__(self, app, operator, symbol):
        inputs = ['n_1', 'n_2']
        outputs = ['result']
        name = f'{symbol}\nNumber\n{operator}'
        self.isGeo = False
        super().__init__(app, inputs, outputs, name)
        
        self.inputDefaultValue = {
            'n_1': 0,
            'n_2': 0 if operator != '÷' else 1  # 除法默认除数为1
        }
        
        # 设置默认值
        for node in self.inputNodes:
            node.value = self.inputDefaultValue[node.name]
            
        # 初始化输出值
        self.outputNodes[0].value = 0
        self.hasAllInputs = True
        self.operator = operator
    
    def calculate(self, n1, n2):
        if self.operator == '+': return n1 + n2
        elif self.operator == '-': return n1 - n2
        elif self.operator == '×': return n1 * n2
        elif self.operator == '÷': return n1 / (n2 if n2 != 0 else 1)
    
    def updateValue(self, nodeName, value):
        # 更新输入节点值
        for node in self.inputNodes:
            if node.name == nodeName:
                node.value = value
        
        # 计算并更新输出
        n1_val = self.inputNodes[0].value
        n2_val = self.inputNodes[1].value
        result = self.calculate(n1_val, n2_val)
        
        for node in self.outputNodes:
            if node.name == 'result':
                node.value = result
                for connection in node.connections:
                    connection.end_node.receiveValue(result)
                    
class Add(BinaryOperator):
    def __init__(self, app):
        super().__init__(app, '+', 'Add')

class Subtract(BinaryOperator):
    def __init__(self, app):
        super().__init__(app, '-', 'Sub')

class Multiply(BinaryOperator):
    def __init__(self, app):
        super().__init__(app, '×', 'Mul')

class Divide(BinaryOperator):
    def __init__(self, app):
        super().__init__(app, '÷', 'Div')
