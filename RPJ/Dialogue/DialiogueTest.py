import pygame
from Dialogue import Dialogue
from sys import exit  as sysExit


pygame.init()
display = pygame.display.set_mode((500,500))

display.fill((0,0,32))
player = pygame.Surface((50,50))
player_x,player_y = 0,0
speed = 5

character = pygame.Surface((50,50))
dialogue = Dialogue((100,100))
while True:
    dialogue.Update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sysExit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player_x -= speed
            elif event.key == pygame.K_d:
                player_x += speed
            elif event.key == pygame.K_w:
                player_y -= speed
            elif event.key == pygame.K_s:
                player_y += speed
            if event.key == pygame.K_SPACE:
                dialogue.Show_single_dialogue("testDialogue")
                
    display.fill((0,0,32))
    player.fill((100,100,100))
    character.fill((200,100,100))
    dialogue.Render(display,(75,75))
    display.blit(player,(player_x,player_y))
    display.blit(character,(150,50))
    pygame.display.update()