from cmu_graphics import *
from Components import *
from Compo_Special import *
from Compo_Geo import *
from Compo_Math import *
from Compo_Vector import *
from Compo_Mani import *
from Connection import Connections
from Toggle import Toggle
from ToolbarButton import ToolbarButton
from ToolbarTab import ToolbarTab

import time

def onAppStart(app):
    ## Window Settings
    app.width = 1512
    app.height = 982
    app.mouseX = app.width/2
    app.mouseY = app.height/2
    
    ## UI Constants
    app.paddingX, app.paddingY = 8, 12
    app.borderX, app.borderY = 12, 12
    app.textHeight, app.textWidth = 13, 7
    app.centerLabelWidth = 80
    
    ## Component Management
    app.components = []
    app.selectedCompo = []
    app.currDraggingComponent = None
    app.lastClickTime = time.time()
    
    ## Connection Management
    app.connections = []
    app.draggingNode = None
    app.tempConnection = None
    
    ## Display Settings
    app.isCompDisplay = True
    app.isAxisDisplay = True
    app.isGridDisplay = True
    app.isDotDisplay = False
    app.isGuidbookDisplay = False
    
    ## Toggle Panel Settings
    app.toggleStates = {
        'Comp Display': app.isCompDisplay,
        'Axis Display': app.isAxisDisplay,
        'Grid Display': app.isGridDisplay,
        'Dot Display': app.isDotDisplay,
        'Guidbook Display': app.isGuidbookDisplay
    }
    
    ## Toggle Panel Layout
    app.toolbarHeight = 110
    app.toggleWidth, app.toggleHeight = 80, 40
    app.togglePanelWidth = 120
    app.togglePanelStartX = app.width - app.togglePanelWidth
    app.togglePanelStartY = app.toolbarHeight + app.paddingY
    
    # Create toggle buttons
    toggleStartX = app.togglePanelStartX + app.togglePanelWidth/2 - app.toggleWidth/2
    firstToggleStartY = app.togglePanelStartY + app.borderY * 3
    toggleNames = list(app.toggleStates.keys())
    app.toggles = [Toggle(app, toggleStartX, 
                         firstToggleStartY + i*(app.textHeight+app.paddingY*3+app.toggleHeight),
                         toggleNames[i], 
                         app.toggleStates[toggleNames[i]]) 
                  for i in range(len(toggleNames))]
    
    ## Grid Settings
    app.x0 = app.togglePanelStartX / 2
    app.y0 = app.height/2
    
    ## Toolbar Settings
    app.isDraggingNewComponent = False
    app.draggedComponentType = None
    app.componentTypes = {
        'Geometry': [CircleCreator, RectCreator],
        'Math': [Slider, Reverse, Square, SquareRoot, MultiplyPi, Absolute, Add, Subtract, Multiply, Divide],
        'Manipulation': [Move],
        'Analyze': [],
        'Vector': [Point, Vector, VectorPreview]
    }
    app.activeCategory = 'Geometry'
    loadToolbar(app)
    
    ## Toolbar Tabs
    app.tabs = []
    tabX = 0
    for category in list(app.componentTypes.keys()):
        isActive = (category == app.activeCategory)
        tab = ToolbarTab(tabX, 0, category, isActive)
        app.tabs.append(tab)
        tabX += tab.width - 2
    
    ## Drag Selection Settings
    app.isDragSelecting = False
    app.dragFrameStart = None
    app.dragFrameEnd = None
    
    ## Group Drag Settings
    app.dragGroupOldMouseX, app.dragGroupOldMouseX = None, None

    ## CstmzingSlider ##
    app.editingField = None  # 'nickname', 'min', or 'max'
    app.customInput = ''
    app.currCstmzSlider = None

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
        if x2 != x1 and y2 != y1:
            drawRect(min(x1, x2), min(y1, y2),
                    abs(x2 - x1), abs(y2 - y1),
                    fill='lightgrey', border = 'red', opacity=20, dashes = True)

