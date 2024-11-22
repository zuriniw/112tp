from cmu_graphics import *
from Components import Slider, CircleCreator, RectCreator
from Connection import Connections
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

    app.connections = []
    app.draggingNode = None
    app.tempConnection = None

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
    
    # Draw components
    for component in app.components:
        component.drawUI()
    
    # Draw connections
    for connection in app.connections:
        connection.draw()
    
    # Draw temporary connection while dragging
    if app.tempConnection:
        node, mouseX, mouseY = app.tempConnection
        drawLine(node.x, node.y, mouseX, mouseY, 
                lineWidth=2, fill='gray', dashes = (4,2))

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
    
    # 首先检查是否点击到节点
    for component in app.components:
        for node in component.inputNodes + component.outputNodes:
            if node.hitTest(mouseX, mouseY):
                app.draggingNode = node
                return
    
    # 检查连接线
    for connection in app.connections:
        if connection.hitTest(mouseX, mouseY):
            if currentTime - app.lastClickTime < 0.3:  # 双击检测
                app.connections.remove(connection)
                return
            app.lastClickTime = currentTime
            return
    
    # 最后检查组件
    for component in app.components:
        if component.hitTest(mouseX, mouseY):
            if currentTime - app.lastClickTime < 0.3:
                app.components.remove(component)
                app.selectedComponent = None
                return
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

def onMouseDrag(app, mouseX, mouseY):
    if app.draggingNode:
        # 处理节点拖动
        app.tempConnection = (app.draggingNode, mouseX, mouseY)
    elif app.selectedComponent:  # 只处理被选中的组件
        if isinstance(app.selectedComponent, Slider) and app.selectedComponent.isDraggingHandle:
            # 更新滑块值
            normalized_x = (mouseX - app.selectedComponent.x) / app.selectedComponent.width
            app.selectedComponent.value = app.selectedComponent.min_val + normalized_x * (app.selectedComponent.max_val - app.selectedComponent.min_val)
            app.selectedComponent.value = max(app.selectedComponent.min_val, min(app.selectedComponent.max_val, app.selectedComponent.value))
        elif app.selectedComponent.isDragging:
            # 普通拖动
            newX = mouseX - app.selectedComponent.width / 2
            newY = mouseY - app.selectedComponent.height / 2
            app.selectedComponent.x, app.selectedComponent.y = keepWithinBounds(app, newX, newY)
            app.selectedComponent.updateNodePositions()

def onMouseRelease(app, mouseX, mouseY):
    if app.draggingNode:
        start_node = app.draggingNode
        for component in app.components:
            for node in component.inputNodes + component.outputNodes:
                if node.hitTest(mouseX, mouseY) and node != start_node:
                    if start_node.isOutput != node.isOutput:
                        output_node = start_node if start_node.isOutput else node
                        input_node = node if start_node.isOutput else start_node
                        
                        # Create new connection
                        new_connection = Connections(output_node, input_node)
                        
                        # Add connection to nodes
                        output_node.addConnection(new_connection)
                        input_node.addConnection(new_connection)
                        
                        # Add connection to app
                        app.connections.append(new_connection)
        
        app.draggingNode = None
        app.tempConnection = None

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
