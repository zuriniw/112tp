from cmu_graphics import *
from Components import Slider, CircleCreator, RectCreator
from Connection import Connections
from Toggle import Toggle
from ToolbarButton import ToolbarButton
from ToolbarTab import ToolbarTab

import time

def onAppStart(app):
    app.width = 1512
    app.height = 982
    app.toolbarHeight = 110
    app.components = []
    app.selectedComponent = None
    app.lastClickTime = time.time()

    app.paddingX, app.paddingY = 8, 12
    app.borderX, app.borderY = 12, 12
    app.textHeight, app.textWidth = 13, 7

    app.connections = []
    app.draggingNode = None
    app.tempConnection = None

    app.isCompDisplay = True
    app.isGridDisplay = False
    app.isDotDisplay = False
    app.isGuidbookDisplay = False

    app.toggleStates = {
        'Comp Display': app.isCompDisplay,
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

    # Toolbar organization
    app.categories = ['Geometry', 'Math', 'Other', 'Line']
    app.activeCategory = 'Geometry'  # Default active category

    app.isDraggingNewComponent = False
    app.draggedComponentType = None

    app.componentTypes = {
        'Geometry': [CircleCreator, RectCreator],
        'Math': [Slider],
        'Other': [],
        'Line': []
    }
    initToolbar(app)
    
    # Toolbar tab
    app.tabs = []
    tabX = 0
    for category in app.categories:
        isActive = (category == app.activeCategory)
        tab = ToolbarTab(tabX, 0, category, isActive)
        app.tabs.append(tab)
        tabX += tab.width - 2

def initToolbar(app): 
    buttomCompoList = app.componentTypes[app.activeCategory]
    app.buttomList = [ToolbarButton(app, app.borderX + buttomCompoList.index(buttomCompo) * (50 + app.paddingX), 40, buttomCompo) for buttomCompo in buttomCompoList]

def drawToolbar(app):
    tabHeight = 30
    drawLine(0, app.toolbarHeight, app.width, app.toolbarHeight)
    drawLine(0, tabHeight-1, app.width, tabHeight-1)
    # 绘制标签页
    for tab in app.tabs:
        tab.drawUI()
    # 绘制按钮
    for button in app.buttomList:
        button.drawUI()

def drawPlayground(app):
    # big background
    drawRect(0, 0, app.width, app.height, fill='white')
    
def redrawAll(app):
    drawPlayground(app)
    drawToolbar(app)
    if app.isCompDisplay:
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
                    lineWidth=2, fill='lightGrey', dashes = (4,2))
        
        # Draw component being dragged
        if app.isDraggingNewComponent and app.draggedComponentType:
            preview = app.draggedComponentType(app)
            preview.x = app.mouseX - preview.width/2
            preview.y = app.mouseY - preview.height/2
            preview.drawUI()
    
    drawRect(app.togglePanelStartX, app.togglePanelStartY, app.togglePanelWidth, app.height - app.toolbarHeight - 2 * app.paddingY, border = 'black', fill = 'white')
    for toggle in app.toggles:
        toggle.drawUI()

    

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
            if currentTime - app.lastClickTime < 0.3:
                app.connections.remove(connection)
                return
            app.lastClickTime = currentTime
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
    
    # 检查toolbar buttom


    # 检查toobar tab
    for tab in app.tabs:
        if tab.hitTest(mouseX, mouseY):
            # 更新活动状态
            for t in app.tabs:
                t.isActive = (t == tab)
            app.activeCategory = tab.category
            # 重新初始化工具栏按钮
            initToolbar(app)
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
                app.selectedComponent = None
                return
            # 2///拖动手柄
            if isinstance(component, Slider):
                if component.hitTestHandle(mouseX, mouseY):
                    # 点击到滑块手柄
                    component.isDraggingHandle = True
                    app.selectedComponent = component
                else:
                    # 点击到滑块其他部分，只设置拖动状态
                    app.selectedComponent = component
                    component.isDragging = True
                    component.isDraggingHandle = False
            # 3///点到组件
            else:
                app.selectedComponent = component
                component.isDragging = True
            app.lastClickTime = currentTime
            break
    if not hitComponent:
        app.selectedComponent = None        

def onMouseDrag(app, mouseX, mouseY):
    if app.draggingNode:
        # 处理节点拖动和悬停检测
        app.tempConnection = (app.draggingNode, mouseX, mouseY)
        
        # 检查是否悬停在任何输入节点上
        for component in app.components:
            for node in component.inputNodes:  # 只检查输入节点
                if node.hitTest(mouseX, mouseY):
                    node.isHovering = True
                else:
                    node.isHovering = False
                    
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
