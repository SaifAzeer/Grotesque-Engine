'''Change Data.Constant.ROOTPOSITION to images root folder position '''

import json
from os import getcwd
from typing import List
import pygame
from sys import exit
import Data.Constant
from Grid import Grid
from Data.Constant import GRID_SIZE,GRID_NUMBER
from Data.Constant import LEFT_SURFACE_SIZE,MAIN_SURFACE_SIZE
from MyEncoder import MyEncoder, NoIndent,OneDictPerLine
from Tiles import Tiles
from Data.TileType import TileType
from UI.UIManager import UIManager
from Data.Global import Global
from AI import NextTileFinder
from GruesomeMapEditor.AI import floodFill
from UI.Button import Button

#import numpy as np

class GruesomeMapMaker:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode(Data.Constant.DISPLAY_SIZE)
        pygame.display.set_caption('Gruesome Map Editor')

        self.left_surface = pygame.Surface(Data.Constant.LEFT_SURFACE_SIZE)
        self.left_surface.fill((80,80,80))

        self.main_surface = pygame.Surface(Data.Constant.MAP_SIZE)
        self.main_surface.fill((50,50,50))
        self.main_surface_rect = self.main_surface.get_rect()

        self.background_image = pygame.image.load("background.png")
        self.background_image = pygame.transform.scale(self.background_image,MAIN_SURFACE_SIZE)
        self.background =  pygame.Surface(Data.Constant.MAIN_SURFACE_SIZE)
        #self.background.fill((200,200,200))
        self.mouseDown = False # use to move map 2
        self.background_position = [Data.Constant.LEFT_SURFACE_SIZE[0],0] 
        self._font = pygame.font.SysFont('arial', 15)
        
        self.d_action_rect = {} #collider name : list of action rectangles to render
        self.actionName = "empty"

        self.main_grid = Grid()
        self.side_grid = Grid()

        self.l_tiles = []
        self.l_selectedTiles = []
        self.l_tile_preview = []

        self.layer_1_tiles = []
        self.layer_2_tiles = []
        self.layer_3_tiles = []
        # map for each layer.. tile id at each loc
        #self.map_1 = [[0 for i in range(Data.Constant.GRID_NUMBER[0])] for j in range(Data.Constant.GRID_NUMBER[0])]
        #self.map_2 = [[0 for i in range(Data.Constant.GRID_NUMBER[0])] for j in range(Data.Constant.GRID_NUMBER[0])]       
        #self.map_3 = [[0 for i in range(Data.Constant.GRID_NUMBER[0])] for j in range(Data.Constant.GRID_NUMBER[0])]       
        self.map_1 = [[0 for i in range(GRID_NUMBER[0])] for j in range(GRID_NUMBER[1])]
        self.map_2 = [[0 for i in range(GRID_NUMBER[0])] for j in range(GRID_NUMBER[1])]
        self.map_3 = [[0 for i in range(GRID_NUMBER[0])] for j in range(GRID_NUMBER[1])]
        
        #image used for each layer.. use to offload to json
        self.layer_1_image = {}
        self.layer_2_image = {}
        self.layer_3_image = {}

        self.uiManager = UIManager()
        self.uiManager.explorer.currFolderPath= getcwd()
        self.tileAi = NextTileFinder.NextTileFinder()
        self.floodFill = floodFill.FloodFill()
        
        self.displayFocus = "left" # if we click on main display or side one.. focus it
        self.currentTile_image =None
        self.currentTile = None
        if len(self.uiManager.d_tileSet)>0:
            self.currentTile_image = self.uiManager.d_tileSet[1]
            self.currentTile = Tiles(self.main_grid.GetMainGridLoc(pygame.mouse.get_pos()),TileType.image,pygame.mouse.get_pos(),0,self.currentTile_image)

        
        self.middle_mouse_down_pos = None
        self.middle_mouse_down = False
        self.selection_rectangle_width = 0
        self.selection_rectangle_height = 0
        self.sr_topLeft  = [0,0]

        # changing tile by pressing numbers
        self.is_shift_down = False
        self.multiple_number_pressed : str = ""
        self.numberPressed = 0

        self.b_add_line = False
        self.mouse_click_pos = [0,0] # for line preview with 'L' is pressed
        # moving the map.. tracker to reset the map
        self.world_mouse_click = None
        self.previousMousePos = 0 # use when moving the map with mouse

        self.mapMovement = [0,0]
        # use to calculate real position after  mouse button is released and gridPos is calculated and pos is calculated
        # from gridLoc
        self.tile_map_movement = [0,0]
        self.mousePos = [0,0]

        self.btn_folder_click_return :str 

    def print_in_grid(self,maps):
        # this function will print the contents of the array
        for y in range(len(maps)):
            for x in range(len(maps[0])):
	            # value by column and row
                print(maps[y][x], end=' ')
                if x == len(maps[0])-1:
                    # print a visited_val line at the end of each row
                    print('\n') 

    def delete_tile(self,l_del) -> None:
        for i in l_del:
            if Global.currentLayer ==1 :
                if i in self.layer_1_tiles: # if no more tile with image we deleted.. not not add in json           
                    self.map_1[i.original_gridPos[1]][i.original_gridPos[0]] = 0
                    self.layer_1_tiles.remove(i)
            
            elif Global.currentLayer ==2 :
                if i in self.layer_2_tiles:
                    self.map_2[i.gridPos[1]][i.gridPos[0]] = 0
                    self.layer_2_tiles.remove(i)
            
            elif Global.currentLayer ==3 :
                if i in self.layer_3_tiles:
                    self.map_3[i.gridPos[1]][i.gridPos[0]] = 0
                    self.layer_3_tiles.remove(i)

            if i in l_del:            
                self.l_tiles.remove(i)
        self.l_selectedTiles = []


    def delete_replace_tile_from_list(self,tileList,to_delete_list) ->List[Tiles]:
        '''compare and delete items in to delete list from another list'''
        l_result = []
        for i in to_delete_list:
            if i in tileList:
                l_result.append(i)
        self.delete_tile(l_result)
        
        return l_result



    def delete_tile_from_list(self,del_list) -> None:
        l_result = []
        for i in del_list:
            if i in self.l_tiles:
                l_result.append(i)
        for i in l_result:
            self.l_tiles.remove(i)


    def number_pressed(self,event):
        '''change tileset selected when number is pressed.. based on order of tiles'''
        isNumpressed = True
        if event.key == pygame.K_0:
            self.numberPressed = 0

        elif event.key == pygame.K_1:
            self.numberPressed = 1
                    
        elif event.key == pygame.K_2:
            self.numberPressed = 2

        elif event.key == pygame.K_3:
            self.numberPressed = 3

        elif event.key == pygame.K_4:
            self.numberPressed = 4

        elif event.key == pygame.K_5:
            self.numberPressed = 5

        elif event.key == pygame.K_6:
            self.numberPressed = 6

        elif event.key == pygame.K_7:
            self.numberPressed = 7

        elif event.key == pygame.K_8:
            self.numberPressed = 8

        elif event.key == pygame.K_9:
            self.numberPressed = 9
        
        else:
            # fail safe.. make sure we do not reach switch tile below when button pressed randomly
            isNumpressed = False
        
        if self.is_shift_down:
            self.multiple_number_pressed += str(self.numberPressed)
            
        if isNumpressed:
            if self.uiManager.Switch_tile(self.numberPressed):
                self.change_tile(self.uiManager.Switch_tile(self.numberPressed))


    def create_tile(self,pos,img,types = TileType.image ) -> Tiles:
        '''create a new tile and add it to global list for display'''
        #self.currentTile = Tiles(gridPos,types,pos,img)
        id = 0
        for ID, name in self.uiManager.d_tileSet.items():
            if name == img:
                # calculate position even when map have movec
                # self.tile_map_movement is -ve then going right and +ve when going left. so we * by -ve 1
                position = [pos[0] + self.tile_map_movement[0] *-1,pos[1]+ self.tile_map_movement[1]*-1]
               
                _gridPos = self.main_grid.GetMainGridLoc(position) 
                tile = Tiles(_gridPos,types,position,ID,img)
                tile.originalPos = position    
                tile.Get_pos_by_grid(self.main_grid,self.tile_map_movement) # place grid at the right place when map move
          
                if Global.currentLayer == 1:
                    self.Setup_layer_tile(tile,ID,_gridPos,self.layer_1_tiles,self.map_1)

                elif Global.currentLayer == 2:
                    self.Setup_layer_tile(tile,ID,_gridPos,self.layer_2_tiles,self.map_2)

                elif Global.currentLayer == 3:
                    self.Setup_layer_tile(tile,ID,_gridPos,self.layer_3_tiles,self.map_3)

                self.l_tiles = self.layer_1_tiles + self.layer_2_tiles + self.layer_3_tiles   
        
                return tile
            


    def create_tile_gridPos(self,pos,img,types = TileType.image) -> Tiles:
        '''create a new tile and add it to global list for display with gridPosition given'''
        #self.currentTile = Tiles(gridPos,types,pos,img)
        id = 0
        for ID, name in self.uiManager.d_tileSet.items():
            if name == img:
                tile = Tiles(pos,types,self.main_grid.GetMainWorldLoc(pos),ID,img)
                tile.originalPos = self.side_grid.GetMainWorldLoc(pos)               
                tile.Get_pos_by_grid(self.main_grid,self.tile_map_movement) # place grid at the right place when map move

                if Global.currentLayer == 1:
                    self.Setup_layer_tile(tile,ID,pos,self.layer_1_tiles,self.map_1)

                elif Global.currentLayer == 2:
                    self.Setup_layer_tile(tile,ID,pos,self.layer_2_tiles,self.map_2)

                elif Global.currentLayer == 3:
                    self.Setup_layer_tile(tile,ID,pos,self.layer_3_tiles,self.map_3)

                self.l_tiles = self.layer_1_tiles + self.layer_2_tiles + self.layer_3_tiles   
                return tile
            
    def Create_groupTiles(self):
        pass

    def UpdateMap(self,tile,id,pos):
        '''problems when calling.. need to investigate'''
        if Global.currentLayer == 1:
                        
            self.Setup_layer_tile(tile,id,pos,self.layer_1_tiles,self.map_1)

        elif Global.currentLayer == 2:
            self.Setup_layer_tile(tile,id,pos,self.layer_2_tiles,self.map_2)

        elif Global.currentLayer == 3:
            self.Setup_layer_tile(tile,id,pos,self.layer_3_tiles,self.map_3)

        self.l_tiles = self.layer_1_tiles + self.layer_2_tiles + self.layer_3_tiles   
        return tile


    def Setup_layer_tile(self,tile,ID,gridPos,l_tiles,map):
        '''use by create tile Func. to setup tiles.. ie: add in map list and tile list'''
        #add only witin main surface
        if gridPos[0] > GRID_NUMBER[0] or gridPos[1] > GRID_NUMBER[1] or gridPos[0] < 0 or gridPos[1] < 0:
            return    # check if we are checking within the map size... gridNumber and map size is same
        if tile not in l_tiles:   
            map[gridPos[1]][gridPos[0]] = ID
            l_tiles.append(tile)
    

    def Check_if_within_mainMap(self,mousePOs):
        """check if mouse are within map boundary and not  background"""
        pass
            

    def change_tile(self,new_img : str):
        ''' selecting new tile from left layout'''
        self.currentTile_image = new_img #swap tile
        self.currentTile.Load_image(self.currentTile_image)


    #--------------------------------------------------------------------------------------
    def calculate_selection_rectangle(self) -> List[int]:
        '''create rectangle when middle mouse click'''
        #if self.middle_mouse_down:
        #get mouse locations and calculate rect size to draw rect
        self.selection_rectangle_width  = self.mousePos[0] - self.middle_mouse_down_pos[0]
        self.selection_rectangle_height = self.mousePos[1] - self.middle_mouse_down_pos[1]

        if self.selection_rectangle_width < 0 and self.selection_rectangle_height >= 0:
            self.selection_rectangle_width = abs(self.selection_rectangle_width)    
            self.sr_topLeft = [self.mousePos[0],self.middle_mouse_down_pos[1]]

        elif self.selection_rectangle_height < 0 and self.selection_rectangle_width >=  0:
            self.selection_rectangle_height = abs(self.selection_rectangle_height)
            self.sr_topLeft = [self.middle_mouse_down_pos[0],self.mousePos[1]]

        elif self.selection_rectangle_width <0 and self.selection_rectangle_height <0:
            self.selection_rectangle_width = abs(self.selection_rectangle_width)    
            self.selection_rectangle_height = abs(self.selection_rectangle_height)
            self.sr_topLeft = [self.mousePos[0],self.mousePos[1]]

        else:                
            self.sr_topLeft= [self.middle_mouse_down_pos[0],self.middle_mouse_down_pos[1]]

        return [self.sr_topLeft,self.selection_rectangle_width,self.selection_rectangle_height]
    
