from cmu_graphics import *

class Draggable:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.isDragging = False

    def hitTest(self, mouseX, mouseY):
        return (self.x <= mouseX <= self.x + self.width) and (self.y <= mouseY <= self.y + self.height)

class Slider(Draggable):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.value = 50  # Initial slider value

    def draw(self):
        drawRect(self.x, self.y, self.width, self.height, fill='lightgrey')
        handleX = self.x + (self.value / 100) * self.width
        drawRect(handleX - 5, self.y, 10, self.height, fill='darkgrey')

class CircleCreator(Draggable):
    def __init__(self, x, y, radius):
        super().__init__(x - radius, y - radius, 2 * radius, 2 * radius)
        self.radius = radius

    def draw(self):
        drawOval(self.x, self.y, self.radius * 2, self.radius * 2, fill='lightblue')
