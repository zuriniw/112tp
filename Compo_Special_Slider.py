from Components import Component
from cmu_graphics import *
from Node import *

def processValueWithPrecision(value, precision_value):
    if precision_value == 0.1:
        return float(f"{value:.1f}")
    return int(value / precision_value + 0.5) * precision_value

class Slider(Component):
    def __init__(self, app, name='Slider'):
        inputs = []
        outputs = ['value']
        super().__init__(app)
        self.name = name
        self.outputs = outputs
        self.outputNodes = [Node(output, self, True) for output in outputs]
        
        self.width = 120
        self.height = 32
        self.outputHeight = app.textHeight
        self.nickname = ''

        self.isDragging = False
        self.isDraggingHandle = False
        
        self.precision_options = [10, 1, 0.1]
        self.current_precision_index = 1
        
        self.updateNodePositions()
    
    def getValue(self):
        precision = self.precision_options[self.current_precision_index]
        return processValueWithPrecision(self.outputNodes[0].value, precision)
    
    def updateValue(self, value):
        precision = self.precision_options[self.current_precision_index]
        processed_value = processValueWithPrecision(value, precision)
        self.outputNodes[0].value = processed_value
        
        for connection in self.outputNodes[0].connections:
            connection.end_node.receiveValue(processed_value)



class Slider1D(Slider):
    def __init__(self, app, name='Slider\n1D\n<-->', min_val=-200, max_val=200):
        super().__init__(app, name)
        self.min_val = min_val
        self.max_val = max_val
        self.handleWidth = 12
        self.isDraggingHandle = False
        self.isPinned = False
        
        self.outputNodes[0].value = (min_val + max_val) / 2
        
        self.fields = {
            'nickname': self.nickname,
            'value': str(self.getValue()),
            'min': str(self.min_val),
            'max': str(self.max_val),
            'precision': f'{self.precision_options[self.current_precision_index]} decimal',
            'pin': self.isPinned
        }
    
    def updateFields(self):
        self.fields.update({
            'nickname': self.nickname,
            'value': str(self.getValue()),
            'min': str(self.min_val),
            'max': str(self.max_val),
            'precision': f'{self.precision_options[self.current_precision_index]} decimal',
            'pin': self.isPinned
        })
        
        # check the domain, if not in the domain, run to the boundry
        current_value = self.getValue()
        if current_value < self.min_val:
            self.updateValue(self.min_val)
        elif current_value > self.max_val:
            self.updateValue(self.max_val)
        
        # syn to the pinned
        if self.isPinned:
            for pinned_slider in self.app.pinnedSliders:
                if pinned_slider.original_slider == self:
                    pinned_slider.syncWithOriginal()

    def calculate(self):
        # current slider's value
        return self.getValue()
    
    def hitTestHandle(self, mouseX, mouseY):
        handleX = self.x + ((self.getValue() - self.min_val) / 
                           (self.max_val - self.min_val)) * (self.width - self.handleWidth)
        return (handleX <= mouseX <= handleX + self.handleWidth and 
                self.y <= mouseY <= self.y + self.height)
    
    def drawUI(self):
        for node in self.outputNodes:
            node.drawNode()
            
        drawRect(self.x, self.y, self.width, self.height, 
                fill='white' if not self.isSelected else 'lightGrey', 
                border='black')
        
        handleX = self.x + ((self.getValue() - self.min_val) / 
                           (self.max_val - self.min_val)) * (self.width-self.handleWidth)
        drawRect(handleX, self.y, self.handleWidth, self.height, fill='black')
        
        drawLabel(f'{self.getValue()}', handleX, self.y - 10)
        
        if self.nickname:
            appendix = ' ^ ' if self.isPinned else ''
            drawLabel(f'[ {self.nickname} ]'+ appendix, 
                     self.x + self.width/2, self.y+self.height+8, size=12)

    def handleDrag(self, mouseX, mouseY):
        normalized_x = (mouseX - self.x) / self.width
        newValue = self.min_val + normalized_x * (self.max_val - self.min_val)
        newValue = max(self.min_val, min(self.max_val, newValue))

        self.updateValue(newValue)

