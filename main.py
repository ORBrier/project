import pygame
import random
import sys

# size of screen
display_width = 1350
display_height = 850

# normal game setup
clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Arcade game')

# declaring miscellaneous variables
menu = True
restart_screen = False
options_screen = False
added_player = False
game = False
score = 0
dead = False
respawned = True
phase2 = False
boss_health = 20
buffer = False
player_health = 3

# options screen variables
options = [
    "Return to Menu",
    "Help and Controls",
    "Change Acount:",
    "Difficulty:"
]
controls = [
    "Item 1",
    "Item 2",
    "Item 3",
    "Item 4",
    "Item 5"
]

selected_option = 0
difficulty = 0.3
EASY = True
MEDIUM = False
HARD = False
controls_screen = False
accounts_screen = False

# fonts
big_font = pygame.font.SysFont("display", 32)
small_font = pygame.font.SysFont("Calibri", 25)
font = pygame.font.Font(None, 36)


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
        self.image = pygame.Surface([100, 100])
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.down = True
        self.health = 10

    def update(self):
        if self.down:
            self.rect.y -= 5
            if self.rect.y <= 10:
                self.down = False
        else:
            self.rect.y += 5
            if self.rect.y >= 840-100:
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
key_state = {
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
    global added_player

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
    if added_player == False:
        player = Player()
        player.rect.y = 1
        player_group.add(player)
        player.rect.x = 200
        added_player = True

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

pygame.init()

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

        # open/close options menu
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_o:
                options_screen = True
                menu = False



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

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 and options_screen:
                EASY = True
                MEDIUM = False
                HARD = False
            if event.key == pygame.K_2 and options_screen:
                EASY = False
                MEDIUM = True
                HARD = False
            if event.key == pygame.K_3 and options_screen:
                EASY = False
                MEDIUM = False
                HARD = True

        # options menu interactivity
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_option = (selected_option - 1) % len(options)
            elif event.key == pygame.K_DOWN:
                selected_option = (selected_option + 1) % len(options)
            elif event.key == pygame.K_RETURN:
                if selected_option == 0:
                    menu = True
                    options_screen = False
                elif selected_option == 1:
                    controls_screen = True
                elif selected_option == 2:
                    accounts_screen = True
                elif selected_option == 3:
                    print("difficult")

    # --Menu-- # -------------------------------------------------------------------------------------------------------------------------------
    if menu == True:
        screen.fill(black)

        button_width = 240
        button_height = 50
        button_x = (display_width - button_width) // 2
        button_y = (display_height - button_height) // 2 + 200

        # start button
        start_button_rect = pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(button_x, button_y, button_width, button_height))
        start_text = font.render("Press N to start", True, (255, 255, 255))
        start_text_rect = start_text.get_rect(center=start_button_rect.center)
        screen.blit(start_text, start_text_rect)

        # options button
        option_button_rect = pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(button_x, button_y + 75, button_width, button_height))
        option_text = font.render("Press O for options", True, (255, 255, 255))
        option_text_rect = option_text.get_rect(center=option_button_rect.center)
        screen.blit(option_text, option_text_rect)

        # leaderboard display
        leaderboard_title = big_font.render("Leaderboard rankings", True, white)
        screen.blit(leaderboard_title, (550, 20))

        title_x = 400
        title_y = 70
        rankTitle = small_font.render("Rank", 300, white)
        scoreTitle = small_font.render("Score", 300, white)
        nameTitle = small_font.render("Account", 300, white)
        diffTitle = small_font.render("Difficulty", 300, white)
        screen.blit(rankTitle, (title_x,title_y))
        screen.blit(scoreTitle, (title_x + 150, title_y))
        screen.blit(nameTitle, (title_x + 300, title_y))
        screen.blit(diffTitle, (title_x + 450, title_y))

        records = read_records()
        start_y = 70
        for rank, record in enumerate(records, start=1):
            if rank > 10:
                pass
            else:
                rank_text = small_font.render(str(rank), True, white)
                score_text = small_font.render(record[1], True, white)
                name_text = small_font.render(record[0], True, white)
                difficulty_text = small_font.render(record[2], True, white)
                screen.blit(rank_text, (title_x, start_y + rank * 30))
                screen.blit(score_text, (title_x + 150, start_y + rank * 30))
                screen.blit(name_text, (title_x + 300, start_y + rank * 30))
                screen.blit(difficulty_text, (title_x + 450, start_y + rank * 30))

    # --Options screen-- # -------------------------------------------------------------------------------------------------------------------------------
    elif options_screen == True:

        screen.fill(black)

        if controls_screen:
            controls_title = big_font.render("Controls:", True, white)
            screen.blit(controls_title, (550, 20))
            y_offset = 70
            for item in controls:
                text_surface = small_font.render(item, True, white)
                text_rect = text_surface.get_rect()
                text_rect.center = (display_width // 2 - 110, y_offset)
                screen.blit(text_surface, text_rect)
                y_offset += 35

            # Back button
            back_button_rect = pygame.Rect(100, display_height - 100, 200, 50)
            pygame.draw.rect(screen, white, back_button_rect)
            back_button_text = small_font.render("Go back", True, black)
            text_rect = back_button_text.get_rect(center=back_button_rect.center)
            screen.blit(back_button_text, text_rect)

            # Handle mouse events for the back button
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if back_button_rect.collidepoint(event.pos):
                            controls_screen = False

        elif accounts_screen:
            accounts = big_font.render("Accounts:", True, white)
            screen.blit(accounts, (540, 45))

            account_name1 = small_font.render("1: Oli", True, white)
            screen.blit(account_name1, (450, 100))

            account_name2 = small_font.render("2: Ben", True, white)
            screen.blit(account_name2, (550, 100))

            account_name3 = small_font.render("3: Guest", True, white)
            screen.blit(account_name3, (650, 100))

            # Back button v2
            back_button2_rect = pygame.Rect(100, display_height - 100, 200, 50)
            pygame.draw.rect(screen, white, back_button2_rect)
            back_button2_text = small_font.render("Go back", True, black)
            text2_rect = back_button2_text.get_rect(center=back_button2_rect.center)
            screen.blit(back_button2_text, text2_rect)

            # Handle mouse events for the back button
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if back_button2_rect.collidepoint(event.pos):
                            accounts_screen = False

        else:
            for i, option in enumerate(options):
                if i == selected_option:
                    option_text = font.render("> " + option, True, white)
                else:
                    option_text = font.render(option, True, white)
                screen.blit(option_text, (100, 100 + i * 50))

            # difficluty toggle
            difficulty_text1 = small_font.render("Easy", True, white)
            screen.blit(difficulty_text1, (260, 100 + 3 * 50))

            difficulty_text2 = small_font.render("Medium", True, white)
            screen.blit(difficulty_text2, (320, 100 + 3 * 50))

            difficulty_text3 = small_font.render("Hard", True, white)
            screen.blit(difficulty_text3, (420, 100 + 3 * 50))

            if EASY:
                difficulty_text1 = small_font.render("Easy", True, green)
                screen.blit(difficulty_text1, (260, 100 + 3 * 50))
            if MEDIUM:
                difficulty_text2 = small_font.render("Medium", True, green)
                screen.blit(difficulty_text2, (320, 100 + 3 * 50))
            if HARD:
                difficulty_text3 = small_font.render("Hard", True, green)
                screen.blit(difficulty_text3, (420, 100 + 3 * 50))


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
        for g in boss_group:
            boss_group.remove(g)

        added_boss = False
        added_player = False
        respawned = False

        # clear score
        temp_score = score
        score = 0

        # update leaderboard
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

        # boss shooting
        if phase2:
            for boss in boss_group:
                chance = random.randint(0, 10000)
                if (chance % 10) == 0:
                    bossShoot = Shoot()
                    bossShoot.rect.x = boss.rect.x
                    bossShoot.rect.y = boss.rect.y
                    shoot_group.add(bossShoot)

        # enemies shooting
        for enemy in enemy_group:
            chance = random.randint(0, 10000)
            if (chance % 333) == 0:
                shoot = Shoot()
                shoot.rect.x = enemy.rect.x
                shoot.rect.y = enemy.rect.y
                shoot_group.add(shoot)

        # calculate mechanics for each bullet
        if score < 10:
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

        # boss bullets and health
        if score >= 10 and buffer == False:
            for bullet in bullet_group:
                if bullet.rect.colliderect(boss.rect):
                    boss.health -= 1
                    score += 1
                    buffer = True

        if boss.health <= 0:
            boss_group.remove(boss)
            all_sprites_list.remove(boss)
            phase2 = False

        # calculate mechanics for player being hit by the enemy
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

        # respawing sprites to restart game
        if respawned == False:
            spawn()
            respawned = True

        # sprites draw
        enemy_group.draw(screen)
        player_group.draw(screen)
        bullet_group.draw(screen)
        shoot_group.draw(screen)
        if score == 10:
            phase2 = True
            boss_group.draw(screen)

        # flag for leaderboard score
        flag = False

    # updating the gamme window
    pygame.display.flip()
    clock.tick(75)
