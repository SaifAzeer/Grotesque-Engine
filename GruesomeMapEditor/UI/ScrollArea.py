
from typing import List
from pygame import Surface
from UI.Button_Function import Button_Function
from UI.Button import Button
from Data.TileType import Button_Type
from pygame import mouse

class ScrollArea:
    def __init__(self,l_widgets:List[Button],area_size,colour = (200,20,20)):
        self.l_widgets = l_widgets
        self.area_size = area_size
        self.colour = colour
        # to calculate using a widjet * number of widgets
        self.scroll_surface = Surface(area_size) 
        self.scroll_surface.fill(colour)

        self.scroll_y = 0 # use to scroll
        self.scrolled = 0
        self.scroll_speed = 30

    def Render(self,display):
        #display.blit(self.scroll_surface,(0,0),(0,self.scroll_y,100,100))
        #self.FillArea()
        self.scroll_surface.fill(self.colour)
        self.FillArea()
        display.blit(self.scroll_surface,(0,0))

    def Render_tiles(self,display):
        self.scroll_surface.fill(self.colour)
        display.blit(self.scroll_surface,(0,0))

    def Update_l_widget(self,l_new_widgets):
        self.l_widgets = []
        self.l_widgets = l_new_widgets

    def Fill_tiles(self):
        
    def FillArea(self):
        for i in self.l_widgets:
            self.scroll_surface.blit(i.surf,(i.rect.x,i.rect.y))
            i.render_text()

    def ScrollUp(self):
        for i in self.l_widgets:
            i.rect.y -= self.scroll_speed
            i.position[1] -= self.scroll_speed
        self.scrolled -= self.scroll_speed

    def ScrollDown(self):
        if self.scrolled > 0:
            return
        for i in self.l_widgets:
            i.rect.y += self.scroll_speed
            i.position[1] += self.scroll_speed