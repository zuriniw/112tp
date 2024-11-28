from cmu_graphics import *
from Components import *

class Panel(Component):
    def __init__(self, app):
        inputs = ['value']
        outputs = []
        super().__init__(app)
        
        self.name = 'Panel'
        self.inputs = inputs
        self.inputNodes = [Node(input_type, self, False) for input_type in inputs]
        
        # Add inputHeight attribute
        self.inputHeight = app.textHeight
        
        self.inputDefaultValue = {
            'value': None,
        }

        self.width = 120
        self.height = 60
        self.value = None
        
        self.updateNodePositions()

    def getDefaultValue(self, nodeName):
            return self.inputDefaultValue.get(nodeName)

    def drawUI(self):
        # Draw node
        for node in self.inputNodes:
            node.drawNode()
        
        # Draw background
        drawRect(self.x, self.y, self.width, self.height, 
                 fill='white' if not self.isSelected else 'lightGrey', 
                 border='black')
        
        # Draw value
        if self.value is not None:
            drawLabel(f'{self.value}', 
                      self.x + self.width/2, 
                      self.y + self.height/2, 
                      size=16)
        else:
            drawLabel('Feed food 4 me!', 
                      self.x + self.width/2, 
                      self.y + self.height/2, 
                      fill='grey')

    def receiveValue(self, value):
        # Update the displayed value when input changes
        self.value = value

    def updateValue(self, name, value):
        # Update the panel's displayed value
        if name == 'value':
            self.value = value
            # Optionally, propagate the value to connected nodes if needed
            for node in self.inputNodes:
                if node.name == name:
                    node.value = value