#----------------------------------------------------------------
# Action Editor
#----------------------------------------------------------------

    def Create_action_rectangle(self,rect_name:str) -> None:
        '''Create rectangle that will be used as colliders in action editor'''    
        if self.uiManager.is_actionEditor_on: # if we are in the action editor menu   
            rect_dimentions = self.calculate_selection_rectangle()      
            rect_dimentions = self.Snap_action_rectangle_on_grid(rect_dimentions) # top left
            rect_dimentions.append(self._font.render(rect_name,True,(100,100,100)))
            # add multiple rectangle with same name 
            if rect_name in self.d_action_rect:
                self.d_action_rect[rect_name].append(rect_dimentions)
            else:
                l_newRect = [rect_dimentions]
                self.d_action_rect[rect_name] = l_newRect


    def Snap_action_rectangle_on_grid(self,rect_dimention)-> list[int]:
        '''snap rectangle to grid , recalculate width and height based on amount of grid'''
        topLeftGrid = self.main_grid.GetMainGridLoc( rect_dimention[0])
        horTileAmount =rect_dimention[1] // GRID_SIZE[0]
        width = horTileAmount * GRID_SIZE[0]
        verTileAmount =rect_dimention[2] // GRID_SIZE[1]
        height = verTileAmount * GRID_SIZE[1]
        return [self.main_grid.GetMainWorldLoc(topLeftGrid),width, height]
    

    def Delete_action_Rectangle(self)-> None:
        for i,j in self.d_action_rect.items(): 
            for rectangle in j: # check if we click inside the rectangle
                if self.mousePos[0] > rectangle[0][0] and self.mousePos[0] < rectangle[0][0] + rectangle[1]:
                    if self.mousePos[1] > rectangle[0][1] and self.mousePos[1] < rectangle[0][1] + rectangle[2]:
                        j.remove(rectangle)
                        if len(j)==0: # remove keys from dictionary if there are no more action rectangles
                            self.d_action_rect.pop(i)
                        return
