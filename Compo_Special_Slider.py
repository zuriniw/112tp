'''
[special components] that have unique interaction and GUI, 
not belong to [typical components]
include:
    - Slider
    - 
'''

from Components import Component
from cmu_graphics import *
from Node import *

class Slider(Component):
    def __init__(self, app, name='Slider\n<--->', min_val=-200, max_val=200):
        inputs = []
        outputs = ['value']
        super().__init__(app)
        
        self.name = name
        self.outputs = outputs
        self.outputNodes = [Node(output, self, True) for output in outputs]
        
        self.min_val = min_val
        self.max_val = max_val
        # 只在输出节点中存储值
        self.outputNodes[0].value = (min_val + max_val) / 2
        
        self.width = 120
        self.height = 32
        self.handleWidth = 12
        self.isDraggingHandle = False
        self.outputHeight = app.textHeight
        self.updateNodePositions()

        self.nickname = ''
        self.isPinned = False

        # Add right-click event binding
        self.rightClickX = 0
        self.rightClickY = 0
        
        self.precision_options = [10, 1, 0.1]  # 整数、一位小数、两位小数的精度值
        self.current_precision_index = 1  # 默认使用精度1

        self.fields = {
            'nickname': self.nickname,
            'value': str(self.getValue()),
            'min': str(self.min_val),
            'max': str(self.max_val),
            'precision': f'{self.precision_options[self.current_precision_index]} decimal',
            'pin':self.isPinned
        }
        

    def updateFields(self):
        self.fields = {
            'nickname': self.nickname,
            'value': str(self.getValue()),
            'min': str(self.min_val),
            'max': str(self.max_val),
            'precision': f'{self.precision_options[self.current_precision_index]} decimal',
            'pin': self.isPinned
        }
        
        # 同步更新pinned slider的属性
        if self.isPinned:
            for pinned_slider in app.pinnedSliders:
                if pinned_slider.original_slider == self:
                    pinned_slider.min_val = self.min_val
                    pinned_slider.max_val = self.max_val
                    pinned_slider.current_precision_index = self.current_precision_index
                    # 确保值在新范围内
                    current_value = pinned_slider.getValue()
                    new_value = max(self.min_val, min(self.max_val, current_value))
                    pinned_slider.updateValue(new_value)
        
        

    def getValue(self):
        precision = self.precision_options[self.current_precision_index]
        return processValueWithPrecision(self.outputNodes[0].value, precision)
    
    def updateValue(self, value):
        precision = self.precision_options[self.current_precision_index]
        processed_value = processValueWithPrecision(value, precision)
        
        self.outputNodes[0].value = processed_value
        
        # 通过输出节点传递处理后的值
        for connection in self.outputNodes[0].connections:
            connection.end_node.receiveValue(processed_value)
            
        # 同步更新PinnedSlider
        if self.isPinned:
            for pinned_slider in app.pinnedSliders:
                if pinned_slider.original_slider == self:
                    pinned_slider.outputNodes[0].value = processed_value

    def hitTestHandle(self, mouseX, mouseY):
        # 计算手柄的中心位置，考虑手柄宽度
        handleX = self.x + ((self.getValue() - self.min_val) / (self.max_val - self.min_val)) * (self.width - self.handleWidth)
        # 检查鼠标是否在手柄的范围内
        return (handleX <= mouseX <= handleX + self.handleWidth) and (self.y <= mouseY <= self.y + self.height)

    def drawUI(self):
        # Draw node
        for node in self.outputNodes:
            node.drawNode()
        # Draw background
        drawRect(self.x, self.y, self.width, self.height, fill='white' if not self.isSelected else 'lightGrey', border='black')
        # Draw handle
        handleX = self.x + ((self.getValue() - self.min_val) / (self.max_val - self.min_val)) * (self.width-self.handleWidth)
        drawRect(handleX, self.y, self.handleWidth, self.height, fill='black')
        # Draw value label
        drawLabel(f'{self.getValue()}', handleX, self.y - 10)
        # Draw Nickname
        if self.nickname:
            appendix = ' ^ ' if self.isPinned else ''
            drawLabel(f'[ {self.nickname} ]'+ appendix, self.x + self.width/2, self.y+self.height+8, size = 12)



