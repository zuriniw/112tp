from cmu_graphics import *
from Components import *

#from Compo_Special_Slider import *
from Compo_Special_Slider import *

from Compo_Special_Panel import *
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
        'Math': [Slider1D, Slider2D, Series, Reverse, Square, SquareRoot, MultiplyPi, Absolute, Add, Subtract, Multiply, Divide],
        'Manipulation': [Move],
        'Analyze': [Panel],
        'Vector': [Point, Vector, VectorPreview]
    }
    app.activeCategory = 'Geometry'
    loadToolbar(app)

    # Dictionary mapping keys to component classes
    app.component_map = {
        's': Slider1D,
        'c': CircleCreator,
        'r': RectCreator,
        'p': Point,
        '2': Slider2D
    }
    
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
    app.editingField = 'nickname'  # 'nickname', 'min', or 'max'
    app.customInput = ''
    app.currCstmzSlider = None
    
    app.currGeoComponent = None

    app.pinnedSliders = []
    app.pinnedSliderHeight = 100
    app.currDraggingPinnedSlider = None

    app.dragOffset = {'x': 0, 
                         'y': 0}



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
        fields = currSlider.fields
        height = 20*len(fields)
        y_offset = -1 * (height + 10)
        
        # Draw popup background
        drawRect(currSlider.x, currSlider.y + y_offset - 10 , 120, height, fill='white', border='black')
        drawLine(currSlider.x+1.5, currSlider.y - 20,currSlider.x+1.5, currSlider.y, dashes = (3,3))
        
        # Draw fields
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

