from cmu_graphics import *

from Components import *

from Compo_Special_Slider import *
from Compo_Analyse_Distance import *
from Compo_Special_Panel import *
from Compo_Geo import *
from Compo_Math import *
from Compo_Vector import *
from Compo_Mani import *
from Connection import Connections
from Toggle import Toggle
from Toolbar import *

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
    app.isMessageDisplay = True
    
    ## Toggle Panel Settings
    app.toggleStates = {
        'Comp Display': app.isCompDisplay,
        'Axis Display': app.isAxisDisplay,
        'Grid Display': app.isGridDisplay,
        'Dot Display': app.isDotDisplay,
        'Message Display': app.isMessageDisplay
    }
    
    ## Toggle Panel Layout
    app.toolbarHeight = 110
    app.toggleWidth, app.toggleHeight = 80, 40
    app.togglePanelWidth = 120
    app.togglePanelStartX = app.width - app.togglePanelWidth
    app.togglePanelStartY = app.toolbarHeight + app.paddingY
    
    ## Create toggle buttons
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
        'Vector': [Point, Vector, VectorPreview],
        'Geometry': [CircleCreator, RectCreator],
        'Math': [Slider1D, Slider2D, Series, Reverse, Square, SquareRoot, MultiplyPi, Absolute, Add, Subtract, Multiply, Divide],
        'Manipulation': [Move],
        'Analyze': [Panel, Distance],
        
    }
    app.activeCategory = 'Vector'
    loadToolbar(app)

    ## Dictionary mapping keys to component classes
    app.component_map = {
        's': Slider1D,
        'c': CircleCreator,
        'r': RectCreator,
        'p': Point,
        '2': Slider2D,
        'v': Vector,
        'm': Move

    }
    
    ## Instructions that will foating when hovering over compo buttons
    app.compoInfoMapping = {
        Vector: f"input:\n -start: geo point(s)\n -end: geo point(s)\n \noutput:\n -vector(s)\n{'-'*24}\nVector is invisable!\n\nFeed it in [Move Geo]\nOr use [Vect Preview]\nto have a look;-)",
        Point: f"input:\n -x: num(s)\n -y: num(s)\n \noutput:\n -geo point(s)\n{'-'*24}\npoint is the mother of\nalmost anything here\neg: Geometry, Vector,\n ..., except number\n who is the grandma!",
        VectorPreview: 'input:\n -vector: vector(s)\n -anchor: geo point(s)\n \noutput:\n -none',
        CircleCreator: 'input:\n -point: geo point(s)\n -radius: num(s)\n -isGradFill: boolean\n \noutput:\n -circle(s)',
        RectCreator: 'input:\n -point: geo point(s)\n -width: num(s)\n -height: num(s)\n \noutput:\n -rect(s)',
        Move: 'input:\n -geo:point/rect/cir..(s)\n -vector: vector(s)\n \noutput:\n -moved geo(s)',
        Series: f"input:\n -First: num\n -Step: num\n -Count: num\n \noutput:\n -list of nums\n{'-'*24}\nWhy not feed output\nto [Point]'s x or y to\ncreate points array?",
        Reverse: 'input:\n -n: num(s)\n \noutput:\n -negated num(s)',
        Square: 'input:\n -n: num(s)\n \noutput:\n -squared num(s)',
        SquareRoot: 'input:\n -n: num(s)\n \noutput:\n -the square root(s)',
        MultiplyPi: 'input:\n -n: num(s)\n \noutput:\n -π * n(s)',
        Absolute: 'input:\n -n: num(s)\n \noutput:\n -the absolute val(s)',
        Add: 'input:\n -n_1: num(s)\n -n_2: num(s)\n \noutput:\n -the sum(s)',
        Subtract: 'input:\n -n_1: num(s)\n -n_2: num(s)\n \noutput:\n -the difference(s)',
        Multiply: 'input:\n -n_1: num(s)\n -n_2: num(s)\n \noutput:\n -the product(s)',
        Divide: 'input:\n -n_1: num(s)\n -n_2: num(s)\n \noutput:\n -the quotient(s)',

        Slider1D: f"no input node here\noutput:\n -num\n{'-'*24}\n[DRAG HANDLE]\nto give 1 value \n\n[RIGHT CLICK]\nto set parameters\n - [TAB]:  navigate \n - [TYPE]:  enter\n - [ENTER]: set/toggle",
        Slider2D: f"no input node here\noutput:\n -num\n{'-'*24}\n[DRAG HANDLE]\nto give 1 value \n\n[RIGHT CLICK]\nto set parameters\n - [TAB]:  navigate \n - [TYPE]:  enter\n - [ENTER]: set/toggle",

        Panel: f"input:\n -any output\noutput:\n data repre\n{'-'*24}\nIt add transparency\nto your mysterious \ncomponents",
        Distance: f"input:\n -geo/point(s)\n -geo/point(s)\noutput:\n -distance num(s)\n{'-'*24}\nDistance can be\ninput(s) of other geo",

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

    ## CstmzingSlider
    app.editingField = 'nickname' 
    app.customInput = ''
    app.currCstmzSlider = None

    ## Right Click Toggle 
    app.currGeoComponent = None

    ## Hover Over Tool Bar 
    app.currCompInToolBar = None

    ## pinned sliders 
    app.pinnedSliders = []
    app.pinnedSliderHeight = 100
    app.currDraggingPinnedSlider = None

    app.dragOffset = {'x': 0, 'y': 0}

    app.message = ';-) Welcome 2 ShapeShift Playgound!'
    app.hintMessage = "DRAG-&-DROP a component from toolbar. Let's go!"
    app.secondHintMessage = 'press [BACKSPACE] to temporary block, or [TOGGLE OFF] me on the right panel'

    app.isSliderPlaying = False
    app.isSliderRecording = False
    app.stepsPerSecond = 28

def loadToolbar(app): 
    currbuttomCompoList = app.componentTypes[app.activeCategory]
    app.currButtomList = [ToolbarButton(app, app.borderX + currbuttomCompoList.index(buttomCompo) * (60 + app.paddingX), 40, buttomCompo) for buttomCompo in currbuttomCompoList]
    

def drawToolbar(app):
    tabHeight = 30
    drawLine(0, app.toolbarHeight, app.width, app.toolbarHeight)
    drawLine(0, tabHeight-1, app.width, tabHeight-1)
    for tab in app.tabs:
        tab.drawUI()
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
        gridSize = 40
        
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
            drawLine(app.borderX, y, app.togglePanelStartX, y, fill='lightGrey', lineWidth=0.5)
            
def drawDot(app):
    if app.isDotDisplay:
        gridSize = 40
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
                drawLabel('+', x,y, fill = 'grey',size = 16, opacity = 30)


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
                    fill=rgb(228,234,230), border = rgb(71,230,121), opacity=40, dashes = True)