class PinnedSlider1D(Slider):
    def __init__(self, original_slider, app):
        super().__init__(app, original_slider.name)
        self.original_slider = original_slider
        self.min_val = original_slider.min_val
        self.max_val = original_slider.max_val
        self.current_precision_index = original_slider.current_precision_index
        self.outputNodes[0].value = original_slider.getValue()
    
    def syncWithOriginal(self):
        self.min_val = self.original_slider.min_val
        self.max_val = self.original_slider.max_val
        self.current_precision_index = self.original_slider.current_precision_index
    
    def updateValue(self, value):
        precision = self.precision_options[self.current_precision_index]
        processed_value = processValueWithPrecision(value, precision)
        
        self.outputNodes[0].value = processed_value
        self.original_slider.outputNodes[0].value = processed_value
        
        # update connection
        for connection in self.original_slider.outputNodes[0].connections:
            connection.end_node.receiveValue(processed_value)

    def updateFields(self):
        self.min_val = self.original_slider.min_val
        self.max_val = self.original_slider.max_val
        self.current_precision_index = self.original_slider.current_precision_index
        
        # ensure in the domain
        current_value = self.getValue()
        new_value = max(self.min_val, min(self.max_val, current_value))
        if current_value != new_value:
            self.updateValue(new_value)

    def calculate(self):
        # current slider's value
        return self.getValue()
    
    def hitTestHandle(self, mouseX, mouseY, x, y):
        trackY = y + self.height/2
        handleX = x + ((self.getValue() - self.min_val) / 
                      (self.max_val - self.min_val)) * self.width
        handleRadius = 7
        distance = ((mouseX - handleX)**2 + (mouseY - trackY)**2)**0.5
        return distance <= handleRadius
    
    def drawTwinUI(self, x, y):
        trackY = y + self.height/2
        drawLine(x, trackY, x + self.width, trackY,
                fill='black', lineWidth=2)
        
        # draw the small lines
        for i in range(11):
            tickX = x + (i / 10) * self.width
            drawLine(tickX, trackY - 2.5, tickX, trackY + 2.5,
                    fill='black', lineWidth=1)
        # draw the handle
        handleX = x + ((self.getValue() - self.min_val) / 
                      (self.max_val - self.min_val)) * self.width
        drawCircle(handleX, trackY, 7, fill='white', border='black')
        
        # draw the value and nickname
        drawLabel(f'{self.getValue()}', handleX, y - 5, size=12)
        if self.original_slider.nickname:
            drawLabel(f'[ {self.original_slider.nickname} ]',
                     x + self.width/2, y + self.height + 12, size=12)

