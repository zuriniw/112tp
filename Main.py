from cmu_graphics import *
from Components import Slider, CircleCreator

def onAppStart(app):
    app.width = 1512
    app.height = 982
    app.canvasWidth = app.width * 0.4
    app.nodeZoneWidth = app.width * 0.6
    app.toolbarHeight = 50
    app.isDraggingSplitter = False
    app.dragStartX = None
    app.splitterWidth = 10
    app.splitterColor = 'darkblue'
    app.components = []
    app.selectedComponent = None
    app.nodeZoneMidX = app.canvasWidth + app.nodeZoneWidth/2
    app.nodeZoneLeft = app.canvasWidth + app.splitterWidth 
    app.nodeZoneRight = app.width - app.splitterWidth

def drawCanvas(app):
    drawRect(0, 0, app.canvasWidth, app.height, fill='white')
    drawLabel('Canvas Area', app.canvasWidth / 2, app.height / 2, size=20, bold=True)

def drawNodePlayground(app):
    drawRect(app.canvasWidth + app.splitterWidth, 0, app.nodeZoneWidth, app.height, fill='grey')
    drawRect(app.canvasWidth + app.splitterWidth, 0, app.nodeZoneWidth, app.toolbarHeight, fill='darkgrey')
    drawLabel('Toolbar', app.canvasWidth + app.splitterWidth + app.nodeZoneWidth / 2, app.toolbarHeight / 2, size=14, bold=True, fill='white')
    drawLabel('Node Manipulation Zone', app.canvasWidth + app.splitterWidth + app.nodeZoneWidth / 2, app.height / 2, size=20, bold=True)

def drawSplitter(app):
    splitterColor = 'lightblue' if app.isDraggingSplitter else app.splitterColor
    drawRect(app.canvasWidth, 0, app.splitterWidth, app.height, fill=splitterColor)

def redrawAll(app):
    drawCanvas(app)
    drawSplitter(app)
    drawNodePlayground(app)
    for component in app.components:
        component.drawUI()

def onMousePress(app, mouseX, mouseY):
    if app.canvasWidth <= mouseX <= app.canvasWidth + app.splitterWidth:
        app.isDraggingSplitter = True
        app.dragStartX = mouseX
        app.splitterColor = 'lightblue'
    else:
        for component in app.components:
            if component.hitTest(mouseX, mouseY):
                # print('hit')
                app.selectedComponent = component
                component.isDragging = True
                break
        
def onMouseDrag(app, mouseX, mouseY):
    if app.isDraggingSplitter:
        adjustSplitter(app, mouseX)
    elif app.selectedComponent and app.selectedComponent.isDragging:
        newX = mouseX - app.selectedComponent.width / 2
        newY = mouseY - app.selectedComponent.height / 2
        app.selectedComponent.x, app.selectedComponent.y = keepWithinBounds(app, newX, newY)

# keep components inside of the bound of node zone
def keepWithinBounds(app, x, y):
    # Adjust x to keep within horizontal bounds
    if x < app.nodeZoneLeft:
        x = app.nodeZoneLeft
    elif x + app.selectedComponent.width > app.nodeZoneRight:
        x = app.nodeZoneRight - app.selectedComponent.width
    # Adjust y to keep within vertical bounds (if necessary)
    if y < app.top:
        y = app.top
    elif y + app.selectedComponent.height > app.bottom:
        y = app.bottom - app.selectedComponent.height
    return x, y


def onMouseRelease(app, mouseX, mouseY):
    if app.isDraggingSplitter:
        app.isDraggingSplitter = False
        app.splitterColor = 'darkblue'
    if app.selectedComponent:
        app.selectedComponent.isDragging = False
        app.selectedComponent = None

def onKeyPress(app, key):
    if key == 's':
        newSlider = Slider(app)   
        app.components.append(newSlider)
    elif key == 'c':
        newCircleCreator = CircleCreator(app)
        app.components.append(newCircleCreator)

def adjustSplitter(app, mouseX):
    deltaX = mouseX - app.dragStartX
    newCanvasWidth = app.canvasWidth + deltaX
    minimalWidth = app.width / 3
    if minimalWidth <= newCanvasWidth <= app.width - minimalWidth:
        app.canvasWidth = newCanvasWidth
        app.nodeZoneWidth = app.width - app.canvasWidth - app.splitterWidth
    app.dragStartX = mouseX

def main():
    runApp()

main()
