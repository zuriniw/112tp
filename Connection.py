from cmu_graphics import *

class Connections:
    def __init__(self, app, start_node, end_node):
        self.start_node = start_node
        self.end_node = end_node
        self.isValid = self.validateConnection(app)
    
    def validateConnection(self, app):
        start_value, end_value = self.start_node.value, self.end_node.value
        # Enhanced type validation
        if start_value is None:
            return False
        
        # Specific checks for point and radius
        if isinstance(end_value, list) and end_value[0][0] == 'point':
            # Ensure start_value is compatible point type
            if not (isinstance(start_value, list) and 
                    isinstance(start_value[0], list) and 
                    start_value[0][0] == 'point'):
                app.message = f'Wrong feed!'
                app.hintMessage = f'[should feed in point(s)]'
                return False
        
        return True

    def draw(self):
        drawLine(
            self.start_node.x, self.start_node.y,
            self.end_node.x, self.end_node.y,
            lineWidth=2,
            fill='grey' if self.isValid else 'orange',
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
        