class Slider2D(Slider):
    def __init__(self, app, name='Slider\n2D\n<-|->', min_val=-100, max_val=100):
        # Call parent class constructor with correct parameters
        super().__init__(app, name)
        self.min_val = min_val
        self.max_val = max_val
        self.isPinned = False

        # Modify outputs for 2D
        self.outputs = ['x', 'y']
        self.outputNodes = [Node('x', self, True), Node('y', self, True)]
        
        # Set dimensions
        self.width = 120
        self.height = 120
        self.handleSize = 14
        
        # Initialize values
        self.outputNodes[0].value = (min_val + max_val) / 2  # x值
        self.outputNodes[1].value = (min_val + max_val) / 2  # y值
        
        # dragging related
        self.isDragging = False
        self.isDraggingHandle = False

        # field
        self.fields = {
            'nickname': self.nickname,
            'x': str(self.getValues()[0]),
            'y': str(self.getValues()[1]),
            'min': str(self.min_val),
            'max': str(self.max_val),
            'precision': f'{self.precision_options[self.current_precision_index]} decimal',
            'pin': self.isPinned
        }
        

    def getValues(self):
        precision = self.precision_options[self.current_precision_index]
        return (processValueWithPrecision(self.outputNodes[0].value, precision),
                processValueWithPrecision(self.outputNodes[1].value, precision))
    def calculate(self):
        # current slider's value
        return self.getValue()

    def updateValue(self, x_val, y_val):
        precision = self.precision_options[self.current_precision_index]
        processed_x = processValueWithPrecision(x_val, precision)
        processed_y = processValueWithPrecision(y_val, precision)
        
        # update node value
        self.outputNodes[0].value = processed_x
        self.outputNodes[1].value = processed_y
        
        # update fields in the right click menu
        self.fields.update({
            'x': str(processed_x),
            'y': str(processed_y)
        })
        
        # notify the connections, broadcast to the lower nodes
        for connection in self.outputNodes[0].connections:
            connection.end_node.receiveValue(processed_x)
        for connection in self.outputNodes[1].connections:
            connection.end_node.receiveValue(processed_y)
        
        # pinned sync
        if self.isPinned:
            for pinned_slider in self.app.pinnedSliders:
                if pinned_slider.original_slider == self:
                    pinned_slider.outputNodes[0].value = processed_x
                    pinned_slider.outputNodes[1].value = processed_y

    def updateFields(self):
        x_val, y_val = self.getValues()
        
        # check the domain
        if x_val < self.min_val or x_val > self.max_val or y_val < self.min_val or y_val > self.max_val:
            new_x = max(self.min_val, min(self.max_val, x_val))
            new_y = max(self.min_val, min(self.max_val, y_val))
            self.updateValue(new_x, new_y)
        
        self.fields.update({
            'nickname': self.nickname,
            'x': str(x_val),
            'y': str(y_val),
            'min': str(self.min_val),
            'max': str(self.max_val),
            'precision': f'{self.precision_options[self.current_precision_index]} decimal',
            'pin': self.isPinned
        })
        
        if self.isPinned:
            for pinned_slider in self.app.pinnedSliders:
                if pinned_slider.original_slider == self:
                    pinned_slider.syncWithOriginal()

    def hitTestHandle(self, mouseX, mouseY):
        x_val, y_val = self.getValues()
        handleX = self.x + ((x_val - self.min_val) / 
                        (self.max_val - self.min_val)) * self.width
        handleY = self.y + (1 - (y_val - self.min_val) / 
                        (self.max_val - self.min_val)) * self.height
        
        return (abs(mouseX - handleX) <= self.handleSize/2 and 
                abs(mouseY - handleY) <= self.handleSize/2)

    def drawUI(self): 
        # node
        for node in self.outputNodes:
            node.drawNode()
        # background
        drawRect(self.x, self.y, self.width, self.height, 
                fill='white' if not self.isSelected else 'lightGrey',
                border='black')
        # grid
        for i in range(1, 10):
            lineX = self.x + (i/10) * self.width
            lineY = self.y + (i/10) * self.height
            drawLine(lineX, self.y, lineX, self.y + self.height,
                    fill='lightGray', lineWidth=1)
            drawLine(self.x, lineY, self.x + self.width, lineY,
                    fill='lightGray', lineWidth=1) 
        # handler
        x_val, y_val = self.getValues()
      
        handleX = self.x + ((x_val - self.min_val) / 
                        (self.max_val - self.min_val)) * self.width
        handleY = self.y + (1 - (y_val - self.min_val) / 
                        (self.max_val - self.min_val)) * self.height
        drawLine(handleX, self.y, handleX, self.y + self.height,
                fill='black', lineWidth=1, opacity=50)
        drawLine(self.x, handleY, self.x + self.width, handleY,
                fill='black', lineWidth=1, opacity=50)
        drawRect(handleX - self.handleSize/2, handleY - self.handleSize/2,
                self.handleSize, self.handleSize,
                fill='black')
        # corodinate
        drawLabel(f'({x_val}, {y_val})', handleX, self.y - 10)   
        # nickname
        if self.nickname:
            appendix = ' ^ ' if self.isPinned else ''
            drawLabel(f'[ {self.nickname} ]'+ appendix,
                     self.x + self.width/2, self.y + self.height + 12,
                     size=12)          
        # frame
        drawRect(self.x, self.y, self.width, self.height, fill= None, border='black')
        


    def handleDrag(self, mouseX, mouseY):
        # related coordinate
        normalizedX = (mouseX - self.x) / self.width
        normalizedY = 1 - (mouseY - self.y) / self.height      # flip!
        
        # transform coordinate
        newX = self.min_val + normalizedX * (self.max_val - self.min_val)
        newY = self.min_val + normalizedY * (self.max_val - self.min_val)
        
        # in domain
        newX = max(self.min_val, min(self.max_val, newX))
        newY = max(self.min_val, min(self.max_val, newY))
        
        self.updateValue(newX, newY)



