from Components import Component
from cmu_graphics import *
from Node import *

def processValueWithPrecision(value, precision_value):
    """处理数值精度
    precision_value: 10 代表整数(10的倍数), 1 代表整数, 0.1 代表一位小数"""
    # 避免浮点数精度问题，使用字符串格式化
    if precision_value == 0.1:
        return float(f"{value:.1f}")
    return int(value / precision_value + 0.5) * precision_value

class Slider(Component):
    """基础滑块组件，处理共同属性和方法"""
    def __init__(self, app, name='Slider'):
        inputs = []
        outputs = ['value']
        super().__init__(app)
        self.name = name
        self.outputs = outputs
        self.outputNodes = [Node(output, self, True) for output in outputs]
        
        # 基础属性
        self.width = 120
        self.height = 32
        self.outputHeight = app.textHeight
        self.nickname = ''

        # 添加拖拽相关属性
        self.isDragging = False
        self.isDraggingHandle = False
        
        # 精度控制
        self.precision_options = [10, 1, 0.1]
        self.current_precision_index = 1
        
        self.updateNodePositions()
    
    def getValue(self):
        precision = self.precision_options[self.current_precision_index]
        return processValueWithPrecision(self.outputNodes[0].value, precision)
    
    def updateValue(self, value):
        """基础的值更新方法"""
        precision = self.precision_options[self.current_precision_index]
        processed_value = processValueWithPrecision(value, precision)
        self.outputNodes[0].value = processed_value
        
        for connection in self.outputNodes[0].connections:
            connection.end_node.receiveValue(processed_value)