def drawCstmzingSliderPopUp(app):
    currSlider = app.currCstmzSlider
    if currSlider in app.components:
        fields = {
            'nickname': currSlider.nickname,
            'min': str(currSlider.min_val),
            'max': str(currSlider.max_val)
        }

        # Draw popup background
        drawRect(currSlider.x, currSlider.y - 80, 120, 20*len(fields),
                fill='white', border='black')
        
        # Draw fields
        y_offset = -70
        drawLine(currSlider.x+1.5, currSlider.y - 20,currSlider.x+1.5, currSlider.y, dashes = (3,3))
        for field, value in fields.items():
            # Highlight editing field
            if field == app.editingField:
                drawRect(currSlider.x, currSlider.y + y_offset - 10, 
                        120, 20, fill='lightBlue', opacity=30)
                if app.customInput != '':
                    text = f"{field}: {app.customInput}_"  # Show cursor
                else:
                    text = f"{field}: {value}_"
            else:
                text = f"{field}: {value}"
            drawLabel(text, currSlider.x + 60, currSlider.y + y_offset)
            y_offset += 20
    
def drawGeoComponentPopUp(app):
    # 处理几何组件的弹出窗口
    if app.currGeoComponent in app.components and hasattr(app, 'currGeoComponent') and app.currGeoComponent:
        
        currComponent = app.currGeoComponent
        fields = {
            'display': 'On' if currComponent.isDisplay else 'Off'
        }
        
        # Draw popup background
        drawRect(currComponent.x, currComponent.y - 40, 120, 20*len(fields),
                 fill='white', border='black')
        
        # Draw fields
        y_offset = -30
        drawLine(currComponent.x+1, currComponent.y - 30,currComponent.x+1, currComponent.y, dashes = (3,3))
        for field, value in fields.items():
            # Highlight editing field
            if field == app.editingField:
                drawRect(currComponent.x, currComponent.y + y_offset - 10,
                         120, 20, fill='lightBlue', opacity=30)
            
            text = f"{field}: {value}"
            drawLabel(text, currComponent.x + 60, currComponent.y + y_offset)
            y_offset += 20

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
    
    if app.currCstmzSlider:
        drawCstmzingSliderPopUp(app)
    
    if hasattr(app, 'currGeoComponent') and app.currGeoComponent:
        drawGeoComponentPopUp(app)



def onMouseMove(app, mouseX, mouseY):
    ###### 1. Update Mouse Position ######
    app.mouseX = mouseX
    app.mouseY = mouseY
    
    ###### 2. Handle Node Hovering ######
    # Reset all node hover states
    for component in app.components:
        for node in component.inputNodes + component.outputNodes:
            node.isHovering = node.hitTest(mouseX, mouseY)
    
    ###### 3. Handle Button Hovering ######
    for button in app.currButtomList:
        button.isHovering = button.hitTest(mouseX, mouseY)


