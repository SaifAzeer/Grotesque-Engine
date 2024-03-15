import pygame
from sys import exit

pygame.init()
display = pygame.display.set_mode((1000,1000))
image = pygame.image.load("J:\\Tileset\\Avery\\characters\\Loved old designs.png")
imageWidth = image.get_width()
imageHeight = image.get_height()
splitIMageSizeX = 48
splitIMageSizeY = 72
spltImageNumX = (imageWidth //splitIMageSizeX) 
splitImageNumY = (imageHeight //splitIMageSizeY)
subsurfaces = []
for x in range(0,spltImageNumX):
    for y in range(0,splitImageNumY):
        location = pygame.Rect(x*splitIMageSizeX, y*splitIMageSizeY,splitIMageSizeX,splitIMageSizeY)
   
        newImage = image.subsurface(location)
        subsurfaces.append([newImage, (x*splitIMageSizeX, y*splitIMageSizeY)])

print(len(subsurfaces))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    #for i in subsurfaces:
    #    display.blit(i[0],i[1])
    display.blit(subsurfaces[11][0],subsurfaces[11][1])
    pygame.display.update()