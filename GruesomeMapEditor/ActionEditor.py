from dataclasses import dataclass

@dataclass
class RectangleContains:
    name: str
    width: int
    height: int
    topLeft: list[int] 


class ActionEditor:
    def __init__(self):
        self.d_colliders = {} # key = name, item = list of tiles
    
    def Add_colliders(self,name,l_tiles) -> None:
        ''' concat list of tiles to list in dictionary if it exist.. and add new key "name" if not exist'''
        for k,i in self.d_colliders.items():
            if name == k:
                self.d_colliders[name] =self.d_colliders[name] + l_tiles
                return
        self.d_colliders[name] = l_tiles
    
    def Remove_colliders(self,name,l_tiles):
        pass

    
    def Create_rect(self,name:str,dimentions:list[int]):
        pass

    def Remove_rect(self,name):
        pass
    