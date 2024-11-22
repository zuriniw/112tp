from cmu_graphics import *
from Components import Slider, CircleCreator, RectCreator
import time

def onAppStart(app):
    app.width = 1512
    app.height = 982
    app.toolbarHeight = 80
    app.components = []
    app.selectedComponent = None
    app.lastClickTime = time.time()

    app.paddingX, app.paddingY = 8, 12
    app.borderX, app.borderY = 12, 12
    app.textHeight, app.textWidth = 13, 7

    app.centerLabelWidth = 80

def drawPlayground(app):
    # big background
    drawRect(0, 0, app.width, app.height, fill='white')
    # tool bar background
    drawRect(0, 0, app.width, app.toolbarHeight, fill='black')
    # textLabel
    drawLabel('Toolbar', app.width / 2, app.toolbarHeight / 2, bold = True, size=14, fill='white', font='monospace')

def redrawAll(app):
    drawPlayground(app)
    for component in app.components:
        component.drawUI()

def onMouseMove(app, mouseX, mouseY):
    # if is hovering over a node, it highlights
    for component in app.components:
        for node in component.inputNodes + component.outputNodes:
            if node.hitTest(mouseX, mouseY):
                node.isHovering = True
            else:
                node.isHovering = False

def onMousePress(app, mouseX, mouseY):
    currentTime = time.time()
    for component in app.components:
        if component.hitTest(mouseX, mouseY):
            if currentTime - app.lastClickTime < 0.3:  # 双击检测
                app.components.remove(component)
                app.selectedComponent = None
                return
            # 单击处理
            if isinstance(component, Slider):
                if component.hitTestHandle(mouseX, mouseY):
                    component.isDraggingHandle = True
                    app.selectedComponent = component
                else:
                    app.selectedComponent = component
                    component.isDragging = True
            else:
                app.selectedComponent = component
                component.isDragging = True
            app.lastClickTime = currentTime
            break
    else:
        app.lastClickTime = currentTime
def onMouseDrag(app, mouseX, mouseY):
    for component in app.components:
        if isinstance(component, Slider) and component.isDraggingHandle:
            # 更新滑块值
            normalized_x = (mouseX - component.x) / component.width
            component.value = component.min_val + normalized_x * (component.max_val - component.min_val)
            component.value = max(component.min_val, min(component.max_val, component.value))
        elif component.isDragging:
            # 普通拖动
            newX = mouseX - component.width / 2
            newY = mouseY - component.height / 2
            component.x, component.y = keepWithinBounds(app, newX, newY)
            component.updateNodePositions()

def onMouseRelease(app, mouseX, mouseY):
    if app.selectedComponent:
        if isinstance(app.selectedComponent, Slider):
            app.selectedComponent.isDraggingHandle = False
        app.selectedComponent.isDragging = False
        app.selectedComponent = None

def keepWithinBounds(app, x, y):
    if x < 4:
        x = 4
    elif x + app.selectedComponent.width > app.width - 4:
        x = app.width - app.selectedComponent.width - 4
    if y < app.toolbarHeight + 2:
        y = app.toolbarHeight + 2
    elif y + app.selectedComponent.height > app.height - 4:
        y = app.height = app.selectedComponent.height - 4
    return x, y


def onKeyPress(app, key):
    if key == 's':
        newSlider = Slider(app)
        app.components.append(newSlider)
    elif key == 'c':
        newCircleCreator = CircleCreator(app)
        newCircleCreator.updateNodePositions()
        app.components.append(newCircleCreator)     
    elif key == 'r':
        newRectCreator = RectCreator(app)
        newRectCreator.updateNodePositions()
        app.components.append(newRectCreator)
        
def main():
    runApp()

main()
