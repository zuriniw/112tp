from cmu_graphics import *
from Components import TypicleComponent

class CircleCreator(TypicleComponent):
    def __init__(self, app):
        inputs = ['point', 'radius']
        outputs = ['circle']
        name = 'Draw\nCirc\nO'
        self.isGeo = True
        self.isDisplay = True
        super().__init__(app, inputs, outputs, name)
        
        self.inputDefaultValue = {
            'point': [['point', (app.x0, app.y0)]],
            'radius': 40
        }
        
        for node in self.inputNodes:
            node.value = self.inputDefaultValue[node.name]
            
        self.outputNodes[0].value = [['cir', (app.x0, app.y0), 40]]
        self.hasAllInputs = True
        
    def calculate(self):
        point_val = self.inputNodes[0].value
        radius_val = self.inputNodes[1].value

        # 使用helper function对齐列表
        point_val, radius_val = align_lists(point_val, radius_val, 
                                            default_value=['point', (self.app.x0, self.app.y0)])

        circles = []
        for point, radius in zip(point_val, radius_val):
            if point[0] == 'point':
                circles.append(['cir', point[1], abs(radius)])

        return circles
        
    def draw(self):
        if self.hasAllInputs:
            circles = self.calculate()
            if not circles:
                return
            for circle in circles:
                    x, y = circle[1]
                    radius = circle[2]
                    if int(radius) != 0:
                        drawCircle(x, y, radius,
                                 fill=None,
                                 border='blue',
                                 visible=self.isDisplay)
                    
                        
class RectCreator(TypicleComponent):
    def __init__(self, app):
        inputs = ['point', 'width', 'height']
        outputs = ['rect']
        name = 'Draw\nRect\nO'
        
        self.isGeo = True
        self.isDisplay = True
        
        super().__init__(app, inputs, outputs, name)
        
        self.inputDefaultValue = {
            'point': [['point', (app.x0, app.y0)]],
            'width': 40,
            'height': 40
        }
        
        for node in self.inputNodes:
            node.value = self.inputDefaultValue[node.name]
        
        self.outputNodes[0].value = [['rect', (app.x0, app.y0), 40, 40]]
        
        self.hasAllInputs = True

    def calculate(self):
        point_val = self.inputNodes[0].value
        width_val = abs(self.inputNodes[1].value) if self.inputNodes[1].value is not None else None
        height_val = abs(self.inputNodes[2].value) if self.inputNodes[2].value is not None else None
        
        rects = []
        
        if isinstance(point_val[0], list) and point_val[0][0] == 'point':
            for point in point_val:
                rects.append(['rect', point[1], width_val, height_val])
        else:
            if point_val[0] == 'point':
                rects.append(['rect', point_val[1], width_val, height_val])
        
        return rects

    def draw(self):
        if self.hasAllInputs:
            rects = self.calculate()
            
            if not rects:
                return
            
            for rect in rects:
                x, y = rect[1]
                width = rect[2]
                height = rect[3]
                
                if int(width) != 0 and int(height) != 0:
                    drawRect(x, y, width, height,
                             fill=None, 
                             border='blue', 
                             visible=self.isDisplay)

def align_lists(list1, list2, default_value=None):
    """
    使两个列表长度一致，并返回调整后的列表
    
    Args:
        list1: 第一个列表
        list2: 第二个列表
        default_value: 用于填充的默认值
    
    Returns:
        调整后的两个列表
    """
    # 确保输入是列表
    list1 = [list1] if not isinstance(list1, list) else list1
    list2 = [list2] if not isinstance(list2, list) else list2
    
    # 如果list1比list2短，延长list1
    if len(list1) < len(list2):
        last_item = list1[-1] if list1 else default_value
        list1.extend([last_item] * (len(list2) - len(list1)))
    
    # 如果list2比list1短，延长list2  
    elif len(list2) < len(list1):
        last_item = list2[-1] if list2 else default_value
        list2.extend([last_item] * (len(list1) - len(list2)))
    
    return list1, list2