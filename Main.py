from cmu_graphics import *
from Components import Slider, CircleCreator, RectCreator
import time

def onAppStart(app):
    app.width = 1512
    app.height = 982
    app.toolbarHeight = 80
    app.components = []
    app.selectedComponent = None

    app.paddingX, app.paddingY = 8, 12
    app.borderX, app.borderY = 12, 12
    app.textHeight, app.textWidth = 11, 7

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
            if currentTime - app.lastClickTime < 0.3:  # If second click is within 300 ms, consider it a double-click
                app.components.remove(component)  # Remove the component
                app.selectedComponent = None
                return  # Exit after deleting the component to avoid errors
            else:
                app.selectedComponent = component
                component.isDragging = True
                app.lastClickTime = currentTime
                break
    else:
        app.lastClickTime = currentTime  # Reset last click time if no component was clicked

def onMouseDrag(app, mouseX, mouseY):
    if app.selectedComponent and app.selectedComponent.isDragging:
        newX = mouseX - app.selectedComponent.width / 2
        newY = mouseY - app.selectedComponent.height / 2
        app.selectedComponent.x, app.selectedComponent.y = keepWithinBounds(app, newX, newY)
        app.selectedComponent.updateNodePositions()

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

def onMouseRelease(app, mouseX, mouseY):
    if app.selectedComponent:
        app.selectedComponent.isDragging = False
        app.selectedComponent = None

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