class PinnedSlider(Slider):
    def __init__(self, original_slider, app):
        super().__init__(app,
            name=original_slider.name,
            min_val=original_slider.min_val,
            max_val=original_slider.max_val)
        
        self.outputs = ['value']
        self.outputNodes = [Node('value', self, True)]
        self.original_slider = original_slider
        
        # 同步所有必要的属性
        self.outputNodes[0].value = original_slider.getValue()
        self.min_val = original_slider.min_val
        self.max_val = original_slider.max_val
        self.current_precision_index = original_slider.current_precision_index
    
    def updateFields(self):
        self.min_val = self.original_slider.min_val
        self.max_val = self.original_slider.max_val
        self.current_precision_index = self.original_slider.current_precision_index
    
    def drawTwinUI(self, x, y):
        # 绘制主背景（透明）
        drawRect(x, y, self.width, self.height, 
                fill=None, border=None)
        
        # 绘制中间轨道
        trackY = y + self.height/2
        drawLine(x, trackY, x + self.width, trackY,
                fill='black', lineWidth=2)
        
        # 绘制刻度
        numTicks = 10  # 刻度数量
        tickHeight = 5  # 刻度高度
        for i in range(numTicks + 1):
            tickX = x + (i / numTicks) * self.width
            # 绘制刻度线
            drawLine(tickX, trackY - tickHeight/2, 
                    tickX, trackY + tickHeight/2,
                    fill='black', lineWidth=1)
        
        # 计算滑块位置
        handleX = x + ((self.getValue() - self.min_val) / 
                    (self.max_val - self.min_val)) * self.width
        
        # 绘制滑块（圆形）
        handleRadius = 7
        drawCircle(handleX, trackY, handleRadius,
                fill='white', border='black')
        
        # 绘制当前值
        drawLabel(f'{self.getValue()}', handleX, y - 5,
                size=12)
        
        # 绘制昵称（如果存在）
        if self.original_slider.nickname:
            drawLabel(f'[ {self.original_slider.nickname} ]',
                    x + self.width/2, y + self.height + 12,
                    size=12)
        # 
    def updateValue(self, value):
        # 先处理精度
        precision = self.precision_options[self.current_precision_index]
        processed_value = processValueWithPrecision(value, precision)
        
        # 更新自身值
        self.outputNodes[0].value = processed_value
        
        # 直接更新原始slider的值，而不是调用其updateValue方法
        self.original_slider.outputNodes[0].value = processed_value
        
        # 更新原始slider的连接
        for connection in self.original_slider.outputNodes[0].connections:
            connection.end_node.receiveValue(processed_value)

    def hitTestHandle(self, mouseX, mouseY, x, y):
       # 计算滑块中心位置
        trackY = y + self.height/2
        handleX = x + ((self.getValue() - self.min_val) / 
                    (self.max_val - self.min_val)) * self.width
        
        # 计算鼠标到滑块中心的距离
        handleRadius = 7  # 与绘制时相同的半径
        distance = ((mouseX - handleX)**2 + (mouseY - trackY)**2)**0.5
        
        # 如果距离小于滑块半径，则判定为点击到滑块
        return distance <= handleRadius

def processValueWithPrecision(value, precision_value):
    """处理数值精度
    precision_value: 10 代表整数(10的倍数), 1 代表整数, 0.1 代表一位小数"""
    # 避免浮点数精度问题，使用字符串格式化
    if precision_value == 0.1:
        return float(f"{value:.1f}")
    return int(value / precision_value + 0.5) * precision_value