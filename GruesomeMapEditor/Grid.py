import Data.Constant

class Grid:
    def __init__(self):
        # offset to put the grid 0 at the end of the left panel
        self.x_offset = Data.Constant.LEFT_SURFACE_SIZE[0]// Data.Constant.GRID_SIZE[0]


    def GetMainGridLoc(self,world_location):
        '''Substract X number from offset to start the 0 after the left panel'''
        return [(world_location[0]// Data.Constant.GRID_SIZE[0]) - self.x_offset ,world_location[1]// Data.Constant.GRID_SIZE[1]]


    def GetMainWorldLoc(self,grid_location): 
        '''Add offset to world position.. since we dont want the side surface to contain grid'''
        return [(grid_location[0] + self.x_offset) * Data.Constant.GRID_SIZE[0],grid_location[1] * Data.Constant.GRID_SIZE[1]]

    def Get_gridPos(self,location):
        return [location[0]//Data.Constant.GRID_SIZE[0],location[1]//Data.Constant.GRID_SIZE[1]]
    
    def GetWorldLoc(self,gridLoc):
        return [gridLoc[0]*Data.Constant.GRID_SIZE[0],gridLoc[1]*Data.Constant.GRID_SIZE[1]]

    def MapOffset(self,mapLoc,tileLoc):
        pass