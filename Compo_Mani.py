'''
- Component
    - TypicleComponent
        - Move
'''
from cmu_graphics import *
from Components import TypicleComponent

## HELPER: take in world cdnt and give back drawing cdnt for drawing
def getDrawingPoint(x0,y0,worldPoint):
    wx, wy = worldPoint
    dx = wx + x0
    dy = y0 - wy
    drawingPoint = (dx, dy)
    return drawingPoint

## HELPER: take in world cdnt and give back drawing cdnt for drawing
def alignLists(L, M, default_value=None):
    L = [L] if not isinstance(L, list) else L
    M = [M] if not isinstance(M, list) else M
    if len(L) < len(M):
        last_item = L[-1] if L else default_value
        L.extend([last_item] * (len(M) - len(L)))
    elif len(M) < len(L):
        last_item = M[-1] if M else default_value
        M.extend([last_item] * (len(L) - len(M)))

########################################################################################
# PANEL is for reveal the value of any outputNode 
# output representation: same as its input
########################################################################################

class Move(TypicleComponent):
    def __init__(self, app):
        inputs = ['geo', 'vector']
        outputs = ['moved']
        name = 'Move\nGeo\nΛ'
        self.isGeo = True
        self.isDisplay = True
        super().__init__(app, inputs, outputs, name)
        
        self.inputDefaultValue = {
            'geo': [['cir',(0, 0),40]],
            'vector': [['vector',(200, -200)]]
        }
        
        for node in self.inputNodes:
            node.value = self.inputDefaultValue[node.name]
        self.outputNodes[0].value = self.calculate()

        self.hasAllInputs = True
        self.x0, self.y0 = app.x0, app.y0
    
    def calculate(self):
        geo_val = self.inputNodes[0].value      # get [['geoName',(x,y),...,....]['geoName',(x,y),...,....]...]
        vector_val = self.inputNodes[1].value   # get [['vector',(x,y)]['vector', (x,y)]...]
        
        #align_lists(geo_val, vector_val)
        #print(f'geo{geo_val} & vect{vector_val}')
        if not geo_val or not isinstance(geo_val, list):
            return [[None]]
            
        moved_geos = []
        for geo in geo_val:
            currShape = geo[0]
            x, y = geo[1]
            for vect in vector_val:
                # Get the vector displacement
                dx, dy = vect[1]  # vector format is ['vector', (dx,dy)]
                if currShape == 'cir':
                    r = geo[2]
                    moved_geos.append(['cir', (x + dx, y + dy), r])
                elif currShape == 'rect':
                    w = geo[2]
                    h = geo[3]
                    moved_geos.append(['rect', (x + dx, y + dy), w, h])
                elif currShape == 'point':
                    moved_geos.append(['point', (x + dx, y + dy)])
                
        return moved_geos if moved_geos else [[None]]

    def draw(self):
        if self.hasAllInputs:
            geo_val = self.inputNodes[0].value
            vector_val = self.inputNodes[1].value

            if not geo_val or not vector_val:
                return
                
            moved_geos = self.calculate()
            if not moved_geos or moved_geos[0] is None:
                return
                
            for geo in moved_geos:
                shape_type = geo[0]
                gx, gy = getDrawingPoint(self.x0, self.y0,geo[1])
                if shape_type == 'cir':
                    r = geo[2]
                    if int(r) != 0:
                        drawCircle(gx, gy, r, fill=None, border='blue', visible=self.isDisplay)
                elif shape_type == 'rect':
                    w = geo[2]
                    h = geo[3]
                    if int(w) != 0 and int(h) != 0:
                        drawRect(gx, gy, w, h, fill=None, border='blue', visible=self.isDisplay)
                elif shape_type == 'point':
                    drawCircle(gx, gy, 4, fill='white', border='blue', borderWidth=2, visible=self.isDisplay)
                
                for vect in vector_val:
                    vx0, vy0 = vect[1]
                    vx = gx - vx0
                    vy = gy + vy0
                    drawLine(vx, vy, gx, gy, fill='lightBlue', dashes=True, visible=self.isDisplay, opacity = 50)
    

