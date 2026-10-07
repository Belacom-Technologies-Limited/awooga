import render
import belacomInfo
import pygame

# initialization
renderer = render.main()
screen = renderer.init(icon = "assets/orange.png", caption = "runner")

# constant
layers = [[],[]] 

# frameloop functions
def jumper(main):
    if player.onGround:
        player.veloy = -900

def snailer(sprite):
    sprite.velox = -240
    if sprite.rect.x < -100:
        sprite.rect.x = 900

handlers = [{"condition": pygame.K_SPACE, 
             "handler": jumper}]

# create sprite objects
sky = render.sprite()
ground = render.sprite()
player = render.sprite()
snail = render.sprite()

# create sprites
Sky, skyPos = sky.create(layers, "assets/Sky.png", layer=0, png=False)
Ground, groundPos = ground.create(layers, "assets/ground.png", pos=(0, 300), layer=0, png=False)
Player, playerPos = player.create(layers, "assets/Player/player_stand.png", pos=(10, 200), layer=1, gravity=1800, floor=300)
Snail, snailPos = snail.create(layers, "assets/snail/snail1.png", pos=(900, 300), layer=1)

while True: # frame loop
    renderer.eventLoop(handlers)

    # snail frameloop handler
    snail.update(renderer, handler=snailer)
    
    # player frameloop handler
    player.update(renderer)

    # check for collision
    if playerPos.colliderect(snailPos):
        break

    renderer.updateScreen(layers)

# Loss
belacomInfo.info("you lost fucker")
