from pygame import font,Rect,event,K_RETURN,draw, K_BACKSPACE

class TextBox:
    def __init__(self,position):
        self.position = position
        self.textBox = Rect(position[0],position[1],140,30)
        self.font = font.Font(None,30)
        self.active = False
        self.text = ""  
        self.textResult = ""
        self.txt_surface = self.font.render(self.text,True,(0,0,32))
        self.colour = (30,20,30)

    def Render(self,display) -> None:
        display.blit(self.txt_surface,self.position)
        draw.rect(display,self.colour,self.textBox,2)

    def Update(self,event:event) -> None:
        if self.active == False:
            return 
        if event.key == K_RETURN:
            self.textResult = self.text
            self.active = False
            self.colour = (10,20,50)
        elif event.key == K_BACKSPACE:
            self.text = self.text[:-1]
        else:
            self.text += event.unicode
        self.txt_surface = self.font.render(self.text,True,(0,0,32))
        
    def BackSpace(self) -> None:
        self.text = self.text[:-1]
    
    def Mouse_click(self,position):
        if self.textBox.collidepoint(position):
            if self.active == True:
                self.active = False
                self.colour = (30,20,30)
            else:
                self.active = True
                self.colour = (20,50,20)