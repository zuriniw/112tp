'''
- Component
    - Panel
'''

from cmu_graphics import *
from Components import *

########################################################################################
# PANEL is for reveal the value of any outputNode 
#       1.panel can show the list of geo representation/values
########################################################################################

class Panel(Component):
    def __init__(self, app):
        inputs = ['value']
        outputs = []
        super().__init__(app)
        
        self.name = 'Create\nPanel\n[/]'
        self.inputs = inputs
        self.inputNodes = [Node(input_type, self, False) for input_type in inputs]
        
        # Add inputHeight attribute
        self.inputHeight = app.textHeight
        
        self.inputDefaultValue = {
            'value': None,
        }

        self.width = 160
        self.height = 60
        self.value = None
        self.isGeo = False
        self.updateNodePositions()

    def getDefaultValue(self, nodeName):
            return self.inputDefaultValue.get(nodeName)

    def drawUI(self):
        # Draw node
        for node in self.inputNodes:
            node.drawNode()

        # Calculate dynamic height based on content
        if self.value is not None and isinstance(self.value, list):
            line_height = 20
            max_display_lines = 12
            label_count = min(len(self.value), max_display_lines) + 1
            self.height = self.app.borderY * 2.2 + label_count * line_height

        # Draw background
        drawRect(self.x, self.y, self.width, self.height,
                fill='white' if not self.isSelected else 'lightGrey',
                border='black')

        # Draw value
        if self.value is not None:
            if isinstance(self.value, list) and len(self.value) > 0:
                line_height = 20
                start_y = self.y + self.app.borderY * 1.1

                # Display first line with total items count
                drawLabel(f'{len(self.value)} items in total',
                        self.x + self.width/2,
                        start_y,
                        size=12,
                        fill='grey')

                # Display up to 12 lines
                for i in range(min(len(self.value), 12)):
                    drawLabel(f'{self.value[i]}',
                            self.x + self.width/2,
                            start_y + (i+1) * line_height,
                            size=12)
                
                # Add ellipsis if more than 12 lines
                if len(self.value) > 12:
                    drawLabel('...',
                            self.x + self.width/2,
                            start_y + 13 * line_height,
                            size=12,
                            fill='grey')
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

                