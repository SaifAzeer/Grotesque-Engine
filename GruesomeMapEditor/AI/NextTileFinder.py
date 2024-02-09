'''Find the next tile type'''
from operator import le, ne
from select import select
from Tiles import Tiles
from typing import List
from Data.TileType import Tile_name_type, TileType


class NextTileFinder:
    def __init__(self):
        self.l_checked = []
        self.l_positions = []

        self.previous = None # not really previous

        self.hor_neighbour = [(1,0),(-1,0)]
        self.ver_neighbour = [(0,1),(0,-1)]
        self.l_counter = 0

    def Arrange_tiles(self,l_selectedTiles,d_border):
        '''check if there is a tile next to this one .. and select appropriate tile'''
        l_updatedTiles = []
        for i in l_selectedTiles:
            self.l_counter += 1
            for j in l_selectedTiles:          
                # top --- going right
                if [i.gridPos[0] + 1,i.gridPos[1]] == j.gridPos and [i.gridPos[0] + 1,i.gridPos[1]] not in self.l_checked:                    
                    if self.previous == None:
                        self.previous = Tile_name_type.top
                    elif self.previous == Tile_name_type.top:
                        self.previous = Tile_name_type.top
                    elif self.previous == Tile_name_type.left:
                        self.previous = Tile_name_type.top_left
                    elif self.previous == Tile_name_type.top_left:
                        self.previous = Tile_name_type.top
                    #elif self.previous == Tile_name_type.right:
                    #    self.previous = Tile_name_type.bot_left
                    else: # in something went wrong.. force it to have the right tile
                        self.previous = Tile_name_type.top

                    self.Update_tile_image(i,d_border)
                 # down  --- going left
                elif [i.gridPos[0] - 1,i.gridPos[1]] == j.gridPos and [i.gridPos[0] - 1,i.gridPos[1]] not in self.l_checked:           
                    if self.previous == None:
                        self.previous = Tile_name_type.bot                   
                    elif self.previous == Tile_name_type.right:
                        self.previous = Tile_name_type.bot_right
                    elif self.previous == Tile_name_type.bot_right:
                        self.previous = Tile_name_type.bot
                    elif self.previous == Tile_name_type.bot:
                        self.previous = Tile_name_type.bot
                    else:
                        self.previous = Tile_name_type.bot  
                        
                    self.Update_tile_image(i,d_border)

                # right ___ going down
                elif [i.gridPos[0],i.gridPos[1] + 1] == j.gridPos and [i.gridPos[0],i.gridPos[1] + 1] not in self.l_checked: 
                    if self.previous == None:
                        self.previous = Tile_name_type.right
                    elif self.previous == Tile_name_type.top:
                        self.previous = Tile_name_type.top_right
                    elif self.previous == Tile_name_type.top_right:
                        self.previous = Tile_name_type.right
                    elif self.previous == Tile_name_type.right:
                        self.previous = Tile_name_type.right
                    #elif self.previous == Tile_name_type.left:
                    #    self.previous = Tile_name_type.top_left
                    else:
                        self.previous = Tile_name_type.right
                    
                    self.Update_tile_image(i,d_border)

                # left --- going up
                elif [i.gridPos[0],i.gridPos[1] - 1] == j.gridPos and [i.gridPos[0],i.gridPos[1] - 1] not in self.l_checked: 
                    if self.previous == None:
                        self.previous = Tile_name_type.left                    
                    elif self.previous == Tile_name_type.bot:
                        self.previous = Tile_name_type.bot_left
                    elif self.previous == Tile_name_type.bot_left:
                        self.previous = Tile_name_type.left
                    elif self.previous == Tile_name_type.left:
                        self.previous = Tile_name_type.left

                    else:
                        self.previous = Tile_name_type.left
                    
                    self.Update_tile_image(i,d_border)

                else:                  
                    continue

            # set last tile from list

            if len(l_selectedTiles) == self.l_counter and self.l_counter >=3:             
                if l_selectedTiles[-2] == Tile_name_type.left:
                   if l_selectedTiles[0] == Tile_name_type.top:
                        self.previous = Tile_name_type.left
                        
                self.Update_tile_image(l_selectedTiles[-1],d_border)

            l_updatedTiles.append(i)

        l_selectedTiles[0].image = d_border[Tile_name_type.top_left]

            
        self.l_checked= []
        self.l_counter = 0
        return l_updatedTiles



    def Set_image_tracker(self,previous,tile,image):
        self.previous = previous
        tile.image = image

    def Update_tile_image(self,tile,d_border):
        #change image here
        tile.image = d_border[self.previous]
        tile.Tile_name_type_direction = self.previous
        self.l_checked.append(tile.gridPos)  

    
    def Order_selected_tiles(self,firstTile,l_selectedTiles):
        ''' order tile in list to make it a continuous line in grid'''
        l_ordered_selected_tiles = []
        l_ordered_selected_tiles.append(firstTile)
        neighbour = l_selectedTiles[0]
        for i in range(len(l_selectedTiles)-1):
            for j in l_selectedTiles:
                if self.Find_neighbour(neighbour.gridPos,j.gridPos,"horizontal"):
                    if j.gridPos not in l_ordered_selected_tiles:
                        neighbour = j
                        l_ordered_selected_tiles.append(neighbour)
                        break
                         
                # look for neighbour vertically if horizontal is not found                          
                if self.Find_neighbour(neighbour.gridPos,j.gridPos,"vertical"):
                    if j.gridPos not in l_ordered_selected_tiles:
                        neighbour = j
                        l_ordered_selected_tiles.append(neighbour)
                        break 

        return l_ordered_selected_tiles


    def Find_neighbour(self,tilePos,possile_neighbour,dir):
        if dir == "horizontal":
            for i in self.hor_neighbour:
                if tilePos[0] + i[0] == possile_neighbour[0] and tilePos[1] + i[1] == possile_neighbour[1]:
                    return True
        elif dir == "vertical":
            for i in self.ver_neighbour:
                if tilePos[0] + i[0] == possile_neighbour[0] and tilePos[1] + i[1] == possile_neighbour[1]:
                    return True
        return False    


    # ----------------------------------------------------------------------------------------------
    #   NOT IN USE.. MAYBE BETTER WAY TO HANDLE RE ARRANGING AI
    # ----------------------------------------------------------------------------------------------
    def ArrangeTile_2(self,l_selectedTiles,d_border):
        curr_x = l_selectedTiles[0].gridPos[0]
        curr_y = l_selectedTiles[1].gridPos[1]
        for i in l_selectedTiles:
            next_x = i.gridPos[0]
            next_y = i.gridPos[1]
            if curr_y == next_y and next_x == curr_x +1:
                #right
                print(i.gridPos)
            elif curr_y == next_y and next_x == curr_x -1:
                #left
                print(i.gridPos)
            elif next_y == curr_y -1 and next_x == curr_x :
                #up
                print(i.gridPos)
            elif next_y == curr_y - 1 and next_x == curr_x:
                #down
                print(i.gridPos)
                