def drawCstmzingSliderPopUp(app):
    currSlider = app.currCstmzSlider
    if currSlider in app.components:
        fields = currSlider.fields
        height = 20*len(fields)
        offsetY = -1 * (height + 10)
        
        # Draw popup background
        drawRect(currSlider.x, currSlider.y + offsetY - 10 , 120, height, fill='white', border='black')
        drawLine(currSlider.x+1.5, currSlider.y - 20,currSlider.x+1.5, currSlider.y, dashes = (3,3))
        
        # Draw fields
        for field, value in fields.items():
            # Highlight editing field
            if field == app.editingField:
                drawRect(currSlider.x, currSlider.y + offsetY - 10, 120, 20, fill='lightBlue', opacity=30)
                if app.customInput != '':
                    text = f"{field}: {app.customInput}_"  # Show cursor
                else:
                    text = f"{field}: {value}_"
            else:
                text = f"{field}: {value}"
            drawLabel(text, currSlider.x + 60, currSlider.y + offsetY)
            offsetY += 20
    
def drawGeoComponentPopUp(app):
    if app.currGeoComponent in app.components and app.currGeoComponent:
        
        currComponent = app.currGeoComponent
        fields = {
            'display': 'On' if currComponent.isDisplay else 'Off'
        }
        
        # Draw popup background
        drawRect(currComponent.x, currComponent.y - 40, 120, 20*len(fields),fill='white', border='black')
        
        # Draw fields
        offsetY = -30
        drawLine(currComponent.x+1, currComponent.y - 30,currComponent.x+1, currComponent.y, dashes = (3,3))
        for field, value in fields.items():
            # Highlight editing field
            if field == app.editingField:
                drawRect(currComponent.x, currComponent.y + offsetY - 10,
                         120, 20, fill='lightBlue', opacity=30)
            
            text = f"{field}: {value}"
            drawLabel(text, currComponent.x + 60, currComponent.y + offsetY)
            offsetY += 20

