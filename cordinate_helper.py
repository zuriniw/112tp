def getWorldPoints(app,points):
    newPoints = []
    for point in points:
        x, y = point[1]
        worldX = x + app.x0
        worldY = app.y0 - y
        newPoint = ['point',(worldX, worldY)]
        newPoints.append(newPoint)
    return newPoints