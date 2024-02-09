from enum import Enum

class TileType(int ,Enum):
    image = 0
    collider = 1
    interact = 2

class Tile_name_type(str,Enum):
    left = "__L.png"
    right = "__R.png"
    top   = "__T.png"
    bot   = "__B.png"
    top_left = "_TL.png"
    top_right = "_TR.png"
    bot_left = "_BL.png"
    bot_right = "_BR.png"
    animation = "_animation"

class Button_Type(int,Enum):
    tile = 0
    action = 1 
    collider = 2 
    back = 3
    file_explorer = 4
    scroll_bar = 5
    

class Expliorer_type(int,Enum):
    file_explorer = 0
    main_layout = 2