def drawPinnedSliders(app):
    for slider in app.pinnedSliders:
        slider.drawTwinUI(app)

def drawMessage(app):
    drawLabel(app.message, app.togglePanelStartX - app.paddingX, app.height - app.borderY*2, align = 'right', size = 16)       
    drawLabel(app.hintMessage, app.togglePanelStartX - app.paddingX, app.height - app.borderY*4, align = 'right', fill = 'blue' if not 'Invalid' in app.message else rgb(215, 127, 87), size = 14)       
    drawLabel(app.secondHintMessage, app.togglePanelStartX - app.paddingX, app.height - app.borderY*6, align = 'right', fill = 'grey', size = 14, opacity = 50)       

def redrawAll(app):
    drawPlayground(app)
    drawToolbar(app)
    drawGrid(app)
    drawAxis(app)
    drawDot(app)
    if app.isMessageDisplay:
        drawMessage(app)
    
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
    
    if (not app.isDraggingNewComponent) and app.currCompInToolBar:
        drawCurrCompoInToolBarInfo(app)

#########
def drawCurrCompoInToolBarInfo(app):
    if not app.currCompInToolBar:
        return
    
    x0, y0 = app.infoboxX, app.infoboxY
    comp = app.currCompInToolBar
    dy = app.paddingY+4

    if comp in app.compoInfoMapping:
        compInfo = app.compoInfoMapping[comp]
        
        textX0 = x0 + app.borderX
        textY0 = y0 + app.borderY
        
        height = len(compInfo.splitlines()) * (dy) + app.borderY
        width = 110

        drawRect(x0, y0, width + 2*app.borderX, height, 
            fill='white', border='black', borderWidth=2)
        
        # Calculate box dimensions dynamically
        lines = compInfo.splitlines()
        for i, line in enumerate(lines):
            textY = textY0 + i * dy
            height += i * 12
            drawLabel(line, textX0, textY, align = 'left')

def onMouseMove(app, mouseX, mouseY):
    ###### 1. Update Mouse Position ######
    app.mouseX = mouseX
    app.mouseY = mouseY
    
    ###### 2.  Node Hovering ######
    # Reset all node hover states
    for component in app.components:
        for node in component.inputNodes + component.outputNodes:
            node.isHovering = node.hitTest(mouseX, mouseY)
    
    ###### 3.  pinned slider button Hovering ######
    for pinnedSlider in app.pinnedSliders:
        if isinstance(pinnedSlider, PinnedSlider2D):
            for button in pinnedSlider.buttons:
                button.isHovering = button.hitTest(mouseX, mouseY)

    ###### 4.  Button Hovering ######
    for button in app.currButtomList:
        button.isHovering = button.hitTest(mouseX, mouseY)
        # Check toolbar button hovering
    for button in app.currButtomList:
        if button.hitTest(mouseX, mouseY):
            # Only set if not already set
            if app.currCompInToolBar != button.component:
                app.currCompInToolBar = button.component
                app.infoboxX, app.infoboxY = button.x, button.y + 65
            return
        
    ###### 5. Tab Hovering ######
    for tab in app.tabs:
        tab.isHovering = tab.hitTest(mouseX, mouseY)
    # Only reset if a button is no longer being hovered
    if app.currCompInToolBar is not None:
        app.currCompInToolBar = None