#----------------------------------------------------------------


    def Select_tiles(self,topLeft,size) -> None:   
        ''' tiles selected in rectangle select'''    
        # when moving box.. unselect tiles outside box.. and render normally
        if Global.currentLayer == 1:
            self.Find_selected_tiles(self.layer_1_tiles,topLeft,size)
        elif Global.currentLayer == 2:
            self.Find_selected_tiles(self.layer_2_tiles,topLeft,size)
        elif Global.currentLayer == 3:
            self.Find_selected_tiles(self.layer_3_tiles,topLeft,size)

        self.l_tiles = self.layer_1_tiles + self.layer_2_tiles + self.layer_3_tiles
        

    def Find_selected_tiles(self,layer,topLeft,size):
        '''Use in Select tiles to find and add in l_selected tiles'''
        for i in layer: 
            if self.is_shift_down == False:
                if i in self.l_selectedTiles:              
                    self.l_selectedTiles.remove(i)                
            if i.position[1] <= topLeft[1] + size[1] and i.position[1] >= topLeft[1]:
                if  i.position[0] <= topLeft[0] + size[0] and i.position[0] >= topLeft[0]:         
                    if i not in self.l_selectedTiles: # prevent dupplication when pressing shift to add more
                        self.l_selectedTiles.append(i)
                        self.tileAi.l_positions.append(i.gridPos)
            # if ALT is pressed.. remove tiles from selected
    


    def add_tile_in_line(self,start,mousePos):
        '''calculate the tiles location between a starting position to the mouse position'''
        l_tile = []
        if self.mouse_click_pos == None:
            return
        if start[0] == mousePos[0]:
            if start[1] > mousePos[1]:
                for i in range(start[1] - mousePos[1]):
                    l_tile.append([start[0],start[1] - i]) # line top
            else:
                for i in range(mousePos[1] - start[1]):
                    l_tile.append([start[0],start[1] + i]) # line down
        
        elif start[1] == mousePos[1]:
            if start[0] > mousePos[0]:
                for i in range(start[0] - mousePos[0]):  # line left
                    l_tile.append([start[0] - i,start[1]])
            else:
                for i in range(mousePos[0] - start[0]):  # line right
                    l_tile.append([start[0] + i,start[1]])
            
        return l_tile


    def preview_line_tile(self,start,mousePos):
        ''' constantly preview the tile as long as it exist'''
        self.l_tile_preview = []
        l_tile = self.add_tile_in_line(start,mousePos)
        if self.mouse_click_pos == None:
            return

        for i in l_tile:
            for j in self.l_tile_preview:
                if j.gridPos == i:
                    break    
            tile = Tiles(i,TileType.image,self.main_grid.GetMainWorldLoc(i),0,self.currentTile_image)
            if tile not in self.l_tile_preview:
                self.l_tile_preview.append(tile)

        # make sure the first tile always appear even if the list is empty.. 
        if self.l_tile_preview == []:      
            tile = Tiles(self.mouse_click_pos,TileType.image,self.main_grid.GetMainWorldLoc(self.mouse_click_pos),0,self.currentTile_image)
            if tile not in self.l_tile_preview:
                self.l_tile_preview.append(tile)


    #   MAP MOVEMENT ----------------------------------------------------------------------------
    def Move_map(self,mousePos):
        ''' move map and everything on the map''' 
        if self.mousePos != self.previousMousePos:
            self.mapMovement[0] += self.mousePos[0]- self.world_mouse_click[0]
            self.mapMovement[1] += self.mousePos[1]- self.world_mouse_click[1]
            for i in self.l_tiles:                        
                if self.mapMovement[0] !=0:                 
                    i.position[0] += self.mousePos[0]- self.world_mouse_click[0] 
                if self.mapMovement[1] !=0:
                    i.position[1] += self.mousePos[1]- self.world_mouse_click[1] 

            if self.mouseDown: # move map background surface
                self.background_position[1] += self.mousePos[1] - self.world_mouse_click[1]
                self.background_position[0] += self.mousePos[0] - self.world_mouse_click[0]

            self.world_mouse_click = self.mousePos
            self.previousMousePos = self.mousePos


    def Reset_map_locaion(self):
        '''put map back to its original location'''
        self.mapMovement = [0,0]
        self.tile_map_movement = [0,0]
        for i in self.l_tiles:                        
            i.position =  i.originalPos
            i.Get_pos_by_grid(self.main_grid,self.tile_map_movement)
        
        self.background_position = [Data.Constant.LEFT_SURFACE_SIZE[0],0] 
        

    def Calc_map_expansion(self):
        '''when moving map with mouse.. map will expand.. get most right tile and most left tile'''
        maxHor = max(node.gridPos[0] for node in self.l_tiles)
        maxVer = max(node.gridPos[1] for node in self.l_tiles)
        if maxHor < Data.Constant.GRID_NUMBER[0]: maxHor = Data.Constant.GRID_NUMBER[0]
        if maxVer < Data.Constant.GRID_NUMBER[1]: maxVer = Data.Constant.GRID_NUMBER[1]
        return (maxHor,maxVer)

