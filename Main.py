from cmu_graphics import *
from Components import *
from Compo_Geo import *
from Compo_Math import *
from Compo_Vector import *
from Connection import Connections
from Toggle import Toggle
from ToolbarButton import ToolbarButton
from ToolbarTab import ToolbarTab

import time

def onAppStart(app):

    app.width = 1512
    app.height = 982

    app.mouseX = app.width/2
    app.mouseY = app.height/2

    app.toolbarHeight = 110
    app.components = []
    app.selectedCompo = []
    app.currDraggingComponent = None
    app.lastClickTime = time.time()

    app.paddingX, app.paddingY = 8, 12
    app.borderX, app.borderY = 12, 12
    app.textHeight, app.textWidth = 13, 7

    app.connections = []
    app.draggingNode = None
    app.tempConnection = None

    app.isCompDisplay = True
    app.isAxisDisplay = True
    app.isGridDisplay = True
    app.isDotDisplay = False
    app.isGuidbookDisplay = False

    app.toggleStates = {
        'Comp Display': app.isCompDisplay,
        'Axis Display': app.isAxisDisplay,
        'Grid Display': app.isGridDisplay,
        'Dot Display':app.isDotDisplay,
        'Guidbook Display':app.isGuidbookDisplay
    }

    app.toggleWidth, app.toggleHeight = 80, 40      # toggle buttom
    app.togglePanelWidth = 120
    app.togglePanelStartX = app.width - app.togglePanelWidth
    app.togglePanelStartY = app.toolbarHeight + app.paddingY

    toggleStartX = app.togglePanelStartX + app.togglePanelWidth/2 - app.toggleWidth/2
    firstToggleStartY = app.togglePanelStartY + app.borderY * 3
    toggleNames = list(app.toggleStates.keys())
    app.toggles = [Toggle(app, toggleStartX, firstToggleStartY + i*(app.textHeight+app.paddingY*3+app.toggleHeight), toggleNames[i], app.toggleStates[toggleNames[i]]) for i in range(len(toggleNames))]

    app.centerLabelWidth = 80

    #grid
    app.x0 = app.togglePanelStartX / 2
    app.y0 = app.height/2

    # Toolbar organization
    app.isDraggingNewComponent = False
    app.draggedComponentType = None

    app.componentTypes = {
        'Geometry': [CircleCreator, RectCreator],
        'Math': [Slider, Reverse, Add, Subtract, Multiply, Divide],
        'Manipulation': [],
        'Analyze': [],
        'Vector':[Point]
    }
    app.activeCategory = 'Geometry'  # Default active category
    loadToolbar(app)
    # Toolbar tab
    app.tabs = []
    tabX = 0
    for category in list(app.componentTypes.keys()):
        isActive = (category == app.activeCategory)
        tab = ToolbarTab(tabX, 0, category, isActive)
        app.tabs.append(tab)
        tabX += tab.width - 2
    
    # Drag selecting components
    app.isDragSelecting = False    # 是否正在拖拽选择
    app.dragFrameStart = None      # 拖拽起始位置
    app.dragFrameEnd = None        # 拖拽结束位置

    # Drag move components
    app.dragGroupOldMouseX,app.dragGroupOldMouseX = None, None 

def loadToolbar(app): 
    currbuttomCompoList = app.componentTypes[app.activeCategory]
    app.currButtomList = [ToolbarButton(app, app.borderX + currbuttomCompoList.index(buttomCompo) * (60 + app.paddingX), 40, buttomCompo) for buttomCompo in currbuttomCompoList]
    

def drawToolbar(app):
    tabHeight = 30
    drawLine(0, app.toolbarHeight, app.width, app.toolbarHeight)
    drawLine(0, tabHeight-1, app.width, tabHeight-1)
    # 绘制标签
    for tab in app.tabs:
        tab.drawUI()
    # 绘制当前标签页里的component按钮
    for button in app.currButtomList:
        button.drawUI()

def drawAxis(app):
    if app.isAxisDisplay:
        # Draw axis
        drawLine(app.borderX, app.y0, app.togglePanelStartX-app.borderX, app.y0, arrowStart=True, arrowEnd=True, opacity = 10)
        drawLine(app.x0, app.toolbarHeight + app.borderY, app.x0, app.height - app.borderY, arrowStart=True, arrowEnd=True, opacity = 10)
        