def onMousePress(app, mouseX, mouseY, button):
    #  left mouse button interaction
    if button == 0:
        currentTime = time.time()
        app.currCompInToolBar = []
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
                            if not app.selectedCompo:  # SINGLE DRAG
                                app.currDraggingComponent = component
                                app.dragOffset = {'x': mouseX - app.currDraggingComponent.x, 'y': mouseY - app.currDraggingComponent.y}
                                component.isDragging = True
                            else:  # GROUP DRAG
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
                if slider.hitTestHandle(mouseX, mouseY):
                    app.currDraggingPinnedSlider = slider
                    return
                if slider.recordButton.hitTest(mouseX, mouseY) and not slider.isSliderPlaying:
                    if slider.isSliderRecording == True:
                        slider.isSliderRecording = False
                        app.message = 'STOP Recording '
                        app.hintMessage = 'PRESS the ► ! cannot wait to watch it'
                    else:
                        slider.isSliderRecording = True
                        slider.store = []       # Clear previous stored
                        app.message = 'START Recording '
                        app.hintMessage = 'PRESS the ● button again to stop'
                    return
                elif slider.playButton.hitTest(mouseX, mouseY) and not slider.isSliderRecording:
                    slider.isSliderPlaying = not slider.isSliderPlaying
                    app.message = 'Nice try! PRESS ► again to stop'
                    app.hintMessage = 'I bet it is the best animation I v ever seen...'

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
    
    ####### 1.  Drag Selection ######
    if app.isDragSelecting:
        app.dragFrameEnd = (mouseX, mouseY)
    
    ####### 2.  Node Connection Dragging ######
    elif app.draggingNode:
        # Create temporary visual connection line
        app.tempConnection = (app.draggingNode, mouseX, mouseY)
        # Highlight potential connection targets
        for component in app.components:
            for node in component.inputNodes:
                node.isHovering = node.hitTest(mouseX, mouseY)
    
    ####### 3.  Component Dragging ######
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
        slider = app.currDraggingPinnedSlider
        x,y = slider.x, slider.y
        
        if isinstance(slider, PinnedSlider2D):
            # 2D slider
            normalized_x = (mouseX - x) / slider.width
            normalized_y = 1 - (mouseY - y) / slider.height  # Flip y axis
            
            newX = slider.min_val + normalized_x * (slider.max_val - slider.min_val)
            newY = slider.min_val + normalized_y * (slider.max_val - slider.min_val)
            
            # in domain
            newX = max(slider.min_val, min(slider.max_val, newX))
            newY = max(slider.min_val, min(slider.max_val, newY))
            slider.updateValue(newX, newY)

            # STORE THE MOUSE TRACK for recording
            if slider.isSliderRecording:
                slider.store.append((newX, newY))

        else:
            # 1D slider
            normalized_x = (mouseX - x) / slider.width
            newValue = slider.min_val + normalized_x * (slider.max_val - slider.min_val)
            newValue = max(slider.min_val, min(slider.max_val, newValue))
            slider.updateValue(newValue)

def onStep(app):
    for slider in app.pinnedSliders:
        if slider.isSliderPlaying:
            if len(slider.store) > 0:
                x, y = slider.store[0]
                slider.updateValue(x,y)
                # LOOP play
                slider.store = slider.store[1:] + [slider.store[0]]

def adjustPosition(app, comp, mouseX, mouseY):
    newX = mouseX - app.dragOffset['x']
    newY = mouseY - app.dragOffset['y']
    return newX, newY

def keepWithinBounds(app, x, y, com):
    x = max(4, min(x, app.width - com.width - 4))
    y = max(app.toolbarHeight + 2, min(y, app.height - com.height - 4))
    return x, y

