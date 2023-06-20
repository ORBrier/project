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

#text variables
player1_score = 0
reset_text = ("press SPACE to reset score")
game_font = pygame.font.SysFont("display", 32)
outcome_font = pygame.font.SysFont("Calibri", 100)

#colours
red = (255, 0,0)
green = (0, 255,0)
blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)
darkBrown = (10, 10, 10)
menuColour = (100, 70, 60)

# ---Classes--- #
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(800,1200)
        self.rect.y = random.randint(0,800)


    def update(self):
        pass

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20,30])
        self.image.fill(blue)
        self.rect = self.image.get_rect()

    def update(self):
        #pos = pygame.mouse.get_pos()
        #self.rect.y = pos[1]
        self.rect.y += 5

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([15, 10])
        self.image.fill(white)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += 10


# --functions-- #

# holding key down
key_state = {
}
def key_held(k):
    if k in key_state:
        return key_state[k]
    else:
        return False


# -----Main code----- #

#start pygame
pygame.init()

#Sprite lists
# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

# List of each block in the game
enemy_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

for x in range(10):
    enemy = Enemy()
    enemy_group.add(enemy)

for y in range(1):
    player = Player()
    player_group.add(player)
player.rect.x = 200


running = True
clock = pygame.time.Clock()


while running:
    #Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        #Quit game option
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet()

                # Set the bullet so it is where the player is
                bullet.rect.x = player.rect.x
                bullet.rect.y = player.rect.y
                # Add the bullet to the lists
                all_sprites_list.add(bullet)
                bullet_group.add(bullet)

        #moving the player
        if event.type == pygame.KEYDOWN:
            key_state[event.key] = True
        elif event.type == pygame.KEYUP:
            key_state[event.key] = False

        #menu setup
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                menu = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                menu = True


        # --Game logic-- #
    menu = False
    if menu: # if menu is open
        screen.fill(menuColour)

        #startText = startFont.render("Press S to start", 300, black)
        #screen.blit(startText, (400, 350))
    else:
        # Call the update() method on all the sprites
        #all_sprites_list.update()

        # Clear the screen
        screen.fill(black)

        if key_held(pygame.K_w):
            player.rect.y -= 10

        enemy_group.update()
        player_group.update()
        bullet_group.update()

        enemy_group.draw(screen)
        player_group.draw(screen)
        bullet_group.draw(screen)
        # Draw all the spites
        #all_sprites_list.draw(screen)


    #updating the gamme window
    pygame.display.flip()
    clock.tick(75)



