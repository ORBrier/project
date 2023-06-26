import pygame
import random

# size of screen
display_width = 1350
display_height = 850

# normal game setup
clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('pygame.display.set_caption')

# miscellaneous variables
menu = True
restart_screen = False
game = False
score = 0
dead = False
respawned = False
big_font = pygame.font.SysFont("display", 32)
small_font = pygame.font.SysFont("Calibri", 25)

# colours
red = (255, 0,0)
green = (0, 255,0)
blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
darkBrown = (10, 10, 10)
lighterBrown= (100, 70, 60)

# ---Classes--- # -------------------------------------------------------------------------------------------------------------------------------
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

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([150, 150])
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.down = True

    def update(self):
        if self.down:
            self.rect.y -= 5
            if self.rect.y <= 10:
                self.down = False
        else:
            self.rect.y += 5
            if self.rect.y >= 840-150:
                self.down = True

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([25,50])
        self.image.fill(blue)
        self.rect = self.image.get_rect()

    def update(self):
        if self.rect.y >= 800:
            pass
        else:
            self.rect.y += 5

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([15, 10])
        self.image.fill(white)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += 10

class Shoot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([15, 10])
        self.image.fill(red)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x -= 5

class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([400, 800])
        self.image.fill(yellow)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x -= 2

# --Functions-- # -------------------------------------------------------------------------------------------------------------------------------
key_state = { # holding key down
}
def key_held(k):
    if k in key_state:
        return key_state[k]
    else:
        return False

# spawning sprites
def spawn():
    global boss
    global player
    global enemy

    # enemies
    for x in range(10):
        enemy = Enemy()
        enemy_group.add(enemy)

    # boss
    boss = Boss()
    boss_group.add(boss)
    boss.rect.x = 1000
    boss.rect.y = 350

    # player
    player = Player()
    player.rect.y = 1
    player_group.add(player)
    player.rect.x = 200

def read_records():
    records = []
    with open("records.txt", "r") as file:
        for line in file:
            record = line.strip().split(",")
            records.append(record)
    return records

def write_records(records):
    with open("records.txt", "w") as file:
        for record in records:
            line = ",".join(record)
            file.write(line + "\n")

def update_leaderboard(name, score, difficulty):
    records = read_records()
    records.append([name, str(score), difficulty])
    records.sort(key=lambda x: int(x[1]), reverse=True)
    write_records(records)


# -----Sprites----- # -------------------------------------------------------------------------------------------------------------------------------

pygame.init() # start pygame

# sprite lists
all_sprites_list = pygame.sprite.Group()

enemy_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
shoot_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()

spawn()

