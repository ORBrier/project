import pygame
import random
import pygame.image
import pygame.transform

"""Difficulty differences:
Easy
- Slowest shooting enemies
- Gains max health when a boss is defeated
- Safe spot avalable

Medium
- Fast shooting enemies
- Gains one health when a boss is defeated
- No safe spot avalable

Hard
- Very fast shooting enemies
- Gains no health when a boss is defeated
- No safe spot avalable
"""

# size of screen
display_width = 1350
display_height = 850

# normal game setup
clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Alien Barrage')

# --- Varialbes --- #

# screens (screen flags)
menu = True
restart_screen = False
options_screen = False
game = False

# game variables
score = 0
final_score = 0
enemies_dead = 0
last_hit_time = 0
buffer_time = 1000
last_hit_time2 = 0
boss_health = 10
player_health = 3

# red flash
show_red_flash = False
red_flash_duration = 1000
red_flash_start_time = 0

# weapons variables
weapon_selection = False
WBlue = True
WGreen = False
WYellow = False
WRed = False
bullet_timer = 0
last_shot_time = 0
explode = False
explode_duration = 1000
explode_time = 0

# other flags
added_player = False
dead = False
respawned = True
buffer = False
buffer2 = False


# looping game variables
current_phase = 0
phase1 = False
phase2 = False

# options screen variables
selected_option = 0
difficulty = 0.3
EASY = True
MEDIUM = False
HARD = False
controls_screen = False
accounts_screen = False
ACC1 = False
ACC2 = False
ACC3 = True

options = [
    "Return to Menu",
    "Infomation on Controls",
    "Change Acount:",
    "Difficulty:"
]
controls = [
    "Move player up => w",
    "Shut down game => Escape",
    "Select option one => 1",
    "Select option two => 2",
    "Select option three => 3"
]

# fonts
big_font = pygame.font.SysFont("display", 32)
small_font = pygame.font.SysFont("Calibri", 25)
font = pygame.font.Font(None, 36)
warning_font = pygame.font.Font(None, 50)

# colour pallete
red = (255, 0,0)
green = (0, 255,0)
blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)
darkerWhite = (230, 200, 160)
titleColour = (150, 150, 250)
yellow = (255, 255, 0)
darkPurple = (48, 25, 52)
darkBrown = (10, 10, 10)
lighterBrown = (100, 70, 60)
orange = (255, 165, 0)

# images variables
game_title_icon = pygame.image.load("gameTitle_icon.png").convert_alpha()
game_title_icon = pygame.transform.scale(game_title_icon, (600, 250))

pirate = pygame.image.load("pirate.png").convert_alpha()
pirate = pygame.transform.scale(pirate, (200, 300))

alien = pygame.image.load("alien.png").convert_alpha()
alien = pygame.transform.scale(alien, (250, 250))

explotion = pygame.image.load("Explotion_animation.png").convert_alpha()
explotion = pygame.transform.scale(explotion, (300, 300))

# for deco: pygame.draw.polygon(screen, color, (point-x, point-y, point-z))

green_button = pygame.image.load("greenWeaponBanner_icon.png")
green_button = pygame.transform.scale(green_button, (300, 600))

yellow_button = pygame.image.load("yellowWeaponBanner_icon.png")
yellow_button = pygame.transform.scale(yellow_button, (300, 600))

red_button = pygame.image.load("redWeaponBanner_icon.png")
red_button = pygame.transform.scale(red_button, (300, 600))