#-------------------------------------------------------------------------------------------------
    def Update(self):
        while True:  
            self.uiManager.Update()
            self.Events()
            self.Render()

            pygame.display.update()


    #--------------------------------------------------------------------------------------
    
    def Render(self):
        self.mousePos = pygame.mouse.get_pos()
        self.background.blit(self.background_image,(0,0))
        self.main_surface.fill((50,50,50))
        #self.left_surface.fill((80,80,80))

        self.display.blit(self.background,(Data.Constant.LEFT_SURFACE_SIZE[0],0))       
        self.display.blit(self.main_surface,self.background_position)

        # tile preview
        if self.currentTile:
            self.currentTile.Mouse_tile_preview(self.display,self.main_grid,self.main_grid.GetMainGridLoc(self.mousePos))
        # tile line preview 
        if self.b_add_line:        
            self.preview_line_tile(self.mouse_click_pos,self.main_grid.GetMainGridLoc(self.mousePos))           
            for i in range(len(self.l_tile_preview)):
                if i == 0:
                    self.l_tile_preview[0].Render_other_colour(self.display,self.main_grid,(140,230,220))
                else:
                    self.l_tile_preview[i].Render_other_colour(self.display,self.main_grid)

        # render all tiles placed
        for i in self.l_tiles:
            if i in self.l_selectedTiles:
                i.Render_other_colour(self.display,self.main_grid)
            else:
                i.Render(self.display) 

        # draw selection rectangle
        pygame.draw.rect(self.display,(20,20,20),pygame.Rect(self.sr_topLeft [0],self.sr_topLeft[1],self.selection_rectangle_width,self.selection_rectangle_height),2)
        for i,k in self.d_action_rect.items(): 
            for j in k: 
                pygame.draw.rect(self.display,(20,20,20),pygame.Rect(j[0][0],j[0][1],j[1],j[2]),2)
                self.display.blit(j[3],j[0])

        self.display.blit(self.left_surface,(0,0))
         # render explorer when left click
        self.uiManager.Render(self.display)
        self.uiManager.Render_on_left_surface(self.display)
        pygame.display.update()


    #--------------------------------------------------------------------------------------
    def Events(self):
        #  add tile when left click and remove when right click-----------------------
        mousePressed = pygame.mouse.get_pressed()
        keyPressed = pygame.key.get_pressed()
        # select another tile from left panel
        onClick_return = self.uiManager.OnClick()

        #preview tiles
        if type(onClick_return) == Tiles:
            self.currentTile = onClick_return
            self.currentTile_image = onClick_return.image
            self.currentTile.Load_image(self.currentTile_image)  # update preview Image

        #--------------------------------------------------------------------------------------------------------------
        #                                               MOUSE KEY PRESSED 
        if mousePressed[0] == True:  #left mouse click
            if self.is_shift_down: # move map
                if self.world_mouse_click == None: self.world_mouse_click = self.mousePos  
                self.Move_map(self.mousePos)
            else:
                self.Add_tiles()
       
        if mousePressed[1] == True: # middle button -> draw rect   
            #self.uiManager.show_file_explorer = False
            self.middle_mouse_down = True   
            self.calculate_selection_rectangle()       
            
            self.Select_tiles(self.sr_topLeft,[self.selection_rectangle_width,self.selection_rectangle_height])           
        else:
            self.middle_mouse_down_pos = self.mousePos
            self.middle_mouse_down = False    
            # remove selection rectangle
            self.selection_rectangle_width = 0
            self.selection_rectangle_height = 0

        if mousePressed[2] == True:
            if self.uiManager.is_actionEditor_on:
                self.Delete_action_Rectangle()
            if keyPressed[pygame.K_LALT]: 
                self.remove_tile()
        #-----------------------------------------------------------------------------------------------------------
   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:      
                self.mouseDown = True
                self.btn_folder_click_return = self.uiManager.ButtonClicked(self.mousePos)
                if self.uiManager.is_actionEditor_on: # check if action editor textbox is clicked
                    self.uiManager.textBox.Mouse_click(event.pos)
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.middle_mouse_down:
                    self.Create_action_rectangle(self.actionName)
                    if self.uiManager.show_file_explorer:
                        self.uiManager.Select_tiles()
                self.mouseDown = False
                self.world_mouse_click = None
                self.tile_map_movement = self.main_grid.GetMainGridLoc(self.mapMovement)                 
                self.tile_map_movement = self.main_grid.GetMainWorldLoc(self.tile_map_movement)
                self.mapMovement = self.tile_map_movement
                # snap background map on grid
                backgroundPos = self.main_grid.GetMainGridLoc(self.background_position)
                self.background_position = self.main_grid.GetMainWorldLoc(backgroundPos)

                for i in self.l_tiles:
                    i.Get_pos_by_grid(self.main_grid,self.tile_map_movement)
               
            elif event.type == pygame.KEYDOWN:
                self.number_pressed(event)
                self.uiManager.Update_textBox(event)

                if self.uiManager.is_actionEditor_on:
                    self.actionName = self.uiManager.textBox.textResult
                    if self.actionName == "": self.actionName = "empty"
                    return
                if event.key == pygame.K_ESCAPE:    
                    self.l_selectedTiles = []
                    self.tileAi.l_positions = []
                
                elif event.key == pygame.K_d:
                    self.delete_tile(self.l_selectedTiles) 

                elif event.key == pygame.K_l:                   
                    if self.b_add_line == False:
                        self.b_add_line = True
                        self.mouse_click_pos = None  
                    else:
                        self.b_add_line = False             
                
                elif event.key == pygame.K_RETURN:                   
                    # find the start of the square.. the top left from the list
                        self.Start_order_selected_tiles()                      
                        self.Start_Tile_order_AI()

                elif event.key == pygame.K_f:
                    #loc of mouse on main map with map movement consideration
                    start_fill_loc = self.main_grid.GetMainGridLoc([self.mousePos[0] + self.tile_map_movement[0] *-1,self.mousePos[1]+ self.tile_map_movement[1]*-1])              
                    self.floodFill.Start(self.map_1,start_fill_loc,self.currentTile.ID)
                    for i in self.floodFill.addedloc: #added loc give loc from map direcly to we get gridPos directly
                        self.create_tile_gridPos(i,self.currentTile_image)
  
                elif event.key == pygame.K_r:
                    self.Reset_map_locaion()

                elif event.key == pygame.K_LSHIFT:
                    self.is_shift_down = True

                elif event.key == pygame.K_SPACE:
                    self.Save()
                   
                elif event.key == pygame.K_DOWN:
                    for i in self.l_tiles:
                        i.gridPos[1]-= 1
                    self.uiManager.explorer.scroll_area.ScrollUp()
                
                elif event.key == pygame.K_UP:
                    for i in self.l_tiles:
                        i.gridPos[1]+= 1
                    self.uiManager.explorer.scroll_area.ScrollDown()
                       
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    self.is_shift_down = False
                    # change tile set by number using double digit number
                    if len(self.multiple_number_pressed) > 0:
                        if self.uiManager.Switch_tile(int(self.multiple_number_pressed)):
                            self.change_tile(self.uiManager.Switch_tile(int(self.multiple_number_pressed)))
                          
                    self.multiple_number_pressed = ""

        

                        
    #--------------------------------------------------------------------------------------
    #KEYPRESSED
    def remove_tile(self)->None:
        '''remove tile from map when pressing left ALT and right click'''  
        #self.uiManager.show_file_explorer = False
        self.b_add_line = False
        removePos = self.main_grid.GetMainGridLoc(pygame.mouse.get_pos()) 
        # calculate remove pos plus map movement and check for removed tiles. or itll not be removed   
        if removePos in self.l_tiles:    
            for i in self.l_tiles:
                if i.gridPos == removePos:
                    if Global.currentLayer == 1:
                        if i in self.layer_1_tiles:
                            self.layer_1_tiles.remove(i)
                            self.map_1[i.original_gridPos[1]][i.original_gridPos[0]] = 0
                    elif Global.currentLayer == 2:
                        if i in self.layer_2_tiles:
                            self.layer_2_tiles.remove(i)
                            self.map_2[i.original_gridPos[1]][i.original_gridPos[0]] = 0
                    elif Global.currentLayer == 3:
                        if i in self.layer_3_tiles:
                            self.layer_3_tiles.remove(i)
                            self.map_3[i.original_gridPos[1]][i.original_gridPos[0]] = 0

                    if i in self.l_selectedTiles:
                        self.l_selectedTiles.remove(i)
                    break
        self.l_tiles = self.layer_1_tiles + self.layer_2_tiles + self.layer_3_tiles 



    def Add_tiles(self)-> None:
        if self.uiManager.show_file_explorer == False:
            #if self.btn_folder_click_return == "folder changed":
            #    if len(self.uiManager.d_tileSet)>0:
            #        self.currentTile_image = self.uiManager.d_tileSet[1]
                
            #add tiles
            try:      
                if self.b_add_line == False:
                    #print(self.uiManager.d_tileSet)
                    self.currentTile = self.create_tile(list(self.mousePos),self.currentTile_image)
                else:         
                    for i in self.l_tile_preview:
                        self.create_tile(self.main_grid.GetMainWorldLoc(i.gridPos),self.currentTile_image)
                    self.mouse_click_pos = self.main_grid.GetMainGridLoc(self.mousePos)
                    
            except FileNotFoundError:
                self.currentTile_image = None


    # ____________________________________________________________AI ________________________________________________________
    def Start_order_selected_tiles(self)->None:
        '''Find top left of selected tiles and order it'''
        if len(self.l_selectedTiles) >0:
            # make sure tile are in proper sequence to get the order right in "Order_selected_tiles". order by  y first
            self.l_selectedTiles =  sorted(self.l_selectedTiles , key=lambda k: [k.gridPos[1], k.gridPos[0]])
            #topLeft =  np.min(np.min(self.l_selectedTiles, axis=0), axis=0).gridPos
            topLeft = self.l_selectedTiles[0].gridPos                        

            topLeftIndex = 0
            # look for top left tile
            for i in range(len(self.l_selectedTiles)):
                if self.l_selectedTiles[0].gridPos[0] < topLeft[0]:
                    topLeft[0] = self.l_selectedTiles[0].gridPos
                    topLeftIndex = i
                if self.l_selectedTiles[1].gridPos[1] < topLeft[1]:
                    topLeft[1] = self.l_selectedTiles[1].gridPos
                    topLeftIndex = i
            self.l_selectedTiles_order = self.tileAi.Order_selected_tiles(self.l_selectedTiles[topLeftIndex],self.l_selectedTiles)  



    def Start_Tile_order_AI(self)-> None:
        if len(self.l_selectedTiles_order) > 0:
            # start AI               
            l_new_tiles = self.tileAi.Arrange_tiles(self.l_selectedTiles_order,self.uiManager.d_border_tile)       
            # update list
            self.l_selectedTiles = self.l_selectedTiles + l_new_tiles
            self.Add_tile_in_list(l_new_tiles)
            # update map
            for i in self.l_tiles:
                #print(i.image)
                for ID, name in self.uiManager.d_tileSet.items():
                    if name == i.image:
                        if Global.currentLayer == 1:
                            self.map_1[i.original_gridPos[1]][i.original_gridPos[0]] = ID
                        elif Global.currentLayer == 2:
                            self.map_2[i.original_gridPos[1]][i.original_gridPos[0]] = ID
                        elif Global.currentLayer == 3:
                            self.map_3[i.original_gridPos[1]][i.original_gridPos[0]] = ID
                i.Load_image(i.image)  

            

    def Add_tile_in_list(self,l_toAdd):
        '''add tiles and remove dupplicate'''
        for i in l_toAdd:
            if i not in self.l_tiles:
                self.l_tiles.append(i)

    def Update_action_dictionary_before_save(self):
        '''remove surface from dictionary value'''
        new_action_dictionary = self.d_action_rect.copy()   
        for k,v in new_action_dictionary.items():
            l_withoutSurface = v.copy()
            for i in range(len(v)):
                l_withoutSurface[i] = l_withoutSurface[i][:-1]
                #convert global position to grid position
                l_withoutSurface[i][0] = self.main_grid.GetMainGridLoc(l_withoutSurface[i][0])
            new_action_dictionary[k] = l_withoutSurface
        return new_action_dictionary



    #--------------------------------------------------------------------------------------
    def Save(self) ->None:
        self.p_map_1 = [[0 for i in range(Data.Constant.MAP_SIZE[0]+1)] for j in range(Data.Constant.MAP_SIZE[1]+1)]
        self.p_map_1 = self.map_1[:Data.Constant.MAP_SIZE[1] +1]
        
        self.p_map_2 = [[0 for i in range(Data.Constant.MAP_SIZE[0]+1)] for j in range(Data.Constant.MAP_SIZE[1]+1)]
        self.p_map_2 = self.map_2[:Data.Constant.MAP_SIZE[1] +1]

        self.p_map_3 = [[0 for i in range(Data.Constant.MAP_SIZE[0]+1)] for j in range(Data.Constant.MAP_SIZE[1]+1)]
        self.p_map_3 = self.map_2[:Data.Constant.MAP_SIZE[1] +1]

        # since max tile is calculated in overall tile in all 3 layers..
        # all 3 maps will contain same amount of tile. so we just need to fill all layer map from 1 tile number
        for i in range(len(self.p_map_1)):
            self.p_map_1[i] = self.map_1[i][:Data.Constant.MAP_SIZE[0]+1]
            self.p_map_2[i] = self.map_2[i][:Data.Constant.MAP_SIZE[0]+1]
            self.p_map_3[i] = self.map_3[i][:Data.Constant.MAP_SIZE[0]+1]
        

        self.Offload_to_json()
                    
    def Offload_to_json(self):
        self.layer_1_image.clear()
        self.layer_2_image.clear()
        self.layer_3_image.clear()
        self.Prevent_image_dupplication_in_dict(self.p_map_1,self.layer_1_image)
        self.Prevent_image_dupplication_in_dict(self.map_2,self.layer_2_image)
        self.Prevent_image_dupplication_in_dict(self.map_3,self.layer_3_image)
        d_actionWithoutSurface = self.Update_action_dictionary_before_save()
        to_dump = {
            "info":{"grid_size":Data.Constant.GRID_SIZE,
                    "grid_number":Data.Constant.GRID_NUMBER
            },
            "colliders":{
                "collider_rect": OneDictPerLine(d_actionWithoutSurface) 
            },
            "layer_1":{"images": self.layer_1_image,
                        "map" : [NoIndent(elem) for elem in self.p_map_1]
            },
            "layer_2":{"images": self.layer_2_image,
                        "map" : [NoIndent(elem) for elem in self.p_map_2]
            },
            "layer_3":{"images": self.layer_3_image,
                        "map" : [NoIndent(elem) for elem in self.p_map_3]
            }
        }
        with open("test_animaton.json" , "w") as f:           
            json.dump(to_dump, f, cls=MyEncoder, sort_keys=True, indent=4)


    def Prevent_image_dupplication_in_dict(self,map,l_image):
        '''look for all image used with ids to offload to json.. images name only not location '''
        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j] == 0:
                    continue
                if map[i][j] in l_image:
                    continue
                num = map[i][j]
                l_image[num] = self.uiManager.d_tileSet[num]


if __name__ == "__main__":
    gruesomeMapMaker = GruesomeMapMaker()
    gruesomeMapMaker.Update()