from pygame import Surface
from GruesomeMapEditor.Data.TileType import Button_Type
from UI.ScrollArea import ScrollArea


class Explorer:
    '''when left click open a explorer which will contain other menus'''
    def __init__(self,surfaceSize = (400,400)) -> None:
        self.surface = Surface(surfaceSize)
        self.surface.fill((200,200,200))
        self.x = 180

        self.l_file_explorer_buttons = []

        self.scroll_area = None
        
        self.filePath = [] # add here when we browse filePath buttons
        self.currFolderPath = ""
        self.scroll_area = ScrollArea(self.l_file_explorer_buttons,(200,300))

    def Render(self,display,MouseLoc) -> None:
        display.blit(self.surface,MouseLoc)


    def Render_file_explorer(self,display):
        '''render file explorer and child buttons'''
        display.blit(self.surface,(self.x,10))
        self.surface.fill((200,200,200))
        self.scroll_area.Render(self.surface)


    def Add_scroll_area(self,dimention):
        self.scroll_area = ScrollArea(self.l_file_explorer_buttons,dimention)

    def Change_folder(self):
        '''change folder when browsing explorer'''
        pass


    def Refresh(self):
        ''' Update buttons or tiles '''
        # clicked file explorer button .. so change folder and change buttons
        if len(self.l_file_explorer_buttons)>0:
            if self.l_file_explorer_buttons[0].btn_type == Button_Type.file_explorer:
  
                self.l_file_explorer_buttons = []