def drawPinnedSliders(app):
    startX = app.borderX * 3
    for slider in app.pinnedSliders:
        i = app.pinnedSliders.index(slider)
        x = startX + 180 * i
        
        # 计算基准y位置，确保昵称对齐
        baseY = app.height - app.pinnedSliderHeight + app.borderY*2
        if isinstance(slider, PinnedSlider2D):
            y = baseY - app.borderY*7 - 4  # 调整2D滑块的整体位置
        else:
            y = baseY
            
        slider.drawTwinUI(x, y)

        

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

        if app.isDragSelecting:
            drawDraggingFrame(app)
    
        if app.currCstmzSlider:
            drawCstmzingSliderPopUp(app)
        
    drawRect(app.togglePanelStartX, app.togglePanelStartY, app.togglePanelWidth, app.height - app.toolbarHeight - 2 * app.paddingY, border = 'black', fill = 'white')
    
    for toggle in app.toggles:
        toggle.drawUI()
    
    for component in app.components:
        if isinstance(component, TypicleComponent) and component.isGeo:
            component.draw()
    
    if app.currGeoComponent:
        drawGeoComponentPopUp(app)
    
    if not app.isCompDisplay:
        drawPinnedSliders(app)



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
    # Handle left mouse button interaction
    if button == 0:
        currentTime = time.time()

        ####### 1. Toolbar Interaction ######
        # Check interaction with toolbar buttons
        for button in app.currButtomList:
            if button.hitTest(mouseX, mouseY):
                app.currDraggingComponent = None  # Reset dragging state
                app.isDraggingNewComponent = True  # Enable dragging new component
                app.draggedComponentType = button.component  # Set component type
                return
        
        # Check interaction with toolbar tabs
        for tab in app.tabs:
            if tab.hitTest(mouseX, mouseY):
                app.currDraggingComponent = None  # Reset dragging state
                for t in app.tabs:
                    t.isActive = (t == tab)  # Activate selected tab
                app.activeCategory = tab.category  # Update active category
                loadToolbar(app)  # Load the toolbar for the active tab
                return
        
        ####### 2. Toggle Panel Interaction ######
        # Handle toggle button state changes
        for toggle in app.toggles:
            if toggle.hitTest(mouseX, mouseY):
                toggle.isOn = not toggle.isOn  # Toggle the state
                var_name = 'is' + toggle.name.replace(' ', '')  # Create attribute name
                setattr(app, var_name, toggle.isOn)  # Update attribute dynamically
                app.toggleStates[toggle.name] = toggle.isOn  # Update toggle states
                return
            
        ####### 3. Component Display Interaction ######
        if app.isCompDisplay:
            ####### 3.1 Node and Connection Interaction ######
            # Check if clicking on a node
            for component in app.components:
                for node in component.inputNodes + component.outputNodes:
                    if node.hitTest(mouseX, mouseY):
                        app.draggingNode = node  # Start dragging the node
                        return
            
            # Check for double-click on a connection to delete it
            for conn in app.connections:
                if conn.hitTest(mouseX, mouseY):
                    if currentTime - app.lastClickTime < 0.3:  # Detect double-click
                        conn.deleteConnection(app)  # Delete the connection
                        return
                    app.lastClickTime = currentTime  # Update last click time
                    return
            
            ####### 3.2 Component Interaction ######
            hitComponent = False
            for component in app.components:
                if component.hitTest(mouseX, mouseY):
                    hitComponent = True
                    
                    # Handle double-click to delete component
                    if currentTime - app.lastClickTime < 0.3:  # Detect double-click
                        component.deleteComponent(app)  # Delete the component
                        app.currDraggingComponent = None  # Reset dragging state
                        return
                    
                    # Handle slider-specific interaction
                    if isinstance(component, Slider):
                        if component.hitTestHandle(mouseX, mouseY):
                            component.isDraggingHandle = True
                            app.currDraggingComponent = component
                        else:
                            if not app.selectedCompo:  # 单个拖拽
                                app.currDraggingComponent = component
                                app.dragOffset = {'x': mouseX - app.currDraggingComponent.x, 'y': mouseY - app.currDraggingComponent.y}
                                component.isDragging = True
                            else:  # 群组拖拽
                                app.dragGroupOldMouseX, app.dragGroupOldMouseY = mouseX, mouseY
                                app.currDraggingComponent = app.selectedCompo
                                for compo in app.selectedCompo:
                                    compo.isDragging = True
                            component.isDraggingHandle = False
                    # Handle general component interaction
                    else:
                        if not app.selectedCompo:  # Single component dragging
                            app.currDraggingComponent = component
                            app.dragOffset = {'x': mouseX - app.currDraggingComponent.x, 'y': mouseY - app.currDraggingComponent.y}
                            component.isDragging = True
                        else:  # Group dragging
                            app.dragGroupOldMouseX, app.dragGroupOldMouseY = mouseX, mouseY
                            app.currDraggingComponent = app.selectedCompo
                            for compo in app.selectedCompo:
                                compo.isDragging = True
                    
                    app.lastClickTime = currentTime  # Update last click time
                    break
            
            ####### 3.3 Empty Space Interaction ######
            if not hitComponent:
                app.currDraggingComponent = None  # Reset dragging state
                app.currCstmzSlider = None  # Clear custom slider
                app.currGeoComponent = None  # Clear geometric component
                app.editingField = 'nickname'
                
                if app.currDraggingComponent is None:
                    for compo in app.selectedCompo:
                        compo.isSelected = False  # Deselect all components
                    app.selectedCompo = []  # Clear selected components
                    
                    app.isDragSelecting = True  # Start drag selection
                    app.dragFrameStart = (mouseX, mouseY)  # Set selection start point
                    app.dragFrameEnd = (mouseX, mouseY)  # Set selection end point
        
        ####### 4. Pinned Sliders Interaction ######
        elif not app.isCompDisplay:
            # Check if a pinned slider handle is clicked
            for slider in app.pinnedSliders:
                i = app.pinnedSliders.index(slider)  # Get slider index
                x = 3 * app.borderX + 180 * i  # Calculate slider position
                
                baseY = app.height - app.pinnedSliderHeight + app.borderY*2
                if isinstance(slider, PinnedSlider2D):
                    y = baseY - app.borderY*7 - 4  # 调整2D滑块的整体位置
                else:
                    y = baseY
                
                if slider.hitTestHandle(mouseX, mouseY, x, y):
                    app.currDraggingPinnedSlider = {  # Start dragging the pinned slider
                        'slider': slider,
                        'x': x,
                        'y': y
                    }
                    return

    ####### 5. Slider Customization Interaction ######
    # Handle right mouse button interaction
    elif button == 2:
        # Check if clicking on sliders or geometric components
        for component in app.components:
            if isinstance(component, Slider) and component.hitTest(mouseX, mouseY) and not app.currGeoComponent:
                app.currCstmzSlider = component  # Open slider customization
                return
            elif (isinstance(component, TypicleComponent) and 
                  component.isGeo and 
                  component.hitTest(mouseX, mouseY)) and not app.currCstmzSlider:
                app.currGeoComponent = component  # Open geometric component customization
                app.editingField = 'display'  # Set editing field
                app.customInput = ''  # Reset custom input
                return

    

