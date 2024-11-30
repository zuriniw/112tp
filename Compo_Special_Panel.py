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
            if isinstance(self.value, list) and len(self.value) > 0:
                # 显示所有数据，不限制行数
                line_height = 20  # 每行文字的高度
                start_y = self.y + 20  # 从顶部开始的偏移
                for i, item in enumerate(self.value):
                    drawLabel(f'{item}',
                            self.x + self.width/2,
                            start_y + i * line_height,
                            size=12)
            else:
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