def getFirstTwoLines(text):
    lines = text.splitlines()
    firstTwoLines = lines[:2] if len(lines) >= 2 else lines
    result = ' '.join(firstTwoLines)
    return result

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
            
            messageName = getFirstTwoLines(newComponent.name)
            app.message = f'A ^{messageName}^ added ;-)'
            if len(app.components)==2:
                app.hintMessage = 'Whoo why not WIRE them together?'  
            elif len(app.components)==1:
                app.hintMessage = "Nice try ;-) let's invite another component"
            else:
                app.hintMessage = "If you wanna remove the component/connection, just DOUBLE CLICK on it"

        # Reset dragging state
        app.isDraggingNewComponent = False
        app.draggedComponentType = None
        return
    
    ###### 2.  Node Connection Creation ######
    if app.draggingNode:
        nodeA = app.draggingNode
        for component in app.components:
            for node in component.inputNodes + component.outputNodes:
                if node.hitTest(mouseX, mouseY) and node.component != nodeA:
                    # Ensure one input and one output
                    if nodeA.isOutput != node.isOutput and nodeA.component != node.component:
                        startNode,endNode = (nodeA,node) if nodeA.isOutput else (node,nodeA)
                        # Create and setup new connection
                        new_connection = Connections(app,startNode, endNode)
                        new_connection.end_node.addConnection(new_connection)
                        new_connection.start_node.addConnection(new_connection)
                        if new_connection.isValid:
                            if endNode.component.isGeo and endNode.component.name !='Vector\nPreview\n~':
                                shapeName = endNode.component.outputNodes[0].value[0][0]
                                shapeCount = len(endNode.component.outputNodes[0].value)
                                if new_connection.isValid and shapeName != 'point':
                                    app.message = f'{shapeCount} {shapeName}(s) be drawn successfully :-)'
                                    app.hintMessage = 'Congrats! u can hide the base point(s) by right click and toggle'
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
        if app.selectedCompo:
            app.message = f'You have selected {len(app.selectedCompo)} component(s) ;-)'
            app.hintMessage = 'move ? delete ?'

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
        app.dragOffset = {'x': 0, 'y': 0}

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
        
        # GPT taught how to use try here
        elif key == 'enter':
            # Save changes and exit editing mode
            if app.editingField == 'nickname':
                app.currCstmzSlider.nickname = app.customInput  # Update nickname
            
            elif app.editingField == 'value':
                try:
                    new_value = float(app.customInput)
                    l, r = app.currCstmzSlider.min_val, app.currCstmzSlider.max_val
                    new_value = max(min(new_value, r), l)
                    app.currCstmzSlider.updateValue(new_value)
                except ValueError:
                    pass
            elif app.editingField == 'x':
                try:
                    new_x = float(app.customInput)
                    l, r = app.currCstmzSlider.min_val, app.currCstmzSlider.max_val
                    new_x = max(min(new_x, r), l)
                    app.currCstmzSlider.updateValue(new_x, app.currCstmzSlider.outputNodes[1].value)
                except ValueError:
                    pass
            elif app.editingField == 'y':
                try:
                    new_y = float(app.customInput)
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
                # switch precision level
                app.currCstmzSlider.current_precision_index = (
                    app.currCstmzSlider.current_precision_index + 1
                ) % len(app.currCstmzSlider.precision_options)
                
            elif app.editingField == 'pin':
                # Pin or unpin the slider
                app.currCstmzSlider.isPinned = not app.currCstmzSlider.isPinned
                if app.currCstmzSlider.isPinned:
                    # Create and add a pinned slider
                    i = len(app.pinnedSliders)
                    x=app.borderX*3 + i*180
                    baseY = app.height - app.pinnedSliderHeight + app.borderY * 2
                    if isinstance(app.currCstmzSlider,Slider1D):
                        y1=baseY
                        pinned_twin = PinnedSlider1D(app, app.currCstmzSlider, x,y1)
                    elif isinstance(app.currCstmzSlider,Slider2D):
                        y2=baseY - app.borderY * 7 - 4
                        pinned_twin = PinnedSlider2D(app, app.currCstmzSlider, x,y2)
                    app.pinnedSliders.append(pinned_twin)
                else:
                    # Remove the corresponding pinned slider
                    app.pinnedSliders = [slider for slider in app.pinnedSliders
                                        if slider.original_slider != app.currCstmzSlider]
                
            # only update(not reset)
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

    ####### 2.  Geometric Component Interaction ######
    elif app.currGeoComponent:
        if key == 'tab':
            # Toggle the display state of the component
            app.currGeoComponent.isDisplay = not app.currGeoComponent.isDisplay
            app.editingField = None  # Reset editing field
        elif key == 'escape':
            # Cancel and exit editing mode
            app.currGeoComponent = None
            app.editingField = 'nickname'

    ####### 3.  General Keypress Actions ######
    else:
        if key in app.component_map:
        # Use the mapped class to create and append the component
            create_and_append_component(app.component_map[key], app)
            
        elif key in ['backspace', 'delete']:
            # Delete selected components
            if app.selectedCompo:
                for compo in app.selectedCompo:
                    compo.deleteComponent(app)
                app.selectedCompo = []  # Clear all the selection
            else:
                app.message = ';-)'
                app.hintMessage = ''
                app.secondHintMessage = ''

def create_and_append_component(component_class, app):
    # Create a new
    newComponent = component_class(app)
    # Update node positions
    newComponent.updateNodePositions()
    # Add to the app list
    app.components.append(newComponent)

    messageName = getFirstTwoLines(newComponent.name)
    app.message = f'A ^{messageName}^ added ;-)'
    app.hintMessage = 'Whoo why not wire them together?' if len(app.components)==2 else "Nice try ;-) let's invite another component"


def main():
    runApp()

main()