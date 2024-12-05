'''
- Component: 
  - TypicleComponent:
      - UnaryOperator: Reverse, Square, SquareRoot, MultiplyPi, Absolute
      - BinaryOperator: Add, Subtract, Multiply, Divide
      - Series
'''

from Components import TypicleComponent
from cmu_graphics import *

## HELPER: 
def alignLists(L, M, default_value=None):
    L = [L] if not isinstance(L, list) else L
    M = [M] if not isinstance(M, list) else M
    
    if len(L) < len(M):
        last_item = L[-1] if L else default_value
        L.extend([last_item] * (len(M) - len(L)))
      
    elif len(M) < len(L):
        last_item = M[-1] if M else default_value
        M.extend([last_item] * (len(L) - len(M)))
    
    return L, M

########################################################################################
# UnaryOperator
# output representation: v or [v1, v2, v3, ...]
########################################################################################

class UnaryOperator(TypicleComponent):
    def __init__(self, app, operator, symbol):
        inputs = ['n']
        outputs = ['result']
        name = f'{symbol}\nNumber\n{operator}'
        self.isGeo = False
        super().__init__(app, inputs, outputs, name)
        
        self.inputDefaultValue = {'n': 0}
        
        for node in self.inputNodes:
            node.value = self.inputDefaultValue[node.name]
        self.outputNodes[0].value = self.calculate()

        self.hasAllInputs = True
        self.operator = operator
    
    def performOperation(self, n):  
        if self.operator == '-': return -n
        elif self.operator == '²': return n * n
        elif self.operator == '√': return abs(n) ** 0.5
        elif self.operator == 'π×': return n * 3.14159
        elif self.operator == '|x|': return abs(n)
    
    def calculate(self):  
        n_val = self.inputNodes[0].value
        n_val = [n_val] if not isinstance(n_val, list) else n_val
        result = []
        for n in n_val:
            result.append(self.performOperation(n))
        return result

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

########################################################################################
# UnaryOperator
# output representation: v or [v1, v2, v3, ...]
########################################################################################

class BinaryOperator(TypicleComponent):
    def __init__(self, app, operator, symbol):
        inputs = ['n_1', 'n_2']
        outputs = ['result']
        name = f'{symbol}\nNumber\n{operator}'
        self.isGeo = False
        super().__init__(app, inputs, outputs, name)
        
        self.inputDefaultValue = {
            'n_1': 0,
            'n_2': 0 if operator != '÷' else 1
        }
        
        for node in self.inputNodes:
            node.value = self.inputDefaultValue[node.name]
            
        self.outputNodes[0].value = 0
        self.hasAllInputs = True
        self.operator = operator
    
    def performOperation(self, n1, n2):
        if self.operator == '+': return n1 + n2
        elif self.operator == '-': return n1 - n2
        elif self.operator == '×': return n1 * n2
        elif self.operator == '÷': return n1 / (n2 if n2 != 0 else 1)
    
    def calculate(self):
        n1_val = self.inputNodes[0].value
        n2_val = self.inputNodes[1].value

        n1_val = [n1_val] if not isinstance(n1_val, list) else n1_val
        n2_val = [n2_val] if not isinstance(n2_val, list) else n2_val

        n1_val, n2_val = alignLists(n1_val, n2_val, default_value=0)

        results = [self.performOperation(n1, n2) for n1, n2 in zip(n1_val, n2_val)]

        return results

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

########################################################################################
# SERIES
# output representation: [v1, v2, v3, ...]
########################################################################################

class Series(TypicleComponent):
    def __init__(self, app):
        inputs = ['First', 'Step', 'Count']
        outputs = ['List']
        name = 'Data\nSeries\n➜➜➜'
        super().__init__(app, inputs, outputs, name)
        
        self.isGeo = False

        # Set default values
        self.inputDefaultValue = {
            'First': 0,
            'Step': 20,
            'Count': 5
        }
        
        # Initialize input nodes with default values
        for node in self.inputNodes:
            node.value = self.inputDefaultValue[node.name]
            
        # Initialize output node with calculated value
        initial_output = self.calculate()
        self.outputNodes[0].value = initial_output
        self.hasAllInputs = True
        
    def calculate(self):
        first = self.inputNodes[0].value
        step = self.inputNodes[1].value
        count = self.inputNodes[2].value
        try:
            series = [first + i * step for i in range(count)]
            return series
        except (ValueError, TypeError):
            return []