def onMousePress(app, mouseX, mouseY, button):
    if button == 0:
        currentTime = time.time()
        
        ###### 1. Node and Connection Interaction ######
        # Check if clicking on a node
        for component in app.components:
            for node in component.inputNodes + component.outputNodes:
                if node.hitTest(mouseX, mouseY):
                    app.draggingNode = node
                    return
        
        # Check if double-clicking on a connection
        for conn in app.connections:
            if conn.hitTest(mouseX, mouseY):
                if currentTime - app.lastClickTime < 0.3:  # Double click
                    conn.deleteConnection(app)
                    return
                app.lastClickTime = currentTime
                return
        
        ###### 2. Toolbar Interaction ######
        # Check toolbar buttons
        for button in app.currButtomList:
            if button.hitTest(mouseX, mouseY):
                app.currDraggingComponent = None
                app.isDraggingNewComponent = True
                app.draggedComponentType = button.component
                return
        
        # Check toolbar tabs
        for tab in app.tabs:
            if tab.hitTest(mouseX, mouseY):
                app.currDraggingComponent = None
                for t in app.tabs:
                    t.isActive = (t == tab)
                app.activeCategory = tab.category
                loadToolbar(app)
                return
        
        ###### 3. Toggle Panel Interaction ######
        for toggle in app.toggles:
            if toggle.hitTest(mouseX, mouseY):
                toggle.isOn = not toggle.isOn
                var_name = 'is' + toggle.name.replace(' ', '')
                setattr(app, var_name, toggle.isOn)
                app.toggleStates[toggle.name] = toggle.isOn
                return
        
        ###### 4. Component Interaction ######
        hitComponent = False
        for component in app.components:
            if component.hitTest(mouseX, mouseY):
                hitComponent = True
                
                # Handle double-click deletion
                if currentTime - app.lastClickTime < 0.3:
                    component.deleteComponent(app)
                    app.currDraggingComponent = None
                    return
                
                # Handle slider interaction
                if isinstance(component, Slider):
                    if component.hitTestHandle(mouseX, mouseY):
                        component.isDraggingHandle = True
                        app.currDraggingComponent = component
                    else:
                        app.currDraggingComponent = component
                        component.isDragging = True
                        component.isDraggingHandle = False
                # Handle regular component interaction
                else:
                    if not app.selectedCompo:  # Single component drag
                        app.currDraggingComponent = component
                        component.isDragging = True
                    else:  # Group drag
                        app.dragGroupOldMouseX, app.dragGroupOldMouseY = mouseX, mouseY
                        app.currDraggingComponent = app.selectedCompo
                        for compo in app.selectedCompo:
                            compo.isDragging = True
                
                app.lastClickTime = currentTime
                break
        
        ###### 5. Empty Space Interaction ######
        if not hitComponent:
            app.currDraggingComponent = None
            app.currCstmzSlider = None
            app.currGeoComponent = None
            
        if app.currDraggingComponent is None:
            # Clear selection
            for compo in app.selectedCompo:
                compo.isSelected = False
            app.selectedCompo = []
            
            # Initialize drag selection
            app.isDragSelecting = True
            app.dragFrameStart = (mouseX, mouseY)
            app.dragFrameEnd = (mouseX, mouseY)

        ###### 6. CstmzingSlider pop-up window interaction ######
    
    # Check for right-click on slider
    if button == 2:
        for component in app.components:
            if isinstance(component, Slider) and component.hitTest(mouseX, mouseY) and (not app.currGeoComponent):
                app.currCstmzSlider = component
                return
            elif (isinstance(component, TypicleComponent) and 
            component.isGeo and 
            component.hitTest(mouseX, mouseY)) and (not app.currCstmzSlider):
                app.currGeoComponent = component
                app.editingField = 'display'
                app.customInput = ''
                return

