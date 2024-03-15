from BaseCharacter import BaseCharacter
import pygame  # TO DO :  delete later
from sys import exit as sysExit
from pygame.math import Vector2
from GruesomeMapEditor.Deformed_map_reader import Deformed_map_reader

pygame.init()
display = pygame.display.set_mode((500, 500))

deformed_map_reader = Deformed_map_reader("J:\PythonProg\Pygame\GrotesqueEngine")
deformed_map_reader.open_map("test_animaton.json")

class Player(BaseCharacter):
    def __init__(self):
        super().__init__(display,"player","J:\PythonProg\Pygame\GrotesqueEngine\RPJ\Dialogue\Dialogue.json",deformed_map_reader.l_colliders)

        self.location = self.grid.GetWorldLoc([1, 2])
        # self.gridPosition = [1,2]
        self.SetGridPosition(Vector2(1, 2))
        self.movementSpeed = 3
        

player = Player()

FPS = 60
clock = pygame.time.Clock()
display.fill((0, 0, 32))

character = pygame.Surface((50, 50))
click_d = False
click_a = False
click_w = False
click_s = False
while True:
    player.Update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sysExit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                click_d = True
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                click_a = True
            elif event.key == pygame.K_w or event.key == pygame.K_UP:
                click_w = True
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                click_s = True
            elif event.key == pygame.K_SPACE:
                player.dialogue.Show_multiple_dialogue_timer("testDialogueMultiple",player.location)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                click_d = False
                player.keyRelease()
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                click_a = False
                player.keyRelease()
            elif event.key == pygame.K_w or event.key == pygame.K_UP:
                click_w = False
                player.keyRelease()
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                click_s = False
                player.keyRelease()
        


    if click_d:
        player.MoveRight()
    elif click_a:
        player.MoveLeft()
    elif click_w:
        player.moveUp()
    elif click_s:
        player.moveDown()
    clock.tick(FPS)
    display.fill((0, 0, 32))
    deformed_map_reader.render_map_from_tile(display)
    character.fill((200, 100, 100))
    player.Render(display)
    # display.blit(character,(150,50))
    pygame.display.update()
