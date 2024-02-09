
import os.path as path
from sys import path as sysPath


sysPath.append(path.dirname(path.abspath(path.join(__file__ ,"../"))))

from pygame import mouse,font,display
import glob
from os import getcwd
from Tiles import Tiles
from Data.TileType import TileType,Button_Type
from Data.Constant import LEFT_SURFACE_SIZE,GRID_SIZE,ROOTPOSITION
from Data.TileType import Tile_name_type,Button_Type 
from UI.Button import Button
from Data.Global import Global , ACTION_LAYER
from Data.Constant import DISPLAY_SIZE,UI_WIDGET_X_POS
from UI.Explorer import Explorer
from Data.Global import Global


# TODO -> make a dictionaly for the images.. to make comparing faster
class UIManager:
    TEST = True
    def __init__(self):
        self.tile_location = ROOTPOSITION
        self.explorer_tile_location = self.tile_location
        self.explorer_selected_tile_location = self.tile_location

        self.margin = 20
        self.layer_amount = 0
        self.l_layout_btn = []
        # list of tiles from tileset
        self.l_tiles = [] 
        self.l_explorer_tiles = []
        self.d_tileSet = {}
        self.d_border_tile = {} # in Ai to contain corner/border tiles

        self._font = font.SysFont('century gothic', 15)
        self.text_surf = self._font.render("Object layer 1", True, (244,168,150))
        self.btn_y = DISPLAY_SIZE[1] - 80 # y coord of button and layout text

        # buttons layout list -> contain list of button obj of each layout
        self.l_btn_layout_main = []
        self.l_btn_layout_action = []

        self.d_counter = 1
        self.btn_click_return = {}
        self.Setup_tile_icon()
        self.Main_layout_button()
        self.Action_button_layout()

        self.explorer = Explorer()
        self.show_file_explorer = False # file explorer when searching folders
        self.explorer_click = False # use to prevent adding tiles when clicking file explorer btn/ prev error

        self.btn_file_explorer = self.File_explorer_button()
        self.btn_back = self.Button_back()
        self.is_actionEditor_on = False

        #multiple selection tiles 
        self.l_multilple_selected_tiles = []

    def Setup_tile_icon(self,onleftMenu = True):
        ''''''
        tilePosition_x = 0
        tilePosition_y = 20
        
        # chose which folder location we will use to get the tiles 
        currLocation = self.tile_location
        if onleftMenu == False: # we are in the explorer
            currLocation = self.explorer_tile_location
        #if glob.glob( getcwd()+"/"+currLocation+"/"+'*.png'):
        #    for filename in glob.glob( getcwd()+"/"+currLocation+"/"+'*.png'): 
        if glob.glob( currLocation+"/"+'*.png'):
            for filename in glob.glob(currLocation+"/"+'*.png'): 
                imageName = filename.split('\\')[-1]
                if self.Check_image_if_givenID(currLocation+"/"+imageName) == False:
                    self.d_tileSet[self.d_counter] = currLocation+"/"+imageName
   
                # set tile position        
                if tilePosition_x == 0: # first tile  make sure its beautfully to the left
                    tilePosition_x = self.margin
                else: 
                    tilePosition_x += self.margin + GRID_SIZE[0]
                if tilePosition_x >= LEFT_SURFACE_SIZE[0]: #reset position
                    tilePosition_x = self.margin
                    tilePosition_y += self.margin + GRID_SIZE[1]
                
                t = Tiles( None,TileType.image,[tilePosition_x,tilePosition_y],self.d_counter,currLocation+"/"+imageName)
                self.d_counter +=1
    
                if onleftMenu:# check for ai only when we have tiles at left menu not at explorer
                    self.l_tiles.append(t)
                    self.Find_AI_borders(currLocation,imageName)
                else:
                    self.l_explorer_tiles.append(t)

            if onleftMenu:# only update selected tiles if we are trying to. ie select from left menu, not file explorer
                self.currently_selected = self.d_tileSet[1]

    
    def Find_AI_borders(self,loc,imageName):
        # look for borders for ai to use
        for i in Tile_name_type:
            if imageName[-7:] == i.value:
                self.d_border_tile[i.value] = loc+'/'+imageName


    def Switch_tile(self,number_pressed) -> str:
        ''' use dictionary to find tile based on number pressed'''
        if number_pressed in self.d_tileSet:
            self.currently_selected = self.d_tileSet[number_pressed]
            return self.currently_selected
        else:
            return None
        
    def Check_image_if_givenID(self,img):
        for i in self.d_tileSet.values():
            if i == img:
                return True
        return False


    def OnClick(self) -> str:
        '''clicked on another tile'''
        for i in self.l_tiles:
            if i.MouseHover(mouse.get_pos()):
                if mouse.get_pressed()[0] == True:
                    self.currently_selected =  i.image       
                    return i
                else:
                     return None
                
    '''str -> if button click file explorer btn . send the signal to GruesomeMapMaker
              check if folder changed. and reset selected tiles'''
    def ButtonClicked(self,mousePos) -> str:
        '''get return when clicking button.. add in dict with button name first
        so er can check which button clicked before precessing'''
        # all buttons in the left menu
        for i in self.l_layout_btn:
            if self.Hover_on_widget(mousePos,i):
                self.explorer.filePath = []
                self.Update_layout_text(i.text)
                self.btn_click_return[i.btn_type]=i.on_click() # if we clicked something
                if self.btn_click_return != None: 
                    # click file explorer  btn
                    if i.btn_type == Button_Type.file_explorer :
                        self.Fill_file_explorer()         
                        currentFolder = Global.tilePos
                        #if we dont do that. when we click back after selecting position..
                        # itll search tile at the back position where it does not exist
                        Global.tilePos = self.explorer_selected_tile_location         
                        # reset position 
                        self.explorer_tile_location = ROOTPOSITION    
                        #show and hide explorer
                        if self.show_file_explorer == True:
                            self.show_file_explorer = False
                            return "folder changed"
                        else:
                            self.show_file_explorer = True
                break
        # clicked button in file explorer         
        if self.show_file_explorer:
            for i in self.explorer.l_file_explorer_buttons:
                if self.Hover_on_widget(mousePos,i):
                    self.Update_layout_text(i.text)
                    self.explorer.filePath.append(i.text)
                    i.Set_click_Explorer("click_file",self.explorer.filePath)
                    self.explorer.currFolderPath += '\\'+i.text
                    self.btn_click_return[i.btn_type] = i.on_click() # result of subfolder when click this folder btn
                    print(i.text)
                    self.Show_tiles_file_explorer(i.text)
                    if self.btn_click_return[i.btn_type] != None:
                        self.Fill_file_explorer()     

            # clicked back button
            if self.Hover_on_widget(mousePos,self.btn_back):
                if len(self.explorer.filePath) >0:
                    self.explorer.filePath.pop()
                    self.btn_back.Set_click_Explorer("click_file",self.explorer.filePath)
                    
                    #update curr path loc by removing last location until //
                    self.explorer.currFolderPath = self.explorer.currFolderPath[:self.explorer.currFolderPath.rfind('\\')]

                    self.btn_click_return[ self.btn_back.btn_type] = self.btn_back.on_click()
                    if self.btn_click_return[i.btn_type] != None:
                        self.Show_tiles_file_explorer(remove=True)
                        self.Fill_file_explorer()   


    def Render(self,display,mousepos):      
        for i in self.l_tiles:         
            if i.image == self.currently_selected:
                i.Render_other_colour_position(display,i.position,(250,252,50))
            else:
                i.Render(display)
        display.blit(self.text_surf,(30,self.btn_y-150))
        #render buttons
        for i in self.l_layout_btn:
            i.Render(display)
        self.Open_explorer(display)
        #if self.show_file_explorer:
        #    self.explorer.scroll_area.FillArea()
            #for i in self.explorer.l_file_explorer_buttons:
            #    #self.explorer.surface.blit(i.surf,(i.rect.x,i.rect.y))
            #    self.explorer.scroll_area.scroll_surface.blit(i.surf,(i.rect.x,i.rect.y))
            #    i.render_text()
        

    def Update(self):
        if Global.currentLayer == ACTION_LAYER:
            self.l_layout_btn = self.l_btn_layout_action
            self.l_layout_btn.append(self.btn_file_explorer)
            self.is_actionEditor_on = True
        else:
            self.is_actionEditor_on = False
            self.l_layout_btn = self.l_btn_layout_main
            self.l_layout_btn.append(self.btn_file_explorer)


    def Open_explorer(self,disp):
        if self.show_file_explorer:
            self.explorer.Render_file_explorer(disp)
            self.btn_back.Render(disp)
            for i in self.l_explorer_tiles: #images preview in explorer
                i.Render(self.explorer.surface,(190,10))


    def Hover_on_widget(self,mousePos,widget) -> bool:
        '''check if mouse is on widget'''
        if (mousePos[0] >= widget.position[0] and mousePos[1] >= widget.position[1]
            and mousePos[0] <= widget.position[0] + widget.surfSize[0] 
                and mousePos[1] <= widget.position[1] + widget.surfSize[1]):
            return True
        return False


    def Update_layout_text(self,newText:str):
        self.text_surf = self._font.render(newText, True, (244,168,150))


    #----------------------------------- Layout Button ----------------------------------------------
    def Main_layout_button(self): # Main layout   
        self.Setup_button("obj layer 1",(UI_WIDGET_X_POS,self.btn_y),1,Button_Type.tile)
        self.Setup_button("obj layer 2",(UI_WIDGET_X_POS,self.btn_y),2,Button_Type.tile)
        self.Setup_button("obj layer 3",(UI_WIDGET_X_POS,self.btn_y),3,Button_Type.tile)
        self.Setup_button("collider 1",(UI_WIDGET_X_POS,self.btn_y),ACTION_LAYER,Button_Type.collider)

        self.Setup_button("action editor",(UI_WIDGET_X_POS,self.btn_y),ACTION_LAYER,Button_Type.action)


    def Action_button_layout(self):
        self.btn_y = DISPLAY_SIZE[1] - 80
        self.Setup_button("Back",(UI_WIDGET_X_POS,self.btn_y),1,Button_Type.back)
    
    
    def Setup_button(self,name,pos,layer,layerType):  # Main layout
        '''Initialise button. calls only one time'''
        button = Button(name,layer,layerType)
        button.position = pos
        button.rect.x = pos[0]
        button.rect.y = pos[1]
        self.l_layout_btn.append(button)
        # use this to select button on which layout itll appear
        if layerType == Button_Type.action or layerType == Button_Type.back: # pressed action button
            self.is_actionEditor_on = True
            self.l_btn_layout_action.append(button)
        
        if layerType == Button_Type.back:
            self.is_actionEditor_on = False
        else:
            self.l_btn_layout_main.append(button) # all buttons will be here i guess
        self.btn_y -= 40


    def File_explorer_button(self) -> Button:
        button = Button("file explorer",1,Button_Type.file_explorer)
        button.Set_pos([UI_WIDGET_X_POS,200])
        #button.btn_click = self.buttonFunction.open_file_explorer
        button.Set_click_Explorer("open_explorer")
        return button
    

    def Fill_file_explorer(self) -> None:
        '''fill file explorer with buttons of path'''
        #self.explorer_tile_location = ROOTPOSITION
        
        self.explorer.Refresh()
        position = 10
        maxCounter = len(self.btn_click_return[Button_Type.file_explorer]) 
        # make sure we get return of file explorer only and not other by some unknown mistake
        if Button_Type.file_explorer in self.btn_click_return :
            for i in range(maxCounter):
                button = Button(self.btn_click_return[Button_Type.file_explorer][i],1,Button_Type.file_explorer)
                #.position is for collider with mouse
                button.position = [self.explorer.x + UI_WIDGET_X_POS,position]
                button.rect.x = UI_WIDGET_X_POS #actual position on explorer
                button.rect.y = position
                position += 40
                self.explorer.l_file_explorer_buttons.append(button)
        self.explorer.scroll_area.Update_l_widget(self.explorer.l_file_explorer_buttons)


    def Button_back(self) -> Button:
        position = 350
        button = Button("back",1,Button_Type.file_explorer)
        button.position = [self.explorer.x + UI_WIDGET_X_POS,position]
        button.rect.x = UI_WIDGET_X_POS #actual position on explorer
        button.rect.y = position
        return button
    

    def Show_tiles_file_explorer(self,new_path="",remove = False) -> None:
        '''change global location of tiles to be used -> called every explorer btn clicked'''
        self.l_explorer_tiles = []
        #also prevent dupplication
        back_path =  self.explorer_tile_location[:self.explorer_tile_location.rfind('/')]
        if remove == False:
            if new_path == ROOTPOSITION or new_path == back_path: #itll add ROOTPOS to already ROORPOS if we dont
                return  
            
            self.explorer_tile_location += "/"+ new_path
        else:
            # cannot go back if we are at root pos.. itll cause mayhem
            if self.explorer_tile_location != ROOTPOSITION :
                self.explorer_tile_location = back_path
        Global.tilePos = self.explorer_tile_location
        self.Setup_tile_icon(False)
        

    def Select_tiles(self) ->None:
        self.explorer_selected_tile_location = self.explorer_tile_location
        self.l_tiles = []
        self.tile_location = self.explorer_tile_location
        self.Setup_tile_icon()
