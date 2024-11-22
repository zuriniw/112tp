from cmu_graphics import *

class Connections:
    def __init__(self, start_node, end_node):
        self.start_node = start_node
        self.end_node = end_node
    
    def draw(self):
        drawLine(
            self.start_node.x, self.start_node.y,
            self.end_node.x, self.end_node.y,
            lineWidth=2,
            fill='grey',
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