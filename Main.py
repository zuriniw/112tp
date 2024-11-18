from cmu_graphics import *
from Components.CircleCreator import CircleCreator
from Components.Slider import Slider
import os

def onAppStart(app):
    app.width = 1512
    app.height = 982
    app.canvasWidth = app.width * 0.6
    app.nodeZoneWidth = app.width * 0.4
    app.toolbarHeight = 50
    app.isDragging = False
    app.dragStartX = None
    app.splitterWidth = 10
    app.splitterColor = 'darkblue'
    app.components = [
        CircleCreator(app.nodeZoneWidth / 2, 100, 30),
        Slider(app.nodeZoneWidth / 2 - 50, 200, 100, 20)
    ]

def drawCanvas(app):
    drawRect(0, 0, app.canvasWidth, app.height, fill='white')
    drawLabel('Canvas Area', app.canvasWidth / 2, app.height / 2, size=20, bold=True)

def drawNodePlayground(app):
    drawRect(app.canvasWidth + app.splitterWidth, 0, app.nodeZoneWidth, app.height, fill='grey')
    drawRect(app.canvasWidth + app.splitterWidth, 0, app.nodeZoneWidth, app.toolbarHeight, fill='darkgrey')
    drawLabel('Toolbar', app.canvasWidth + app.splitterWidth + app.nodeZoneWidth / 2, app.toolbarHeight / 2, size=14, bold=True, fill='white')
    drawLabel('Node Manipulation Zone', app.canvasWidth + app.splitterWidth + app.nodeZoneWidth / 2, app.height / 2, size=20, bold=True)

def drawSplitter(app):
    # 根据是否拖拽改变手柄颜色
    splitterColor = 'lightblue' if app.isDragging else app.splitterColor
    drawRect(app.canvasWidth, 0, app.splitterWidth, app.height, fill=splitterColor)

def redrawAll(app):
    drawCanvas(app)
    drawSplitter(app)
    drawNodePlayground(app)

def onMousePress(app, mouseX, mouseY):
    if app.canvasWidth <= mouseX <= app.canvasWidth + app.splitterWidth:
        app.isDragging = True
        app.dragStartX = mouseX
        app.splitterColor = 'lightblue'
    else:
        for component in app.components:
            if component.x - 50 <= mouseX <= component.x + 50 and component.y - 50 <= mouseY <= component.y + 50:
                component.isDragging = True
                break

def onMouseDrag(app, mouseX, mouseY):
    if app.isDragging:
        adjustSplitter(app, mouseX)
    else:
        for component in app.components:
            if component.isDragging:
                component.x = mouseX - app.canvasWidth
                component.y = mouseY
                break

def onMouseRelease(app, mouseX, mouseY):
    app.isDragging = False
    app.splitterColor = 'darkblue'
    for component in app.components:
        component.isDragging = False

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
