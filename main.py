import pygame
import random

# size of screen
display_width = 1350
display_height = 850

# normal game setup
clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('My amazing game')

#some variables
menu = True

#colours
red = (255, 0,0)
green = (0, 255,0)
blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)
darkBrown = (10, 10, 10)

# ---Classes--- #
class enemy(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill(color)
        self.rect = self.image.get_rect()

class player(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.image = pygame.Surface([20,30])
        self.image.fill(color)
        self.rect = self.image.get_rect()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

    #def update(self):
     #   self.rect.y -= 10

class Object(pygame.sprite.Sprite):
    def __init__(self, name, width, height, color):
        super().__init__()
        self.name = (name)
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

# --functions-- #



# -----Main code----- #

#start pygame

while True:
    #Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        #Quit game option
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()

        #moving the player
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.rect.x -= 5

        #menu setup
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                menu = False

    # --Game logic-- #
    if menu == True:
        screen.fill(darkBrown)
        #startText = startFont.render("Press S to start", 300, black)
        #screen.blit(startText, (400, 350))
    else:
        # Call the update() method on all the sprites
        #all_sprites_list.update()

        # Clear the screen
        screen.fill(black)

        # Draw all the spites
        #all_sprites_list.draw(screen)

        #player_list.draw(screen)


    #updating the gamme window
    pygame.display.flip()
    clock.tick(75)