class Slider1D(Slider):
    """可交互的一维滑块"""
    def __init__(self, app, name='Slider\n1D\n<-->', min_val=-200, max_val=200):
        super().__init__(app, name)
        self.min_val = min_val
        self.max_val = max_val
        self.handleWidth = 12
        self.isDraggingHandle = False
        self.isPinned = False
        
        # 初始化输出节点的值
        self.outputNodes[0].value = (min_val + max_val) / 2
        
        # 右键菜单相关
        self.fields = {
            'nickname': self.nickname,
            'value': str(self.getValue()),
            'min': str(self.min_val),
            'max': str(self.max_val),
            'precision': f'{self.precision_options[self.current_precision_index]} decimal',
            'pin': self.isPinned
        }
    
    def updateFields(self):
        # 先更新字段
        self.fields.update({
            'nickname': self.nickname,
            'value': str(self.getValue()),
            'min': str(self.min_val),
            'max': str(self.max_val),
            'precision': f'{self.precision_options[self.current_precision_index]} decimal',
            'pin': self.isPinned
        })
        
        # 检查当前值是否在新范围内，如果不在则调整到最近的边界值
        current_value = self.getValue()
        if current_value < self.min_val:
            self.updateValue(self.min_val)
        elif current_value > self.max_val:
            self.updateValue(self.max_val)
        
        # 同步到钉住的滑块
        if self.isPinned:
            for pinned_slider in self.app.pinnedSliders:
                if pinned_slider.original_slider == self:
                    pinned_slider.syncWithOriginal()
    
    def hitTestHandle(self, mouseX, mouseY):
        """矩形滑块的碰撞检测"""
        handleX = self.x + ((self.getValue() - self.min_val) / 
                           (self.max_val - self.min_val)) * (self.width - self.handleWidth)
        return (handleX <= mouseX <= handleX + self.handleWidth and 
                self.y <= mouseY <= self.y + self.height)
    
    def drawUI(self):
        """绘制矩形滑块界面"""
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
    """钉住的滑块实现"""
    def __init__(self, original_slider, app):
        super().__init__(app, original_slider.name)
        self.original_slider = original_slider
        self.min_val = original_slider.min_val
        self.max_val = original_slider.max_val
        self.current_precision_index = original_slider.current_precision_index
        self.outputNodes[0].value = original_slider.getValue()
    
    def syncWithOriginal(self):
        """与原始滑块同步所有必要属性"""
        self.min_val = self.original_slider.min_val
        self.max_val = self.original_slider.max_val
        self.current_precision_index = self.original_slider.current_precision_index
    
    def updateValue(self, value):
        """更新值并同步到原始滑块"""
        precision = self.precision_options[self.current_precision_index]
        processed_value = processValueWithPrecision(value, precision)
        
        # 更新自身和原始滑块的值
        self.outputNodes[0].value = processed_value
        self.original_slider.outputNodes[0].value = processed_value
        
        # 更新原始滑块的连接
        for connection in self.original_slider.outputNodes[0].connections:
            connection.end_node.receiveValue(processed_value)
    def updateFields(self):
        """同步更新所有字段"""
        self.min_val = self.original_slider.min_val
        self.max_val = self.original_slider.max_val
        self.current_precision_index = self.original_slider.current_precision_index
        
        # 确保当前值在新范围内
        current_value = self.getValue()
        new_value = max(self.min_val, min(self.max_val, current_value))
        if current_value != new_value:
            self.updateValue(new_value)
    def hitTestHandle(self, mouseX, mouseY, x, y):
        """圆形滑块的碰撞检测"""
        trackY = y + self.height/2
        handleX = x + ((self.getValue() - self.min_val) / 
                      (self.max_val - self.min_val)) * self.width
        handleRadius = 7
        distance = ((mouseX - handleX)**2 + (mouseY - trackY)**2)**0.5
        return distance <= handleRadius
    
    def drawTwinUI(self, x, y):
        """绘制钉住滑块的简化界面"""
        trackY = y + self.height/2
        
        # 绘制轨道
        drawLine(x, trackY, x + self.width, trackY,
                fill='black', lineWidth=2)
        
        # 绘制刻度
        for i in range(11):
            tickX = x + (i / 10) * self.width
            drawLine(tickX, trackY - 2.5, tickX, trackY + 2.5,
                    fill='black', lineWidth=1)
        
        # 绘制滑块
        handleX = x + ((self.getValue() - self.min_val) / 
                      (self.max_val - self.min_val)) * self.width
        drawCircle(handleX, trackY, 7, fill='white', border='black')
        
        # 绘制值和昵称
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
        

        # 添加拖拽相关属性
        self.isDragging = False
        self.isDraggingHandle = False

        # 更新字段显示
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

    def updateValue(self, x_val, y_val):
        precision = self.precision_options[self.current_precision_index]
        processed_x = processValueWithPrecision(x_val, precision)
        processed_y = processValueWithPrecision(y_val, precision)
        
        # 统一更新所有值
        self.outputNodes[0].value = processed_x
        self.outputNodes[1].value = processed_y
        
        # 更新字段显示
        self.fields.update({
            'x': str(processed_x),
            'y': str(processed_y)
        })
        
        # 更新连接的节点
        for connection in self.outputNodes[0].connections:
            connection.end_node.receiveValue(processed_x)
        for connection in self.outputNodes[1].connections:
            connection.end_node.receiveValue(processed_y)
        
        # 如果被钉住，同步更新pinned slider的值
        if self.isPinned:
            for pinned_slider in self.app.pinnedSliders:
                if pinned_slider.original_slider == self:
                    pinned_slider.outputNodes[0].value = processed_x
                    pinned_slider.outputNodes[1].value = processed_y

    def updateFields(self):
        x_val, y_val = self.getValues()
        
        # 检查当前值是否在新范围内
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
        # 绘制节点
        for node in self.outputNodes:
            node.drawNode()
        # 绘制背景
        drawRect(self.x, self.y, self.width, self.height, 
                fill='white' if not self.isSelected else 'lightGrey',
                border='black')
        # 绘制网格线
        for i in range(1, 10):
            lineX = self.x + (i/10) * self.width
            lineY = self.y + (i/10) * self.height
            drawLine(lineX, self.y, lineX, self.y + self.height,
                    fill='lightGray', lineWidth=1)
            drawLine(self.x, lineY, self.x + self.width, lineY,
                    fill='lightGray', lineWidth=1)
            
        # 绘制手柄
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
        
        
        # 绘制坐标值
        drawLabel(f'({x_val}, {y_val})', handleX, self.y - 10)
        
        # 绘制昵称
        if self.nickname:
            appendix = ' ^ ' if self.isPinned else ''
            drawLabel(f'[ {self.nickname} ]'+ appendix,
                     self.x + self.width/2, self.y + self.height + 12,
                     size=12)
        
        # 绘制背景网格
        drawRect(self.x, self.y, self.width, self.height, fill= None, border='black')
        


    def handleDrag(self, mouseX, mouseY):
        # 计算相对于滑块左上角的归一化坐标
        normalized_x = (mouseX - self.x) / self.width
        # y轴需要反转，并且使用相对于滑块左上角的坐标
        normalized_y = 1 - (mouseY - self.y) / self.height
        
        # 将归一化坐标转换为值域范围内的值
        newX = self.min_val + normalized_x * (self.max_val - self.min_val)
        newY = self.min_val + normalized_y * (self.max_val - self.min_val)
        
        # 确保值在有效范围内
        newX = max(self.min_val, min(self.max_val, newX))
        newY = max(self.min_val, min(self.max_val, newY))
        
        self.updateValue(newX, newY)



