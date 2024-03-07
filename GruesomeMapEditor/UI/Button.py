from pygame import Surface,font,image,transform
from Data.TileType import Button_Type
from Data.Global import Global ,ACTION_LAYER
from UI.Button_Function import Button_Function
from pygame.mouse import get_pos as mouse_position


class Button:
    is_actionEditor_on = False
    def __init__(self,text:str,layer:int,btn_type:Button_Type):
        self.text = text
        self.layer = layer
        self.btn_type = btn_type
        self.surfSize = (150,40)
        #self.surf = Surface(self.surfSize)
        #self.surf.fill((244,168,150))
        self.surf = image.load("GruesomeMapEditor/Images/UI/btnLuxwhite.png")
        self.surf = transform.scale(self.surf,self.surfSize)
        self.rect = self.surf.get_rect()
        #self.y = layer * 50 # calculate y coordinated of button
        self.position = [0,0]
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

        _font = font.SysFont('arial', 15)
        self.text_surf = _font.render(text, True, (100,100,100))
        self.textRect = self.text_surf.get_rect()
        self.textRect.center = self.rect.center
        self.btn_click = None # fnction thatll be called when button is clicked
        self.click_return = None
        self.buttonFunction = Button_Function()


    def Set_pos(self,position):
        self.position = position
        self.rect.x = position[0]
        self.rect.y = position[1]


    def Set_click_Explorer(self,_btnType,filePath = None) -> str:
        '''when clicking an explorer button.. call functions here'''
        if _btnType == "open_explorer":
            self.btn_click =self.buttonFunction.open_file_explorer()
        elif  _btnType == "click_file":
            self.btn_click =self.buttonFunction.Change_folder_explorer(filePath)
        return self.btn_click


    def on_click(self) :
        '''return button type to know what button we clicked.. used for file explorer button'''
        '''if we clicked on the button.. change layer'''
        Global.currentLayer = self.layer

        ''' if we click action button'''
        if self.btn_type == Button_Type.action:
            Global.currentLayer = ACTION_LAYER

        return self.btn_click            

    def Render(self,disp):
        disp.blit(self.surf,self.position)
        self.on_hover(mouse_position())
        self.render_text()

    def render_text(self):
        self.surf.blit(self.text_surf,self.textRect)
    
    def on_hover(self,mousepos):
        pass
        #if self.rect.collidepoint((mousepos)):
        #    self.surf.fill((20,34,33))
        #else:
        #    self.surf.fill((244,168,150))

    def on_selected(self):
        self.surf.fill((20,34,193))


    