# ---Main game loop--- # -------------------------------------------------------------------------------------------------------------------------------
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        # quit game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()

        # restart game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game = True
                restart_screen = False

        # quit to menu
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                menu = True
                restart_screen = False

        # player firing
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet()

                # Set the bullet so it is where the player is
                bullet.rect.x = player.rect.x
                bullet.rect.y = player.rect.y

                # Add the bullet to the lists
                bullet_group.add(bullet)

        # moving the player
        if event.type == pygame.KEYDOWN:
            key_state[event.key] = True
        elif event.type == pygame.KEYUP:
            key_state[event.key] = False

        # exit menu
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                menu = False
                restart_screen = False
                game = True

    # --Menu-- # -------------------------------------------------------------------------------------------------------------------------------
    if menu: # if menu is open
        screen.fill(black)

        button_width = 220
        button_height = 50
        button_x = (display_width - button_width) // 2
        button_y = (display_height - button_height) // 2 + 200

        # start button
        start_button_rect = pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(button_x, button_y, button_width, button_height))
        start_font = pygame.font.Font(None, 36)
        start_text = start_font.render("Press N to start", True, (255, 255, 255))
        start_text_rect = start_text.get_rect(center=start_button_rect.center)
        screen.blit(start_text, start_text_rect)

        # leaderboard display
        leaderboard_title = big_font.render("Leaderboard rankings", True, white)
        screen.blit(leaderboard_title, (550, 20))

        title_x = 400
        title_y = 70
        rankTitle = small_font.render("Rank", 300, white)
        scoreTitle = small_font.render("Score", 300, white)
        nameTitle = small_font.render("Name", 300, white)
        diffTitle = small_font.render("Difficulty", 300, white)
        screen.blit(rankTitle, (title_x,title_y))
        screen.blit(scoreTitle, (title_x + 150, title_y))
        screen.blit(nameTitle, (title_x + 300, title_y))
        screen.blit(diffTitle, (title_x + 450, title_y))

        records = read_records()
        start_y = 70
        for rank, record in enumerate(records, start=1):
            rank_text = small_font.render(str(rank), True, white)
            score_text = small_font.render(record[1], True, white)
            name_text = small_font.render(record[0], True, white)
            difficulty_text = small_font.render(record[2], True, white)
            screen.blit(rank_text, (title_x, start_y + rank * 30))
            screen.blit(score_text, (title_x + 150, start_y + rank * 30))
            screen.blit(name_text, (title_x + 300, start_y + rank * 30))
            screen.blit(difficulty_text, (title_x + 450, start_y + rank * 30))

    # --Restart screen-- # -------------------------------------------------------------------------------------------------------------------------------
    elif restart_screen == True:
        screen.fill(black)

        # death screen (with img in files)
        you_died_image = pygame.image.load("you_died.jpg")
        x = (display_width - you_died_image.get_width()) // 2
        y = (display_height - you_died_image.get_height()) // 2
        screen.blit(you_died_image, (x, y))

        # restart game text
        restartText = small_font.render("Press R to restart", 300, white)
        screen.blit(restartText, (600, 550))
        menuText = small_font.render("Press M to return to the menu", 300, white)
        screen.blit(menuText, (600, 600))

        # clear the sprites off the screen
        for d in enemy_group:
            enemy_group.remove(d)
        for e in bullet_group:
            bullet_group.remove(e)
        for f in shoot_group:
            shoot_group.remove(f)
        boss_group.remove(1)

        # clear score
        temp_score = score
        score = 0

        # respawing sprites to restart game
        if respawned == False:
            spawn()
            respawned = True

        # Update leaderboard
        nombre = "OLI"
        temp_difficulty = "Easy"
        while flag == False:
            player_name = nombre
            player_score = temp_score
            player_difficulty = temp_difficulty
            update_leaderboard(player_name, player_score, player_difficulty)
            flag = True

    # --Game screen-- # -------------------------------------------------------------------------------------------------------------------------------
    elif game == True:

        # backround design
        screen.fill(black)

        # score text
        scoreTxt = small_font.render(f"Score: {score}", False, white)
        screen.blit(scoreTxt, (10, 10))

        # hold to rise up screen
        if key_held(pygame.K_w) and player.rect.y > 0:
            player.rect.y -= 10

        # enemies shooting
        for enemy in enemy_group:
            chance = random.randint(0, 10000)
            if (chance % 333) == 0:
                shoot = Shoot()
                shoot.rect.x = enemy.rect.x
                shoot.rect.y = enemy.rect.y
                shoot_group.add(shoot)

        # calculate mechanics for each bullet
        for bullet in bullet_group:

            # See if it hit a block
            block_hit_list = pygame.sprite.spritecollide(bullet, enemy_group, True)

            # For each block hit, remove the bullet and add to the score
            for enemy in block_hit_list:
                bullet_group.remove(bullet)
                all_sprites_list.remove(bullet)
                score += 1

            # Remove the bullet if it flies up off the screen
            if bullet.rect.x < -10 or bullet.rect.x > 1400:
                bullet_group.remove(bullet)
                all_sprites_list.remove(bullet)

        # calculate mechanics for player dead and shooting from enemy (same code as bullets and enemies)
        for shoot in shoot_group:
            health_hit_list = pygame.sprite.spritecollide(shoot, player_group, True)
            for player in health_hit_list:
                shoot_group.remove(shoot)
                all_sprites_list.remove(shoot)
                dead = True
            if shoot.rect.x < -10 or shoot.rect.x > 1400:
                shoot_group.remove(shoot)
                all_sprites_list.remove(shoot)

        # condition in game end
        if dead:
            restart_screen = True
            game = False
            dead = False

        # sprites update
        enemy_group.update()
        player_group.update()
        bullet_group.update()
        shoot_group.update()
        boss_group.update()

        # sprites draw
        enemy_group.draw(screen)
        player_group.draw(screen)
        bullet_group.draw(screen)
        shoot_group.draw(screen)
        if score == 10: # after first wave dies
            boss_group.draw(screen)

        # flag for leaderboard score
        flag = False

    # updating the gamme window
    pygame.display.flip()
    clock.tick(75)