def drawGrid(app):
    if app.isGridDisplay:
        # Define grid parameters
        gridSize = 30
        
        # Calculate grid counts from origin to edges
        rightGrids = int((app.togglePanelStartX - app.x0) // gridSize)
        leftGrids = int((app.x0 - app.borderX) // gridSize)
        upGrids = int((app.y0 - app.toolbarHeight) // gridSize)
        downGrids = int((app.height - app.y0) // gridSize)
        
        # Draw vertical lines
        for i in range(-leftGrids, rightGrids + 1):
            x = app.x0 + i * gridSize
            drawLine(x, app.toolbarHeight, x, app.height,
                    fill='lightGrey', lineWidth=0.5)
        
        # Draw horizontal lines
        for j in range(-upGrids, downGrids + 1):
            y = app.y0 + j * gridSize
            drawLine(app.borderX, y, app.togglePanelStartX, y,
                    fill='lightGrey', lineWidth=0.5)
            
def drawDot(app):
    if app.isDotDisplay:
        gridSize = 30
        
        # Calculate grid counts from origin to edges
        rightGrids = int((app.togglePanelStartX - app.x0) // gridSize)
        leftGrids = int((app.x0 - app.borderX) // gridSize)
        upGrids = int((app.y0 - app.toolbarHeight) // gridSize)
        downGrids = int((app.height - app.y0) // gridSize)
        
        # Draw dots at grid intersections
        for i in range(-leftGrids, rightGrids + 1):
            for j in range(-upGrids, downGrids + 1):
                x = app.x0 + i * gridSize
                y = app.y0 + j * gridSize
                drawCircle(x, y, 1, fill='darkgrey')


def drawPlayground(app):
    # big background
    drawRect(0, 0, app.width, app.height, fill='white')

def drawDraggingFrame(app):
    if app.isDragSelecting and app.dragFrameStart != app.dragFrameEnd:
        x1, y1 = app.dragFrameStart
        x2, y2 = app.dragFrameEnd
        # 绘制半透明的选择框
        if x2 != x1 and y2 != y1:
            drawRect(min(x1, x2), min(y1, y2),
                    abs(x2 - x1), abs(y2 - y1),
                    fill='lightgrey', border = 'red', opacity=20, dashes = True)

def redrawAll(app):
    drawPlayground(app)
    drawToolbar(app)
    drawGrid(app)
    drawAxis(app)
    drawDot(app)
    
    if app.isCompDisplay:
        # Draw existing components
        for component in app.components:
            component.drawUI()
            
        # Draw connections
        for connection in app.connections:
            connection.draw()
            
        # Draw temporary connection
        if app.tempConnection:
            node, mouseX, mouseY = app.tempConnection
            drawLine(node.x, node.y, mouseX, mouseY,
                    lineWidth=2, fill='black', dashes=(4,3))
        
        # Draw component being dragged - Fix preview movement
        if app.isDraggingNewComponent and app.draggedComponentType:
            preview = app.draggedComponentType(app)
            # Update preview position based on mouse
            preview.x = app.mouseX - preview.width/2
            preview.y = app.mouseY - preview.height/2
            # Update node positions before drawing
            preview.updateNodePositions()
            # Draw the preview
            preview.drawUI()

    drawRect(app.togglePanelStartX, app.togglePanelStartY, app.togglePanelWidth, app.height - app.toolbarHeight - 2 * app.paddingY, border = 'black', fill = 'white')
    for toggle in app.toggles:
        toggle.drawUI()
    
    for component in app.components:
        if isinstance(component, TypicleComponent) and component.isGeo:
            component.draw()
    
    if app.isDragSelecting:
        drawDraggingFrame(app)



def onMouseMove(app, mouseX, mouseY):
    # Update mouse position for preview
    app.mouseX = mouseX
    app.mouseY = mouseY
    
    # 处理节点悬停
    for component in app.components:
        for node in component.inputNodes + component.outputNodes:
            if node.hitTest(mouseX, mouseY):
                node.isHovering = True
            else:
                node.isHovering = False
    
    # 处理按钮悬停
    for button in app.currButtomList:
        button.isHovering = button.hitTest(mouseX, mouseY)
    
    # 更新预览组件位置
    if app.isDraggingNewComponent:
        app.mouseX = mouseX
        app.mouseY = mouseY

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
            if currentTime - app.lastClickTime < 0.3:
                app.connections.remove(connection)
                return
            app.lastClickTime = currentTime
            return
        
    # 检查toolbar button
    for button in app.currButtomList:
        if button.hitTest(mouseX, mouseY):
            app.currDraggingComponent = None
            app.isDraggingNewComponent = True
            app.draggedComponentType = button.component
            return
    
    # 检查toolbar tab
    for tab in app.tabs:
        if tab.hitTest(mouseX, mouseY):
            app.currDraggingComponent = None
            for t in app.tabs:
                t.isActive = (t == tab)
            app.activeCategory = tab.category
            loadToolbar(app)
            return
        
    # 检查toggle
    for toggle in app.toggles:
        if toggle.hitTest(mouseX, mouseY):
            toggle.isOn = not toggle.isOn
            # Generate mapping dynamically by converting toggle name to variable name
            var_name = 'is'+toggle.name.replace(' ', '')
            setattr(app, var_name, toggle.isOn)
            app.toggleStates[toggle.name] = toggle.isOn
            return
        
        
    hitComponent = False
    # 最后检查组件
    for component in app.components:
        if component.hitTest(mouseX, mouseY):
            hitComponent = True
            # 1////双击删除
            if currentTime - app.lastClickTime < 0.3:
                # 删除与该组件相关的所有连接
                connectionsToRemove = []
                for connection in app.connections:
                    if (connection.start_node.component == component or 
                        connection.end_node.component == component):
                        connectionsToRemove.append(connection)
                
                # 从 app.connections 中移除这些连接
                for connection in connectionsToRemove:
                    app.connections.remove(connection)
                
                # 删除组件
                app.components.remove(component)
                app.currDraggingComponent = None
                return
            # 2///拖动手柄
            if isinstance(component, Slider):
                if component.hitTestHandle(mouseX, mouseY):
                    # 点击到滑块手柄
                    component.isDraggingHandle = True
                    app.currDraggingComponent = component
                else:
                    # 点击到滑块其他部分，只设置拖动状态
                    app.currDraggingComponent = component
                    component.isDragging = True
                    component.isDraggingHandle = False
            # 3///点到组件
            else:
                # 拖动单个
                if app.selectedCompo == []:
                    app.currDraggingComponent = component
                    component.isDragging = True
                # 拖动多个
                else:
                    app.dragGroupOldMouseX, app.dragGroupOldMouseY = mouseX, mouseY
                    app.currDraggingComponent = app.selectedCompo
                    for compo in app.selectedCompo:
                        compo.isDragging = True
            app.lastClickTime = currentTime
            break

    if not hitComponent:
        app.currDraggingComponent = None

    if app.currDraggingComponent is None:  # 点击空白处
        # 清空已经选中的compo
        for compo in app.selectedCompo:
            compo.isSelected = False

        app.selectedCompo = []

        # Prepare to drad and select
        app.isDragSelecting = True
        app.dragFrameStart = (mouseX, mouseY)
        app.dragFrameEnd = (mouseX, mouseY)

def onMouseDrag(app, mouseX, mouseY):
    app.mouseX = mouseX
    app.mouseY = mouseY
    
    if app.isDragSelecting:
        app.dragFrameEnd = (mouseX, mouseY)
        
    elif app.draggingNode:  # Handle node dragging for connections
        app.tempConnection = (app.draggingNode, mouseX, mouseY)
        # Check for hovering over input nodes
        for component in app.components:
            for node in component.inputNodes:
                node.isHovering = node.hitTest(mouseX, mouseY)

    elif app.currDraggingComponent:  # Handle dragging of current component
        comp = app.currDraggingComponent
        if not isinstance(comp, list):
            if isinstance(comp, Slider):
                if comp.isDraggingHandle:
                    normalized_x = (mouseX - comp.x) / comp.width
                    newValue = comp.min_val + normalized_x * (comp.max_val - comp.min_val)
                    newValue = max(comp.min_val, min(comp.max_val, newValue))
                    comp.updateValue(newValue)
                elif comp.isDragging:
                    newX, newY = adjustPosition(comp, mouseX, mouseY)
                    comp.x, comp.y = keepWithinBounds(app, newX, newY, comp)
                    comp.updateNodePositions()
            elif comp.isDragging:
                newX, newY = adjustPosition(comp, mouseX, mouseY)
                comp.x, comp.y = keepWithinBounds(app, newX, newY, comp)
                comp.updateNodePositions()
        else:
            dx, dy = mouseX - app.dragGroupOldMouseX, mouseY - app.dragGroupOldMouseY
            for selectedCompo in app.currDraggingComponent:
                newX, newY = selectedCompo.x + dx, selectedCompo.y + dy
                selectedCompo.x, selectedCompo.y = keepWithinBounds(app, newX, newY, selectedCompo)
                selectedCompo.updateNodePositions()
            app.dragGroupOldMouseX, app.dragGroupOldMouseY = mouseX, mouseY

def adjustPosition(comp, mouseX, mouseY):
    newX = mouseX - comp.width / 2
    newY = mouseY - comp.height / 2
    return newX, newY

def keepWithinBounds(app, x, y, com):
    x = max(4, min(x, app.width - com.width - 4))
    y = max(app.toolbarHeight + 2, min(y, app.height - com.height - 4))
    return x, y



def onMouseRelease(app, mouseX, mouseY):
    if app.isDraggingNewComponent and app.draggedComponentType:
        # 确保在有效区域内
        if mouseY > app.toolbarHeight:
            # 创建新组件
            newComponent = app.draggedComponentType(app)
            newComponent.x = mouseX - newComponent.width/2
            newComponent.y = mouseY - newComponent.height/2
            app.components.append(newComponent)
            newComponent.updateNodePositions()
        
        # 重置拖动状态
        app.isDraggingNewComponent = False
        app.draggedComponentType = None
        return
        
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

    if app.isDragSelecting:
        app.isDragSelecting = False
        for compo in app.components:
            if isIntersectRects((compo.x, compo.y), (compo.x + compo.width, compo.y+compo.height), app.dragFrameStart, app.dragFrameEnd):
                app.selectedCompo.append(compo)
                compo.isSelected = True
        app.dragFrameStart = None
        app.dragFrameEnd = None
    
    app.dragGroupOldMouseX, app.dragGroupOldMouseY = None, None

def isIntersectRects(leftTop1, rightBot1, leftTop2, rightBot2):
    x1, y1 = leftTop1
    x2, y2 = rightBot1
    x3, y3 = leftTop2
    x4, y4 = rightBot2
    if x2 <= x3 or x4 <= x1:
        return False
    if y2 <= y3 or y4 <= y1:
        return False
    return True


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
