from cmu_graphics import *
from Components import Slider, CircleCreator

def onAppStart(app):
    app.components = []
    app.selectedComponent = None

def onKeyPress(app, key):
    if key == 's':
        # Create a slider
        newSlider = Slider(app.nodeZoneWidth / 2, 50, 100, 20)
        app.components.append(newSlider)
    elif key == 'c':
        # Create a circle creator
        newCircleCreator = CircleCreator(app.nodeZoneWidth / 2, 150, 30)
        app.components.append(newCircleCreator)

def onMousePress(app, mouseX, mouseY):
    # Check for component selection in the node zone
    for component in app.components:
        if component.hitTest(mouseX, mouseY):
            app.selectedComponent = component
            component.isDragging = True
            break

def onMouseDrag(app, mouseX, mouseY):
    if app.selectedComponent and app.selectedComponent.isDragging:
        app.selectedComponent.x = mouseX - app.selectedComponent.width / 2
        app.selectedComponent.y = mouseY - app.selectedComponent.height / 2

def onMouseRelease(app, mouseX, mouseY):
    if app.selectedComponent:
        app.selectedComponent.isDragging = False
        app.selectedComponent = None

def redrawAll(app):
    for component in app.components:
        component.draw()

runApp()