class PinnedSlider2D(Slider2D):
    def __init__(self, original_slider, app):
        super().__init__(app, 
                        name=original_slider.name,
                        min_val=original_slider.min_val,
                        max_val=original_slider.max_val)
        self.original_slider = original_slider
        self.outputNodes[0].value = original_slider.getValues()[0]
        self.outputNodes[1].value = original_slider.getValues()[1]
        self.current_precision_index = original_slider.current_precision_index
        
    def syncWithOriginal(self):
        """与原始滑块同步所有必要属性"""
        self.min_val = self.original_slider.min_val
        self.max_val = self.original_slider.max_val
        self.current_precision_index = self.original_slider.current_precision_index
        
        # 确保当前值在新范围内
        x_val, y_val = self.getValues()
        new_x = max(self.min_val, min(self.max_val, x_val))
        new_y = max(self.min_val, min(self.max_val, y_val))
        if x_val != new_x or y_val != new_y:
            self.updateValue(new_x, new_y)

    def updateValue(self, x_val, y_val):
        precision = self.precision_options[self.current_precision_index]
        processed_x = processValueWithPrecision(x_val, precision)
        processed_y = processValueWithPrecision(y_val, precision)
        
        # 更新自身和原始滑块的值
        self.outputNodes[0].value = processed_x
        self.outputNodes[1].value = processed_y
        self.original_slider.outputNodes[0].value = processed_x
        self.original_slider.outputNodes[1].value = processed_y
        
        # 更新原始滑块的字段显示
        self.original_slider.fields.update({
            'x': str(processed_x),
            'y': str(processed_y)
        })
        
        # 更新原始滑块的连接
        for connection in self.original_slider.outputNodes[0].connections:
            connection.end_node.receiveValue(processed_x)
        for connection in self.original_slider.outputNodes[1].connections:
            connection.end_node.receiveValue(processed_y)

    def hitTestHandle(self, mouseX, mouseY, x, y):
        x_val, y_val = self.getValues()
        handleX = x + ((x_val - self.min_val) / 
                    (self.max_val - self.min_val)) * self.width
        handleY = y + (1-(y_val - self.min_val) / 
                    (self.max_val - self.min_val)) * self.height
        
        # 计算鼠标到手柄中心的距离
        distance = ((mouseX - handleX)**2 + (mouseY - handleY)**2)**0.5
        
        # 使用圆形碰撞检测，半径为手柄大小的一半
        return distance <= self.handleSize/2

    def drawTwinUI(self, x, y):
        # 绘制背景和边框
        drawRect(x, y, self.width, self.height,
                fill='white', border='black')
        
        # 绘制密集网格线
        for i in range(1, 10):
            lineX = x + (i/10) * self.width
            lineY = y + (i/10) * self.height
            drawLine(lineX, y, lineX, y + self.height,
                    fill='lightGray', lineWidth=0.5)
            drawLine(x, lineY, x + self.width, lineY,
                    fill='lightGray', lineWidth=0.5)
        
        # 绘制手柄和十字线
        x_val, y_val = self.getValues()
        handleX = x + ((x_val - self.min_val) / 
                   (self.max_val - self.min_val)) * self.width
        handleY = y + (1-(y_val - self.min_val) / 
               (self.max_val - self.min_val)) * self.height
        
        # 绘制手柄位置的十字线
        drawLine(handleX, y, handleX, y + self.height,
                fill='black', lineWidth=1, opacity=30)
        drawLine(x, handleY, x + self.width, handleY,
                fill='black', lineWidth=1, opacity=30)
        
        drawCircle(handleX, handleY, self.handleSize/2,
                fill='white', border='black')
        
        #label
        drawLabel(f'({x_val}, {y_val})', handleX, y - 10)
        
        # 绘制昵称
        if self.original_slider.nickname:
            drawLabel(f'[ {self.original_slider.nickname} ]',
                    x + self.width/2, y + self.height + 12,
                    size=12)