from cmu_graphics import *

class Connections:
    def __init__(self, app, start_node, end_node):
        self.start_node = start_node
        self.end_node = end_node
        self.isValid = self.validateConnection(app)
    
    def validateConnection(self, app):
        start_value, end_value = self.start_node.value, self.end_node.value
        start_compo, end_compo = self.start_node.component, self.end_node.component
        
        if self.end_node.component.name == 'Create\nPanel\n[/]':
            return True

        if isinstance(end_value, list):
            # 当输入端 不是单值 是列表

            # 点类型检查
            if end_value[0][0] == 'point':
                point_validation = (
                    isinstance(start_value, list) and 
                    len(start_value) > 0 and 
                    isinstance(start_value[0], list) and 
                    start_value[0][0] == 'point'
                )
                if not point_validation:
                    app.message = ';-( Invalid feed!'
                    app.hintMessage = '[plz feed in point(s); double click the connection to unwire]'
                    return False
            # 向量类型检查
            if end_value[0][0] == 'vector':
                vector_validation = (
                    isinstance(start_value, list) and 
                    len(start_value) > 0 and 
                    isinstance(start_value[0], list) and 
                    start_value[0][0] == 'vector'
                )
                if not vector_validation:
                    app.message = ';-( Invalid feed!'
                    app.hintMessage = '[plz feed in vector(s); double click the connection to unwire]'
                    return False

            # 圆形类型检查,这里需要修改，因为move里面谁都能进
            if end_value[0][0] == 'cir':
                shape_validation = (
                    isinstance(start_value, list) and 
                    isinstance(start_value[0], list) and 
                    start_compo.isGeo
                )
                if not shape_validation:
                    app.message = ';-( Invalid feed!'
                    app.hintMessage = '[plz feed in numeric values; double click the connection to unwire]'
                    return False

        # 数值类型检查（单值或列表）
        elif isinstance(end_value, (int, float)):
            value_validation = (
                isinstance(start_value, (int, float)) or 
                (isinstance(start_value, list) and 
                isinstance((start_value[0]), (int, float)))
            )
            if not value_validation:
                app.message = ';-( Invalid feed!'
                app.messageColor = rgb(226, 163, 136)
                app.hintMessage = '[requires numeric input; double click the connection to unwire]'
                return False
        ###现在如果把东西输入panel会报错
        

        print('pass the type checssk!')
        return True

    def draw(self):
        lightPink = rgb(226, 163, 136)
        drawLine(
            self.start_node.x, self.start_node.y,
            self.end_node.x, self.end_node.y,
            lineWidth=2,
            fill='grey' if self.isValid else lightPink,
        )
    
    def hitTest(self, mouseX, mouseY, threshold=5):
        # Line segment hit testing
        x1, y1 = self.start_node.x, self.start_node.y
        x2, y2 = self.end_node.x, self.end_node.y
        
        # Calculate distance from point to line segment
        length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        if length == 0:
            return False
            
        t = max(0, min(1, ((mouseX - x1) * (x2 - x1) + 
                          (mouseY - y1) * (y2 - y1)) / (length ** 2)))
        
        px = x1 + t * (x2 - x1)
        py = y1 + t * (y2 - y1)
        
        distance = ((mouseX - px) ** 2 + (mouseY - py) ** 2) ** 0.5
        return distance <= threshold
    
    def deleteConnection(self, app):
        # 从节点中移除连接
        self.start_node.removeConnection(self)
        self.end_node.removeConnection(self)
        # 从app中移除连接
        if self in app.connections:
            app.connections.remove(self)
        