# ---Classes--- # -------------------------------------------------------------------------------------------------------------------------------
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        enemy_icon = pygame.image.load("enemies_icon.png").convert_alpha()

        # Resize the image to match the size of the enemy's surface
        self.image = pygame.transform.scale(enemy_icon, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(600, 1200)

        if EASY or MEDIUM:
            self.rect.y = random.randint(50, 800)
        if HARD:
            self.rect.y = random.randint(50, 840)
        self.speed_x = random.choice([-2, 2])  # Random horizontal speed
        self.speed_y = random.choice([-2, 2])  # Random vertical speed

    def update(self):
            # Move the enemy based on its speed
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

            # Check boundaries to keep the enemy within the desired area
            if self.rect.left < 600:
                self.speed_x = abs(self.speed_x)  # Reverse horizontal direction
            elif self.rect.right > 1200:
                self.speed_x = -abs(self.speed_x)  # Reverse horizontal direction

            if EASY or MEDIUM:
                if self.rect.top < 50:
                    self.speed_y = abs(self.speed_y)  # Reverse vertical direction
                elif self.rect.bottom > 800:
                    self.speed_y = -abs(self.speed_y)  # Reverse vertical direction

            if HARD:
                if self.rect.top < 50:
                    self.speed_y = abs(self.speed_y)  # Reverse vertical direction
                elif self.rect.bottom > 840:
                    self.speed_y = -abs(self.speed_y)  # Reverse vertical direction

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load the "boss_icon" image
        boss_icon = pygame.image.load("boss_icon.png").convert_alpha()

        # Resize the image to match the size of the boss's surface
        self.image = pygame.transform.scale(boss_icon, (100, 100))
        self.rect = self.image.get_rect()
        self.down = True
        self.health = 10

    def update(self):
        if self.down:
            self.rect.y -= 5
            if self.rect.y <= 50:
                self.down = False
        else:
            self.rect.y += 5
            # remove safe spot on hard mode
            if EASY:
                if self.rect.y >= 840-100:
                    self.down = True
            elif MEDIUM or HARD:
                if self.rect.y >= 840:
                    self.down = True

class Player(pygame.sprite.Sprite):
    def __init__(self, image_no):
        super().__init__()
        # Load the player's icon image
        original_image = pygame.image.load("player_icon.png").convert_alpha()
        green_image = pygame.image.load("player_icon_green.png").convert_alpha()
        yellow_image = pygame.image.load("player_icon_yellow.png").convert_alpha()
        red_image = pygame.image.load("player_icon_red.png").convert_alpha()

        # Define the desired width and height for the player's image
        desired_width = 96
        desired_height = 32

        # Resize the image to the desired dimensions
        if image_no == 1:
            self.image = pygame.transform.scale(original_image, (desired_width, desired_height))
            self.rect = self.image.get_rect()
        elif image_no == 2:
            self.image = pygame.transform.scale(green_image, (desired_width, desired_height))
            self.rect = self.image.get_rect()
        elif image_no == 3:
            self.image = pygame.transform.scale(yellow_image, (desired_width, desired_height))
            self.rect = self.image.get_rect()
        elif image_no == 4:
            self.image = pygame.transform.scale(red_image, (desired_width, desired_height))
            self.rect = self.image.get_rect()

    def update(self):
        if self.rect.y >= 780:
            pass
        else:
            self.rect.y += 5

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        bullets_icon = pygame.image.load("bullets.png").convert_alpha()
        self.image = pygame.transform.scale(bullets_icon, (15, 10))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += 10

class Big_bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        big_bullets_icon = pygame.image.load("bullets.png").convert_alpha()
        self.image = pygame.transform.scale(big_bullets_icon, (60, 40))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += 6

class Shoot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        shoot_icon = pygame.image.load("shoot_icon.png").convert_alpha()
        self.image = pygame.transform.scale(shoot_icon, (15, 10))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x -= 5

class Health_Animation(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        health_icon = pygame.image.load("healthplus_animation.png").convert_alpha()

        # Resize the image to match the size of the boss's surface
        self.image = pygame.transform.scale(health_icon, (30, 30))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y -= 3

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
        player = Player(1)
        player.rect.y = 400
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

def respawn_enemies():
    for x in range(10):
        enemy = Enemy()
        enemy_group.add(enemy)

def respawn_boss():
    boss = Boss()
    boss_group.add(boss)
    boss.rect.x = 1000
    boss.rect.y = 350

def backround_decoration(screen):
    pygame.draw.rect(screen, black, (0, 0, display_width, display_height))

    pygame.draw.rect(screen, darkBrown, (10, 10, display_width - 20, display_height - 20), 10)
    pygame.draw.rect(screen, lighterBrown, (20, 20, display_width - 40, display_height - 40), 5)

def health_symbols():
    # Create Health_Animation sprites
    for hpE1 in range(1):
        health_animation = Health_Animation()
        health_animation.rect.x = 200
        health_animation.rect.y = 150
        health_animation_group.add(health_animation)
    for hpE2 in range(1):
        health_animation = Health_Animation()
        health_animation.rect.x = 450
        health_animation.rect.y = 150
        health_animation_group.add(health_animation)
    respawn_enemies()

# -----Sprites----- # -------------------------------------------------------------------------------------------------------------------------------

pygame.init()

# sprite lists
all_sprites_list = pygame.sprite.Group()

enemy_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
big_bullet_group = pygame.sprite.Group()
shoot_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
health_animation_group = pygame.sprite.Group()

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

        # two back buttions on differnt screens
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b and controls_screen:
                controls_screen = False
                options_screen = True
            if event.key == pygame.K_b and accounts_screen:
                accounts_screen = False
                options_screen = True

        # moving the player
        if event.type == pygame.KEYDOWN:
            key_state[event.key] = True
        elif event.type == pygame.KEYUP:
            key_state[event.key] = False

        # exit menu and start game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and menu:
                menu = False
                restart_screen = False
                game = True
                phase1 = True

        # difficulty change
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

        # account change
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 and accounts_screen:
                ACC1 = True
                ACC2 = False
                ACC3 = False
            if event.key == pygame.K_2 and accounts_screen:
                ACC1 = False
                ACC2 = True
                ACC3 = False
            if event.key == pygame.K_3 and accounts_screen:
                ACC1 = False
                ACC2 = False
                ACC3 = True

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

        # Player clicks on one of the weapon buttons
        if weapon_selection:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if 100 <= mouse_x <= 400 and 100 <= mouse_y <= 700:
                    WBlue = False
                    WGreen = True
                    WYellow = False
                    WRed = False
                    weapon_selection = False
                    game = True
                    if EASY:
                        health_symbols()
                    if MEDIUM:
                        health_symbols()

                    #reset player to reset image (2)
                    for q in player_group:
                        player_group.remove(q)
                    player = Player(2)
                    player.rect.y = 400
                    player_group.add(player)
                    player.rect.x = 200

                if 485 <= mouse_x <= 785 and 100 <= mouse_y <= 700:
                    WBlue = False
                    WGreen = False
                    WYellow = True
                    WRed = False
                    weapon_selection = False
                    game = True
                    if EASY:
                        health_symbols()
                    if MEDIUM:
                        health_symbols()

                    #reset player to reset image (2)
                    for q in player_group:
                        player_group.remove(q)
                    player = Player(3)
                    player.rect.y = 400
                    player_group.add(player)
                    player.rect.x = 200

                if 870 <= mouse_x <= 1170 and 100 <= mouse_y <= 700:
                    WBlue = False
                    WGreen = False
                    WYellow = False
                    WRed = True
                    weapon_selection = False
                    game = True
                    if EASY:
                        health_symbols()
                    if MEDIUM:
                        health_symbols()

                    #reset player to reset image (2)
                    for q in player_group:
                        player_group.remove(q)
                    player = Player(4)
                    player.rect.y = 400
                    player_group.add(player)
                    player.rect.x = 200


    # --Menu-- # -------------------------------------------------------------------------------------------------------------------------------
    if menu == True:

        screen.fill(black)
        backround_decoration(screen)

        # game title
        screen.blit(game_title_icon, (380, 40))

        # pirate and alien decoration
        screen.blit(pirate, (80, 300))
        screen.blit(alien, (1040, 350))

        # epilepsy warning
        warning_text = warning_font.render("EPILEPSY WARNING!", 300, red)
        screen.blit(warning_text, (850, 720))

        # button variables
        button_width = 240
        button_height = 50
        button_x = (display_width - button_width) // 2 -10
        button_y = (display_height - button_height) // 2 + 280

        # start button
        start_button_rect = pygame.draw.rect(screen, red, pygame.Rect(button_x, button_y, button_width + 10, button_height))
        start_text = font.render("Press SPACE to start", True, white)
        start_text_rect = start_text.get_rect(center=start_button_rect.center)
        screen.blit(start_text, start_text_rect)

        # options button (on click)
        option_button_rect = pygame.draw.rect(screen, red, pygame.Rect(button_x, button_y + 75, button_width + 10, button_height))
        pygame.draw.rect(screen, red, option_button_rect)
        option_button_text = font.render("Options", True, white)
        text_rect = option_button_text.get_rect(center=option_button_rect.center)
        screen.blit(option_button_text, text_rect)

        # Handle mouse events for the back button
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if option_button_rect.collidepoint(event.pos):
                        options_screen = True
                        menu = False

        # leaderboard display
        leaderboard_title = big_font.render("Leaderboard rankings", True, titleColour)
        screen.blit(leaderboard_title, (550, 300))

        title_x = 400
        title_y = 330
        rankTitle = small_font.render("Rank", 300, darkerWhite)
        scoreTitle = small_font.render("Score", 300, darkerWhite)
        nameTitle = small_font.render("Account", 300, darkerWhite)
        diffTitle = small_font.render("Difficulty", 300, darkerWhite)
        screen.blit(rankTitle, (title_x,title_y))
        screen.blit(scoreTitle, (title_x + 150, title_y))
        screen.blit(nameTitle, (title_x + 300, title_y))
        screen.blit(diffTitle, (title_x + 450, title_y))

        records = read_records()
        start_y = 330
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
        backround_decoration(screen)

        if controls_screen:

            backround_decoration(screen)

            controls_title = big_font.render("Controls:", True, white)
            screen.blit(controls_title, (display_width // 2 - 50, 30))
            y_offset = 70
            for item in controls:
                text_surface = small_font.render(item, True, white)
                text_rect = text_surface.get_rect()
                text_rect.center = (display_width // 2 , y_offset)
                screen.blit(text_surface, text_rect)
                y_offset += 35

            # back button text
            start_text = font.render("< Back (b)", True, white)
            screen.blit(start_text, start_text_rect)

        elif accounts_screen:

            # Call the backrou decoration
            backround_decoration(screen)

            accounts = big_font.render("Accounts:", True, white)
            screen.blit(accounts, (display_width // 2 - 100, 45))

            account_name1 = small_font.render("1: Oli", True, white)
            screen.blit(account_name1, (500, 100))

            account_name2 = small_font.render("2: Ben", True, white)
            screen.blit(account_name2, (600, 100))

            account_name3 = small_font.render("3: Guest", True, white)
            screen.blit(account_name3, (700, 100))

            if ACC1:
                account_name1 = small_font.render("1: Oli", True, green)
                screen.blit(account_name1, (500, 100))
            elif ACC2:
                account_name2 = small_font.render("2: Ben", True, green)
                screen.blit(account_name2, (600, 100))
            elif ACC3:
                account_name3 = small_font.render("3: Guest", True, green)
                screen.blit(account_name3, (700, 100))

            # back button text
            start_text = font.render("< Back (b)", True, white)
            screen.blit(start_text, start_text_rect)

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
                difficulty_text2 = small_font.render("Medium", True, orange)
                screen.blit(difficulty_text2, (320, 100 + 3 * 50))
            if HARD:
                difficulty_text3 = small_font.render("Hard", True, red)
                screen.blit(difficulty_text3, (420, 100 + 3 * 50))


    # --Restart screen-- # -------------------------------------------------------------------------------------------------------------------------------
    elif restart_screen == True:

        screen.fill(black)

        # final score text
        finalScoreTxt = small_font.render(f"Final Score: {final_score}", False, white)
        screen.blit(finalScoreTxt, (10, 10))

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
        for h in big_bullet_group:
            big_bullet_group.remove(h)

        # reset flags
        added_boss = False
        added_player = False
        respawned = False
        phase1 = True
        phase2 = False

        # clear score
        temp_score = score
        score = 0

        # update leaderboard (select what account and difficulty from options screen)
        # account
        if ACC1:
            nombre = "Oli"
        elif ACC2:
            nombre = "Ben"
        elif ACC3:
            nombre = "Guest"

        # difficulty
        if EASY:
            temp_difficulty = "Easy"
        elif MEDIUM:
            temp_difficulty = "Medium"
        elif HARD:
            temp_difficulty = "Hard"

        # so only one record is added
        while flag == False:
            player_name = nombre
            player_score = temp_score
            player_difficulty = temp_difficulty
            update_leaderboard(player_name, player_score, player_difficulty)
            flag = True

    # --Game screen-- # -------------------------------------------------------------------------------------------------------------------------------
    elif game == True:

        if phase1:
            # Update and draw enemy sprites for the enemies phase
            enemy_group.update()
            enemy_group.draw(screen)

        elif phase2:
            # Update and draw boss sprite for the boss phase
            boss_group.update()
            boss_group.draw(screen)

        # Check if the player is still alive
        if player_health <= 0:
            restart_screen = True
            game = False
            dead = False
            player_health = 3
            for h in player_group:
                player_group.remove(h)
            # Skip the rest of the game logic
            continue

        # respawn boss only when enemies die
        if phase1 and enemies_dead >= 10:
            phase1 = False
            phase2 = True
            enemies_dead = 0
            if score > 10:
                respawn_boss()

        # When the boss dies on EASY and MEDIUM difficulties healing and switch phases (boss -> enemies)
        if EASY:
            if phase2 and boss.health <= 0:
                boss.health = 10  # Reset the boss's health
                player_health = min(player_health + 3, 3)  # Increase player's health to maximum, but not more than 3
                phase1 = True
                phase2 = False
                boss_group.remove(boss)
                all_sprites_list.remove(boss)
                weapon_selection = True # select weapon

        if MEDIUM:
            if phase2 and boss.health <= 0:
                boss.health = 10  # Reset the boss's health
                player_health = min(player_health + 1, 3)  # Increase player's health, but not more than 3
                phase1 = True
                phase2 = False
                boss_group.remove(boss)
                all_sprites_list.remove(boss)
                weapon_selection = True # select weapon

        if HARD:
            if phase2 and boss.health <= 0:
                boss.health = 10  # Reset the boss's health
                phase1 = True
                phase2 = False
                boss_group.remove(boss)
                all_sprites_list.remove(boss)
                weapon_selection = True # select weapon

        # backround design
        screen.fill(black)

        # score text
        scoreTxt = small_font.render(f"Score: {score}", False, white)
        screen.blit(scoreTxt, (10, 10))

        # update score for researt screen (final score)
        final_score = score

        # health bar border
        pygame.draw.rect(screen, yellow, (250, 10, 155, 30), width=3)
        # three seperate blocks for each health, linked to player_health
        if player_health == 3:
            pygame.draw.rect(screen, blue, (255, 15, 45, 20)) #1
            pygame.draw.rect(screen, blue, (305, 15, 45, 20)) #2
            pygame.draw.rect(screen, blue, (355, 15, 45, 20)) #3
        elif player_health == 2:
            pygame.draw.rect(screen, blue, (255, 15, 45, 20)) #1
            pygame.draw.rect(screen, blue, (305, 15, 45, 20)) #2
        elif player_health == 1:
            pygame.draw.rect(screen, blue, (255, 15, 45, 20)) #1

        # hold to rise up screen
        if key_held(pygame.K_w) and player.rect.y > 50:
            player.rect.y -= 10

        # player starts shooting
        bullet_timer = pygame.time.get_ticks()
        if WBlue:
            weapon_delay = 500 #10 for testing
        if WGreen:
            weapon_delay = 200
        if WYellow:
            weapon_delay = 2000
        if WRed:
            weapon_delay = 500

        if bullet_timer - last_shot_time >= weapon_delay and WYellow == False:
            bullet = Bullet()

            # Set the bullet so it is where the player is
            bullet.rect.x = player.rect.x
            bullet.rect.y = player.rect.y

            # Add the bullet to the lists
            bullet_group.add(bullet)

            # Reset the bullet timer
            last_shot_time = bullet_timer

        if bullet_timer - last_shot_time >= weapon_delay and WYellow == True:
            big_bullet = Big_bullet()

            # Set the bullet so it is where the player is
            big_bullet.rect.x = player.rect.x
            big_bullet.rect.y = player.rect.y

            # Add the bullet to the lists
            big_bullet_group.add(big_bullet)

            # Reset the bullet timer
            last_shot_time = bullet_timer

        # boss shooting
        if phase2:
            if EASY or MEDIUM:
                for boss in boss_group:
                    chance = random.randint(0, 10000)
                    if (chance % 10) == 0:
                        bossShoot = Shoot()
                        bossShoot.rect.x = boss.rect.x
                        bossShoot.rect.y = boss.rect.y
                        shoot_group.add(bossShoot)
            if HARD:
                for boss in boss_group:
                    chance = random.randint(0, 10000)
                    if (chance % 8) == 0:
                        bossShoot = Shoot()
                        bossShoot.rect.x = boss.rect.x
                        bossShoot.rect.y = boss.rect.y
                        shoot_group.add(bossShoot)

        # enemies shooting
        # EASY
        if EASY:
            for enemy in enemy_group:
                chance = random.randint(0, 10000)
                if (chance % 333) == 0:
                    shoot = Shoot()
                    shoot.rect.x = enemy.rect.x
                    shoot.rect.y = enemy.rect.y
                    shoot_group.add(shoot)

        # MEDIUM
        if MEDIUM:
            for enemy in enemy_group:
                chance = random.randint(0, 10000)
                if (chance % 100) == 0:
                    shoot = Shoot()
                    shoot.rect.x = enemy.rect.x
                    shoot.rect.y = enemy.rect.y
                    shoot_group.add(shoot)

        # HARD
        if HARD:
            for enemy in enemy_group:
                chance = random.randint(0, 10000)
                if (chance % 50) == 0:
                    shoot = Shoot()
                    shoot.rect.x = enemy.rect.x
                    shoot.rect.y = enemy.rect.y
                    shoot_group.add(shoot)

        if WYellow == False:
            # calculate mechanics for each bullet
            if phase1:

                for bullet in bullet_group:

                    # See if it hit a block
                    block_hit_list = pygame.sprite.spritecollide(bullet, enemy_group, True)

                    # For each block hit, remove the bullet and add to the score
                    for enemy in block_hit_list:
                        # Spawn explostion
                        if explode == True and WRed == True:
                            # draw explostion img
                            screen.blit(explotion, (enemy.rect.x-150, enemy.rect.y-150))
                            # Check if the explostion duration has passed
                            if current_time - explode_time >= explode_duration:
                                explode = False
                        bullet_group.remove(bullet)
                        all_sprites_list.remove(bullet)
                        score += 1
                        enemies_dead += 1

                        # enemies nearby get killed by the explotion
                        if WRed:
                            # Check for nearby enemies
                            for other_enemy in enemy_group:
                                if enemy != other_enemy:
                                    # Calculate the distance between the two enemies' centers
                                    distance = pygame.math.Vector2(enemy.rect.center).distance_to(other_enemy.rect.center)
                                    if distance <= 150:
                                        # Remove the nearby enemy
                                        enemy_group.remove(other_enemy)
                                        all_sprites_list.remove(other_enemy)
                                        score += 1
                                        enemies_dead += 1

                    # Remove the bullet if it flies up off the screen
                    if bullet.rect.x < -10 or bullet.rect.x > 1400:
                        bullet_group.remove(bullet)
                        all_sprites_list.remove(bullet)

            # boss getting hit and health (buffer is the time until the boss can be hit again)
            if phase2 and buffer == False:
                current_time = pygame.time.get_ticks()
                if current_time - last_hit_time >= buffer_time:
                    for bullet in bullet_group:
                        if bullet.rect.colliderect(boss.rect):
                            boss.health -= 1
                            score += 1
                            buffer = True
                            last_hit_time = current_time

        # reset buffer
        current_time = pygame.time.get_ticks()
        if current_time - last_hit_time >= buffer_time:
            buffer = False
            # reset explotion
            explode = True
            explode_time = current_time

        if WYellow == True:
            # calculate mechanics for each big_bullet
            if phase1:
                for big_bullets in big_bullet_group:

                    # See if it hit a block
                    block_hit_list_big = pygame.sprite.spritecollide(big_bullet, enemy_group, True)

                    # For each block hit, add to the score
                    for enemy in block_hit_list_big:
                        score += 1
                        enemies_dead += 1

                    # Remove the big_bullet if it flies up off the screen
                    if bullet.rect.x < -10 or bullet.rect.x > 1400:
                        big_bullet_group.remove(big_bullet)
                        all_sprites_list.remove(big_bullet)

            # boss getting hit and health (buffer is the time until the boss can be hit again) but for the big_bullet one shot
            if phase2 and buffer3 == False:
                current_time3 = pygame.time.get_ticks()
                if current_time3 - last_hit_time >= buffer_time:
                    for big_bullets in big_bullet_group:
                        if big_bullet.rect.colliderect(boss.rect):
                            boss.health -= 1
                            score += 1
                            buffer3 = True
                            last_hit_time = current_time3

        # reset buffer3
        current_time3 = pygame.time.get_ticks()
        if current_time3 - last_hit_time >= buffer_time:
            buffer3 = False

        # calculate mechanics for player being hit by the enemy (player health and being hit)
        current_timev2 = pygame.time.get_ticks()
        if buffer2 == False:
            for shoot in shoot_group:
                current_time = pygame.time.get_ticks()
                if current_time - last_hit_time2 >= buffer_time:
                    health_hit_list = pygame.sprite.spritecollide(shoot, player_group, False)
                    for player in health_hit_list:
                        shoot_group.remove(shoot)
                        all_sprites_list.remove(shoot)
                        player_health -= 1
                        buffer2 = True
                        # screen flash red when hit
                        if show_red_flash:
                            # Fill the screen with red
                            screen.fill((255, 0, 0))

                            # Check if the red flash duration has passed
                            if current_timev2 - red_flash_start_time >= red_flash_duration:
                                show_red_flash = False


                    if shoot.rect.x < -10 or shoot.rect.x > 1400:
                        shoot_group.remove(shoot)
                        all_sprites_list.remove(shoot)

        # reset buffer2
        current_time = pygame.time.get_ticks()
        if current_time - last_hit_time2 >= buffer_time:
            buffer2 = False
            # reset flash
            show_red_flash = True
            red_flash_start_time = current_timev2

        # player dies
        if player_health <= 0:
            dead = True

        # condition in game end
        if dead:
            restart_screen = True
            game = False
            dead = False
            player_health = 3
            WBlue = True
            WGreen = False
            WYellow = False
            WRed = False
            for h in player_group:
                player_group.remove(h)

        # choosing weapons pop-up
        if weapon_selection:
            # remove others sprites from screen
            game = False
            for e in bullet_group:
                bullet_group.remove(e)
            for f in shoot_group:
                shoot_group.remove(f)
            for g in health_animation_group:
                health_animation_group.remove(g)
            for h in big_bullet_group:
                big_bullet_group.remove(h)

            screen.fill(black)

            # show origonal ship
            player.rect. y = 740
            player_current_text = font.render("Current player:", 300, white)
            screen.blit(player_current_text, (10, 740))

            # draw pop-ups
            scoreTxt = small_font.render(f"Score: {score}", False, white)
            screen.blit(scoreTxt, (10, 10))

            screen.blit(green_button, (100, 100))
            screen.blit(yellow_button, (485, 100))
            screen.blit(red_button, (870, 100))


        # sprites update
        enemy_group.update()
        player_group.update()
        bullet_group.update()
        big_bullet_group.update()
        shoot_group.update()
        boss_group.update()
        health_animation_group.update()

        # respawing sprites to restart game
        if respawned == False:
            spawn()
            respawned = True

        # draw sprites
        bullet_group.draw(screen)
        big_bullet_group.draw(screen)
        shoot_group.draw(screen)
        health_animation_group.draw(screen)

        # Draw the player as long as health is greater than zero
        if player_health > 0:
            player_group.draw(screen)

        # Draw enemies when in the enemies phase
        if phase1:
            enemy_group.draw(screen)

        # Draw the boss when in the boss phase
        if phase2:
            boss_group.draw(screen)

        # flag for leaderboard score
        flag = False

    # updating the gamme window
    pygame.display.flip()
    clock.tick(75)
