from Components import TypicleComponent
from cmu_graphics import *

class UnaryOperator(TypicleComponent):
    def __init__(self, app, operator, symbol):
        inputs = ['n']
        outputs = ['result']
        name = f'{symbol}\nNumber\n{operator}'
        self.isGeo = False
        super().__init__(app, inputs, outputs, name)
        
        self.inputDefaultValue = {
            'n': 0
        }
        
        # 设置默认值
        for node in self.inputNodes:
            node.value = self.inputDefaultValue[node.name]
            
        # 初始化输出值
        self.outputNodes[0].value = 0
        self.hasAllInputs = True
        self.operator = operator
    
    def calculate(self, n):
        if self.operator == '-': return -n
        elif self.operator == '²': return n * n
        elif self.operator == '√': return abs(n) ** 0.5
        elif self.operator == 'π×': return n * 3.14159
        elif self.operator == '|x|': return abs(n)
    
    def updateValue(self, nodeName, value):
        # 更新输入节点值
        for node in self.inputNodes:
            if node.name == nodeName:
                node.value = value
        
        # 计算并更新输出
        n_val = self.inputNodes[0].value
        result = self.calculate(n_val)
        
        for node in self.outputNodes:
            if node.name == 'result':
                node.value = result
                for connection in node.connections:
                    connection.end_node.receiveValue(result)
                    
class Reverse(UnaryOperator):
    def __init__(self, app):
        super().__init__(app, '-', 'Rev')

class Square(UnaryOperator):
    def __init__(self, app):
        super().__init__(app, '²', 'Sqr')

class SquareRoot(UnaryOperator):
    def __init__(self, app):
        super().__init__(app, '√', 'Sqrt')

class MultiplyPi(UnaryOperator):
    def __init__(self, app):
        super().__init__(app, 'π×', 'Pi')

class Absolute(UnaryOperator):
    def __init__(self, app):
        super().__init__(app, '|x|', 'Abs')


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