def onMouseDrag(app, mouseX, mouseY):
    # Update current mouse position
    app.mouseX = mouseX
    app.mouseY = mouseY
    
    ####### 1. Handle Drag Selection ######
    if app.isDragSelecting:
        app.dragFrameEnd = (mouseX, mouseY)
    
    ####### 2. Handle Node Connection Dragging ######
    elif app.draggingNode:
        # Create temporary visual connection line
        app.tempConnection = (app.draggingNode, mouseX, mouseY)
        # Highlight potential connection targets
        for component in app.components:
            for node in component.inputNodes:
                node.isHovering = node.hitTest(mouseX, mouseY)
    
    ####### 3. Handle Component Dragging ######
    elif app.currDraggingComponent:
        comp = app.currDraggingComponent
        
        # Single Component Dragging
        if not isinstance(comp, list):
            if isinstance(comp, Slider):
                if comp.isDraggingHandle:
                    comp.handleDrag(mouseX, mouseY)
                else:
                    # slider position movement for both 1D and 2D sliders
                    newX, newY = adjustPosition(app, comp, mouseX, mouseY)
                    comp.x, comp.y = keepWithinBounds(app, newX, newY, comp)
                    comp.updateNodePositions()
            else:
                # regular component movement
                newX, newY = adjustPosition(app, comp, mouseX, mouseY)
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

    ####### 4. Handle Pinned Slider Dragging ######
    elif app.currDraggingPinnedSlider:
        slider = app.currDraggingPinnedSlider['slider']
        x = app.currDraggingPinnedSlider['x']
        y = app.currDraggingPinnedSlider['y']
        
        if isinstance(slider, PinnedSlider2D):
            # 2D slider处理
            normalized_x = (mouseX - x) / slider.width
            normalized_y = 1 - (mouseY - y) / slider.height  # 反转y轴
            
            newX = slider.min_val + normalized_x * (slider.max_val - slider.min_val)
            newY = slider.min_val + normalized_y * (slider.max_val - slider.min_val)
            
            # 确保值在有效范围内
            newX = max(slider.min_val, min(slider.max_val, newX))
            newY = max(slider.min_val, min(slider.max_val, newY))
            
            slider.updateValue(newX, newY)
        else:
            # 1D slider处理
            normalized_x = (mouseX - x) / slider.width
            newValue = slider.min_val + normalized_x * (slider.max_val - slider.min_val)
            newValue = max(slider.min_val, min(slider.max_val, newValue))
            slider.updateValue(newValue)


def adjustPosition(app, comp, mouseX, mouseY):
    newX = mouseX - app.dragOffset['x']
    newY = mouseY - app.dragOffset['y']
    return newX, newY

def keepWithinBounds(app, x, y, com):
    x = max(4, min(x, app.width - com.width - 4))
    y = max(app.toolbarHeight + 2, min(y, app.height - com.height - 4))
    return x, y