def onMouseDrag(app, mouseX, mouseY):
    # Update current mouse position
    app.mouseX = mouseX
    app.mouseY = mouseY
    
    ###### 1. Handle Drag Selection ######
    if app.isDragSelecting:
        app.dragFrameEnd = (mouseX, mouseY)
    
    ###### 2. Handle Node Connection Dragging ######
    elif app.draggingNode:
        # Create temporary visual connection line
        app.tempConnection = (app.draggingNode, mouseX, mouseY)
        # Highlight potential connection targets
        for component in app.components:
            for node in component.inputNodes:
                node.isHovering = node.hitTest(mouseX, mouseY)
    
    ###### 3. Handle Component Dragging ######
    elif app.currDraggingComponent:
        comp = app.currDraggingComponent
        
        # Single Component Dragging
        if not isinstance(comp, list):
            if isinstance(comp, Slider):
                if comp.isDraggingHandle:
                    # Handle slider value adjustment
                    normalized_x = (mouseX - comp.x) / comp.width
                    newValue = comp.min_val + normalized_x * (comp.max_val - comp.min_val)
                    newValue = max(comp.min_val, min(comp.max_val, newValue))
                    comp.updateValue(newValue)
                else:
                    # Handle slider position movement
                    newX, newY = adjustPosition(comp, mouseX, mouseY)
                    comp.x, comp.y = keepWithinBounds(app, newX, newY, comp)
                    comp.updateNodePositions()
            else:
                # Handle regular component movement
                newX, newY = adjustPosition(comp, mouseX, mouseY)
                comp.x, comp.y = keepWithinBounds(app, newX, newY, comp)
                comp.updateNodePositions()
        
        # Multiple Components Dragging
        else:
            # Calculate movement delta
            dx = mouseX - app.dragGroupOldMouseX
            dy = mouseY - app.dragGroupOldMouseY
            
            # Move all selected components
            for selectedCompo in app.currDraggingComponent:
                newX, newY = selectedCompo.x + dx, selectedCompo.y + dy
                selectedCompo.x, selectedCompo.y = keepWithinBounds(app, newX, newY, selectedCompo)
                selectedCompo.updateNodePositions()
            
            # Update reference point for next drag
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
    ###### 1. Handle New Component Creation ######
    if app.isDraggingNewComponent and app.draggedComponentType:
        if mouseY > app.toolbarHeight:  # Only create if dropped in valid area
            # Create and position new component
            newComponent = app.draggedComponentType(app)
            newComponent.x = mouseX - newComponent.width/2
            newComponent.y = mouseY - newComponent.height/2
            app.components.append(newComponent)
            newComponent.updateNodePositions()
        
        # Reset dragging state
        app.isDraggingNewComponent = False
        app.draggedComponentType = None
        return
    
    ###### 2. Handle Node Connection Creation ######
    if app.draggingNode:
        start_node = app.draggingNode
        for component in app.components:
            for node in component.inputNodes + component.outputNodes:
                if node.hitTest(mouseX, mouseY) and node != start_node:
                    # Ensure one input and one output
                    if start_node.isOutput != node.isOutput:
                        # Create and setup new connection
                        new_connection = Connections(start_node, node)
                        new_connection.start_node.addConnection(new_connection)
                        new_connection.end_node.addConnection(new_connection)
                        app.connections.append(new_connection)
        
        # Reset node dragging state
        app.draggingNode = None
        app.tempConnection = None
    
    ###### 3. Handle Drag Selection ######
    if app.isDragSelecting:
        app.isDragSelecting = False
        # Check each component for intersection with selection frame
        for compo in app.components:
            if isIntersectRects((compo.x, compo.y), 
                              (compo.x + compo.width, compo.y + compo.height),
                              app.dragFrameStart, app.dragFrameEnd):
                app.selectedCompo.append(compo)
                compo.isSelected = True
        
        # Reset selection frame
        app.dragFrameStart = None
        app.dragFrameEnd = None
    
    ###### 4. Reset Group Dragging Reference ######
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
    if app.currCstmzSlider:
        if key == 'tab':
            fields = ['nickname', 'min', 'max']
            if app.editingField is None:
                app.editingField = fields[0]
                app.customInput = ''
            else:
                idx = (fields.index(app.editingField) + 1) % len(fields)
                app.editingField = fields[idx]
                app.customInput = ''
        elif key == 'enter':
            # Save changes and exit
            if app.editingField == 'nickname':
                app.currCstmzSlider.nickname = app.customInput
            elif app.editingField == 'min':
                try:
                    new_min = int(app.customInput)
                    # 检查新的最小值是否小于最大值
                    if new_min < app.currCstmzSlider.max_val:
                        app.currCstmzSlider.min_val = new_min
                except ValueError:
                    pass
            elif app.editingField == 'max':
                try:
                    new_max = int(app.customInput)
                    # 检查新的最大值是否大于最小值
                    if new_max > app.currCstmzSlider.min_val:
                        app.currCstmzSlider.max_val = new_max
                except ValueError:
                    pass
            app.currCstmzSlider.outputNodes[0].value = (app.currCstmzSlider.min_val + app.currCstmzSlider.max_val) / 2

            #app.currCstmzSlider = None
            #app.editingField = None
            app.customInput = ''
        elif key == 'escape':
            # Discard changes and exit
            app.currCstmzSlider = None
            app.editingField = None
            app.customInput = ''
        elif key == 'backspace':
            app.customInput = app.customInput[:-1]
        elif len(key) == 1:  # Single character input
            app.customInput += key

    if hasattr(app, 'currGeoComponent') and app.currGeoComponent:
        if key == 'tab':
            # 切换显示状态
            app.currGeoComponent.isDisplay = not app.currGeoComponent.isDisplay
            app.editingField = None
        elif key == 'escape':
            # 取消操作
            app.currGeoComponent = None
            app.editingField = None

    else:        
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
        elif key == 'p':
            newPoint = Point(app)
            newPoint.updateNodePositions()
            app.components.append(newPoint)

        elif key in ['backspace', 'delete']:
            if app.selectedCompo:
                for compo in app.selectedCompo:
                    compo.deleteComponent(app)
                # Clear selection
                app.selectedCompo = []
        
def main():
    runApp()

main()