class PinnedSlider2D(Slider2D):
    def __init__(self, original_slider, app):
        super().__init__(app, 
                        name=original_slider.name,
                        min_val=original_slider.min_val,
                        max_val=original_slider.max_val)
        self.oriSlider = original_slider
        self.outputNodes[0].value = original_slider.getValues()[0]
        self.outputNodes[1].value = original_slider.getValues()[1]
        self.current_precision_index = original_slider.current_precision_index
        
    def syncWithOriginal(self):
        self.min_val = self.oriSlider.min_val
        self.max_val = self.oriSlider.max_val
        self.current_precision_index = self.oriSlider.current_precision_index
        # in domain
        x_val, y_val = self.getValues()
        new_x = max(self.min_val, min(self.max_val, x_val))
        new_y = max(self.min_val, min(self.max_val, y_val))
        if x_val != new_x or y_val != new_y:
            self.updateValue(new_x, new_y)

    def updateValue(self, x_val, y_val):
        precision = self.precision_options[self.current_precision_index]
        processed_x = processValueWithPrecision(x_val, precision)
        processed_y = processValueWithPrecision(y_val, precision)
        
        self.outputNodes[0].value = processed_x
        self.outputNodes[1].value = processed_y
        self.oriSlider.outputNodes[0].value = processed_x
        self.oriSlider.outputNodes[1].value = processed_y
        
        # update fields
        self.oriSlider.fields.update({
            'x': str(processed_x),
            'y': str(processed_y)
        })
        
        # broadcast
        for connection in self.oriSlider.outputNodes[0].connections:
            connection.end_node.receiveValue(processed_x)
        for connection in self.oriSlider.outputNodes[1].connections:
            connection.end_node.receiveValue(processed_y)

    def calculate(self):
        return self.getValue()

    def hitTestHandle(self, mouseX, mouseY, x, y):
        x_val, y_val = self.getValues()
        handleX = x + ((x_val - self.min_val) / 
                    (self.max_val - self.min_val)) * self.width
        handleY = y + (1-(y_val - self.min_val) / 
                    (self.max_val - self.min_val)) * self.height
        distance = ((mouseX - handleX)**2 + (mouseY - handleY)**2)**0.5
        return distance <= self.handleSize/2

    def drawTwinUI(self, x, y):
        # background
        drawRect(x, y, self.width, self.height,
                fill='white', border='black')      
        # grid
        for i in range(1, 10):
            lineX = x + (i/10) * self.width
            lineY = y + (i/10) * self.height
            drawLine(lineX, y, lineX, y + self.height,
                    fill='lightGray', lineWidth=0.5)
            drawLine(x, lineY, x + self.width, lineY,
                    fill='lightGray', lineWidth=0.5)       
        # handle
        x_val, y_val = self.getValues()
        handleX = x + ((x_val - self.min_val) / 
                   (self.max_val - self.min_val)) * self.width
        handleY = y + (1-(y_val - self.min_val) / 
               (self.max_val - self.min_val)) * self.height
        # crossing
        drawLine(handleX, y, handleX, y + self.height,
                fill='black', lineWidth=1, opacity=30)
        drawLine(x, handleY, x + self.width, handleY,
                fill='black', lineWidth=1, opacity=30)
        
        drawCircle(handleX, handleY, self.handleSize/2,
                fill='white', border='black')
        #label
        drawLabel(f'({x_val}, {y_val})', handleX, y - 10)
        # nickname
        if self.oriSlider.nickname:
            drawLabel(f'[ {self.oriSlider.nickname} ]',
                    x + self.width/2, y + self.height + 12,
                    size=12)