def onMouseRelease(app, mouseX, mouseY):
    ###### 1.  New Component Creation ######
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
    
    ###### 2.  Node Connection Creation ######
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
    
    ###### 3.  Drag Selection ######
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
    
    if app.currDraggingPinnedSlider:
        app.currDraggingPinnedSlider = None

    
    ###### 4. Reset Component Dragging States ######
    if app.currDraggingComponent:
        if isinstance(app.currDraggingComponent, list):
            for comp in app.currDraggingComponent:
                comp.isDragging = False
        else:
            app.currDraggingComponent.isDragging = False
            if isinstance(app.currDraggingComponent, (Slider1D, Slider2D)):
                app.currDraggingComponent.isDraggingHandle = False
        app.currDraggingComponent = None
        app.dragOffset = {'x': 0, 
                         'y': 0}

    ###### 5. Reset Pinned Slider State ######
    if app.currDraggingPinnedSlider:
        app.currDraggingPinnedSlider = None

    ###### 6. Reset Group Dragging Reference ######
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
    ####### 1. Handle Custom Slider Interaction ######
    if app.currCstmzSlider:
        if key == 'tab':
            # Switch between editable fields in the slider
            fields = list(app.currCstmzSlider.fields.keys())
            if app.editingField is None:
                app.editingField = fields[0]  # Start editing the first field
                app.customInput = ''  # Clear input
            else:
                idx = (fields.index(app.editingField) + 1) % len(fields)
                app.editingField = fields[idx]  # Switch to the next field
                app.customInput = ''  # Clear input
        
        elif key == 'enter':
            # Save changes and exit editing mode
            if app.editingField == 'nickname':
                app.currCstmzSlider.nickname = app.customInput  # Update nickname
            
            elif app.editingField == 'value':
                try:
                    new_value = float(app.customInput)
                    # 确保输入值在有效范围内
                    l, r = app.currCstmzSlider.min_val, app.currCstmzSlider.max_val
                    new_value = max(min(new_value, r), l)
                    app.currCstmzSlider.updateValue(new_value)
                except ValueError:
                    pass
            elif app.editingField == 'x':
                try:
                    new_x = float(app.customInput)
                    # 确保输入值在有效范围内
                    l, r = app.currCstmzSlider.min_val, app.currCstmzSlider.max_val
                    new_x = max(min(new_x, r), l)
                    app.currCstmzSlider.updateValue(new_x, app.currCstmzSlider.outputNodes[1].value)
                except ValueError:
                    pass
            elif app.editingField == 'y':
                try:
                    new_y = float(app.customInput)
                    # 确保输入值在有效范围内
                    l, r = app.currCstmzSlider.min_val, app.currCstmzSlider.max_val
                    new_y = max(min(new_y, r), l)
                    app.currCstmzSlider.updateValue(app.currCstmzSlider.outputNodes[0].value, new_y)
                except ValueError:
                    pass
            elif app.editingField == 'min':
                try:
                    new_min = int(app.customInput)
                    if new_min < app.currCstmzSlider.max_val:  # Validate minimum value
                        app.currCstmzSlider.min_val = new_min
                except ValueError:
                    pass
            elif app.editingField == 'max':
                try:
                    new_max = int(app.customInput)
                    if new_max > app.currCstmzSlider.min_val:  # Validate maximum value
                        app.currCstmzSlider.max_val = new_max
                except ValueError:
                    pass
            elif app.editingField == 'precision':
                # 切换精度
                app.currCstmzSlider.current_precision_index = (
                    app.currCstmzSlider.current_precision_index + 1
                ) % len(app.currCstmzSlider.precision_options)
                
            elif app.editingField == 'pin':
                # Pin or unpin the slider
                app.currCstmzSlider.isPinned = not app.currCstmzSlider.isPinned
                if app.currCstmzSlider.isPinned:
                    # Create and add a pinned slider
                    if isinstance(app.currCstmzSlider,Slider1D):
                        pinned_twin = PinnedSlider1D(app.currCstmzSlider, app)
                    elif isinstance(app.currCstmzSlider,Slider2D):
                        pinned_twin = PinnedSlider2D(app.currCstmzSlider, app)
                    app.pinnedSliders.append(pinned_twin)
                else:
                    # Remove the corresponding pinned slider
                    app.pinnedSliders = [slider for slider in app.pinnedSliders
                                        if slider.original_slider != app.currCstmzSlider]
                
            # 只更新字段，不重置值
            app.currCstmzSlider.updateFields()
            # Reset input and exit editing
            app.customInput = ''

            if app.currCstmzSlider.isPinned:
                for pinnedSlider in app.pinnedSliders:
                    if pinnedSlider.original_slider == app.currCstmzSlider:
                        pinnedSlider.updateFields()



        elif key == 'escape':
            # Exit editing without saving changes
            app.currCstmzSlider = None
            app.editingField = None
            app.customInput = ''
        elif key == 'backspace':
            # Remove the last character from the input
            app.customInput = app.customInput[:-1]
        elif len(key) == 1:  # Single character input
            app.customInput += key

    ####### 2. Handle Geometric Component Interaction ######
    elif hasattr(app, 'currGeoComponent') and app.currGeoComponent:
        if key == 'tab':
            # Toggle the display state of the component
            app.currGeoComponent.isDisplay = not app.currGeoComponent.isDisplay
            app.editingField = None  # Reset editing field
        elif key == 'escape':
            # Cancel and exit editing mode
            app.currGeoComponent = None
            app.editingField = 'nickname'

    ####### 3. Handle General Keypress Actions ######
    else:
        if key in app.component_map:
        # Use the mapped class to create and append the component
            create_and_append_component(app.component_map[key], app)

        elif key in ['backspace', 'delete']:
            # Delete selected components
            if app.selectedCompo:
                for compo in app.selectedCompo:
                    compo.deleteComponent(app)
                app.selectedCompo = []  # Clear the selection

def create_and_append_component(component_class, app):
    # Create a new component instance
    new_component = component_class(app)
    # Update node positions if the method exists
    if hasattr(new_component, 'updateNodePositions'):
        new_component.updateNodePositions()
    # Append the component to the app's component list
    app.components.append(new_component)

def main():
    runApp()

main()
