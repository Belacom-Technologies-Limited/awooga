import belacomInfo
import json
import sys
import threading
import os
from PIL import Image
import pygame

# file-wide variables
layersLock = threading.Lock()

# does this need a comment?
class main:
    # initialize
    def init(self, size=(800,400), caption = None, icon = None, fps = 60):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        if icon is not None:
            self.icon = pygame.image.load(icon).convert()
            pygame.display.set_icon(self.icon)
        if caption is not None:
            self.caption = caption
            pygame.display.set_caption(self.caption)

        self.fps = fps
        self.clock = pygame.time.Clock()
        self.dt = 1 / fps
        return self.screen

    # blit everything
    def blitAll(self, layers):
        self.screen.fill((0, 0, 0))
        for layer in layers:
            self.blitLayer(layer)

    # blit a single layer
    def blitLayer(self, layer):
        for surface in layer:
            self.screen.blit(surface["img"], surface["coord"])

    # this is obsolete but just in case
    def updateLayer(self, layer, animSurfaces = None):
        if animSurfaces is not None:
            for surface in animSurfaces:
                if surface in layer:
                    layer.remove(surface)
                layer.append(surface)
        self.blitLayer(layer)
        if animSurfaces is not None:
            for surface in animSurfaces:
                layer.remove(surface)

    # event loop
    def eventLoop(self, things):
        for event in pygame.event.get(): # event loop
            if event.type == pygame.QUIT: # exit checker
                pygame.quit()
                sys.exit()
            for thing in things:
                condition = thing["condition"]
                handler = thing["handler"]
                if event.type == pygame.KEYDOWN:
                    if event.key == condition:
                        handler(self)
                elif event.type == condition:
                    handler(self)

    def updateScreen(self, layers):
        self.blitAll(layers)
        pygame.display.flip()
        self.dt = self.clock.tick(self.fps) / 1000.0

    def getDeltaTime(self):
        if not hasattr(self, 'dt'):
            self.dt = 1
        return self.dt



# sprite
class sprite:
    def __init__(self):
        self.e = "e"
        self.velox = 0
        self.veloy = 0
        self.onGround = False

    def create(self, layers, image, pos=(0,0), layer = 0, png = True, gravity = 0, floor = 300):
        # load image into memory
        if png == True:
            self.img = pygame.image.load(image).convert_alpha()
        else:
            self.img = pygame.image.load(image).convert()
        self.surface = {"img": self.img, "coord": pos}

        # add it to the layers
        with layersLock:
            layers[layer].append(self.surface)
            self.surface = layers[layer][len(layers[layer])-1]

        # get rekt
        self.rect = self.img.get_rect(topleft=pos)
        
        # gravity creator
        self.gravity = gravity
        self.floor = floor

        # return
        return self.img, self.rect
    
    def update(self, renderer, handler = None):

        self.dt = renderer.getDeltaTime()
        if handler is not None:
            handler(self)

        self.veloy += self.gravity * self.dt
        self.rect.x += self.velox * self.dt
        self.rect.y += self.veloy * self.dt

        if self.rect.bottom >= self.floor:
            self.rect.bottom = self.floor
            self.veloy = 0
            self.onGround = True
        else:
            self.onGround = False

        with layersLock:
            self.surface["img"] = self.img
            self.surface["coord"] = self.rect.topleft
        









# commented code because why not

# class player:
#     def __init__(self):
#         self.sprite = sprite()
#         self.speed = 5
#
#     def create(self, screen, surfaceNo, filename, width, height, surfaces=[[None]], collisionEnabled=True, x=50, y=50, transparentColor=(0, 0, 0)):
#         self.sprite.create(screen=screen, filename=filename, width=width, height=height, surfaces=surfaces, surfaceNo=surfaceNo, collisionEnabled=collisionEnabled, x=x, y=y, transparentColor=transparentColor)
#
#     def draw(self):
#         self.sprite.update()
#
#     def update(self, speed=5):
#         self.speed = speed
#         input_state = self.sprite.input()
#         keys = input_state["keys"]
#         if keys[pygame.K_w] or keys[pygame.K_UP]:
#             self.sprite.rect.y -= self.speed
#         if keys[pygame.K_s] or keys[pygame.K_DOWN]:
#             self.sprite.rect.y += self.speed
#         if keys[pygame.K_a] or keys[pygame.K_LEFT]:
#             self.sprite.rect.x -= self.speed
#         if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
#             self.sprite.rect.x += self.speed
#
#     def checkCollision(self, surfaces):
#         return self.sprite.checkCollision(surfaces)
#
#     @property
#     def rect(self):
#         return self.sprite.rect
#
#
# class sprite:
#     def __init__(self):
#         self.filename = None
#         self.width = None
#         self.height = None
#         self.image = None
#         self.rect = None
#         self.screen = None
#         self.surface = []
#         self.surfaceNo = 0
#         self.collision = False
#         self.collisionEnabled = True
#     def create(self, screen = None, filename = None, width = None, height = None, collisionEnabled = True, surfaces = [[None]], surfaceNo = 0, x=50, y=50, transparentColor=(0, 0, 0)):
#         self.filename = filename
#         self.width = width
#         self.height = height
#         self.image = pygame.image.load(filename).convert()
#         self.image = pygame.transform.scale(self.image, (width, height))
#         self.image.set_colorkey(transparentColor)
#         self.rect = self.image.get_rect(topleft=(x, y))
#         self.screen = screen
#         self.collisionEnabled = collisionEnabled
#         self.surfaceNo = surfaceNo
#         self.rect.clamp_ip(screen.get_rect())
#         screen.blit(self.image, (x, y))
#         if self.collisionEnabled == True:
#             self.surface = surfaces
#             self.surface[surfaceNo].append(self.rect)
#             return self.surface 
#
#     def input(self):
#         self.keys = pygame.key.get_pressed()
#         self.mouse = pygame.mouse.get_pos()
#         self.mouseButtons = pygame.mouse.get_pressed()
#         result = {"keys": self.keys, "mouse": self.mouse, "mouseButtons": self.mouseButtons}
#         return result
#     
#     def update(self):
#         self.screen.blit(self.image, self.rect)
#         
#     def checkCollision(self, surfaces):
#        self.collision = False
#        for rect in surfaces[self.surfaceNo]:
#            if rect is not None and rect is not self.rect and self.rect.colliderect(rect):
#                self.collision = True
#                break
#        return self.collision

# idk if im adding these
#def pngToList(filename):
#    img = Image.open(filename)
#    img = img.convert("RGB")
#    width, height = img.size
#    grid = []
#    for y in range(height):
#        row = []
#        for x in range(width):
#            pixel = img.getpixel((x, y))
#            row.append(pixel)
#        grid.append(row)
#    return grid

#def sprite(screen, fwd, x, y, width, height, speed, sprite = None, bwd=None, lft=None, rgt=None, handler=None):
#    dt = pygame.time.Clock().tick(60)  # Delta time in seconds
#    if sprite == None:
#        forward = pygame.image.load(fwd).convert_alpha()
#        forward = pygame.transform.scale(forward, (width, height))
#        return forward
#        screen.blit(forward, (x, y))
#    else:
#        if handler is not None:
#            x, y, speed = handler(x, y)
#    keys = pygame.key.get_pressed()
#    if keys[pygame.K_w]:
#        y -= speed * dt
#    if keys[pygame.K_s]:
#        y += speed * dt
#    if keys[pygame.K_a]:
#        x -= speed * dt
#    if keys[pygame.K_d]:
#        x += speed * dt
#    screen.blit(sprite, (x, y))
#    return x, y
