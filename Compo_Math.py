'''
MATH is for operation of single value/list of values: 
- Component: 
  - TypicleComponent:
      - UnaryOperator: Reverse, Square, SquareRoot, MultiplyPi, Absolute
      - BinaryOperator: Add, Subtract, Multiply, Divide
'''

from Components import TypicleComponent
from cmu_graphics import *

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

        n1_val, n2_val = align_lists(n1_val, n2_val, default_value=0)

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

def align_lists(list1, list2, default_value=None):
    list1 = [list1] if not isinstance(list1, list) else list1
    list2 = [list2] if not isinstance(list2, list) else list2
    
    if len(list1) < len(list2):
        last_item = list1[-1] if list1 else default_value
        list1.extend([last_item] * (len(list2) - len(list1)))
      
    elif len(list2) < len(list1):
        last_item = list2[-1] if list2 else default_value
        list2.extend([last_item] * (len(list1) - len(list2)))
    
    return list1, list2
