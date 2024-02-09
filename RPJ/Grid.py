from math import ceil
from pygame.math import Vector2

class Grid:
    '''Always Update Grid Size and map size when creating games '''
    def __init__(self,mapSize=(500,500),gridNumber = (10,10)):
       # self.gridNumber = mapSize[0]//gridNumber[0],mapSize[1]//gridNumber[1]
        self.mapSize = mapSize
        self.gridNumber = gridNumber
        self.gridSize = [self.mapSize[0]/gridNumber[0],self.mapSize[1]/gridNumber[1]]

    def GetGridPos(self,location):
        
        #return  [round(location[0])//self.gridSize[0],round(location[1])//self.gridSize[1]]
        #return  [ceil(location[0])//self.gridSize[0],ceil(location[1])//self.gridSize[1]]
        return Vector2(ceil(location[0])//self.gridSize[0],ceil(location[1])//self.gridSize[1])
    def GetWorldLoc(self,gridLoc):
        return Vector2(gridLoc[0]*self.gridSize[0],gridLoc[1]*self.gridSize[1])

