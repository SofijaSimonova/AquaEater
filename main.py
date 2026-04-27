import pygame
import random
import os

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Aqua Eater")

pygame.mixer.init()

eat_sound = pygame.mixer.Sound("assets/sounds/eat.wav")
game_over_sound = pygame.mixer.Sound("assets/sounds/game_over.wav")
victory_sound = pygame.mixer.Sound("assets/sounds/victory.wav")

folder_path_enemy = "assets/enemy_fish/"
enemies = []
for filename in os.listdir(folder_path_enemy):
    image = pygame.image.load(os.path.join(folder_path_enemy, filename))
    enemies.append(image)

booster_fish_names = ["armor_fish", "frenzy_fish", "speed_fish", "poison_fish"]

background_image = pygame.transform.scale(pygame.image.load("assets/background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))

def get_high_score():
    try:
        with open("data/high_score.txt", "r") as f:
            return int(f.read())
    except:
        return 0


def fish_selection_menu():
    high_score = get_high_score()

    font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 28)

    fish_options = [
        {"image": "assets/fish_skins/main_fish.png", "required_score": 0},
        {"image": "assets/fish_skins/glow.png", "required_score": 10},
        {"image": "assets/fish_skins/shark.png", "required_score": 30},
        {"image": "assets/fish_skins/skeleton.png", "required_score": 50},
    ]

    selected = 0
    lock_icon = pygame.image.load("assets/lock.png")
    lock_icon = pygame.transform.scale(lock_icon, (30, 30))

    while True:
        screen.blit(background_image, (0, 0))
        title = font.render("Select Your Fish", True, (255, 255, 255))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        for i, option in enumerate(fish_options):
            locked = high_score < option["required_score"]
            img = pygame.image.load(option["image"])
            img = pygame.transform.scale(img, (60, 60))
            x = 200 + i * 150
            y = 200

            if i == selected:
                pygame.draw.rect(screen, (255, 255, 0), (x - 5, y - 5, 70, 70), 3)

            screen.blit(img, (x, y))

            if locked:
                screen.blit(lock_icon, (x + 20, y + 70))
                shadow = small_font.render(f"Unlocks at {option['required_score']}", True, (0, 0, 0))
                shadow_rect = shadow.get_rect(center=(x + 30 + 1, y + 120 + 1))
                screen.blit(shadow, shadow_rect)

                required_text = small_font.render(f"Unlocks at {option['required_score']}", True, (255, 255, 255))
                text_rect = required_text.get_rect(center=(x + 30, y + 120))
                screen.blit(required_text, text_rect)

        instructions = small_font.render("<- -> to select | ENTER to confirm | ESC to quit", True, (200, 200, 200))
        screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, 500))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    selected = (selected + 1) % 4
                if event.key == pygame.K_LEFT:
                    selected = (selected - 1) % 4
                if event.key == pygame.K_RETURN:
                    if high_score >= fish_options[selected]["required_score"]:
                        return fish_options[selected]["image"]
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

def victory_screen(score):
    victory_sound.play()
    high_score = max(get_high_score(), score)
    if score > get_high_score():
        with open("data/high_score.txt", "w") as f:
            f.write(str(score))

    font_big = pygame.font.SysFont("comicsansms", 64)
    font_small = pygame.font.SysFont("comicsansms", 32)

    message = font_big.render("Congratulations!", True, (0, 255, 0))
    sub_message = font_small.render("You are the biggest fish in the sea!", True, (255, 255, 255))
    score_text = font_small.render(f"Score: {score}", True, (255, 255, 0))
    exit_text = font_small.render("Press R to Restart or Q to Quit", True, (200, 200, 200))

    waiting = True
    while waiting:
        screen.blit(background_image, (0, 0))
        screen.blit(message, (SCREEN_WIDTH // 2 - message.get_width() // 2, 150))
        screen.blit(sub_message, (SCREEN_WIDTH // 2 - sub_message.get_width() // 2, 220))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 300))
        screen.blit(exit_text, (SCREEN_WIDTH // 2 - exit_text.get_width() // 2, 400))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                    return
                elif event.key == pygame.K_q:
                    waiting = False
                    pygame.quit()
                    return

def game_over_screen(score):
    game_over_sound.play()
    high_score = max(get_high_score(), score)
    if score > get_high_score():
        with open("data/high_score.txt", "w") as f:
            f.write(str(score))

    font_big = pygame.font.SysFont("comicsansms", 72)
    font_small = pygame.font.SysFont("comicsansms", 36)

    game_over_text = font_big.render("GAME OVER", True, (255, 0, 0))
    score_text = font_small.render(f"Score: {score}", True, (255, 255, 255))
    high_score_text = font_small.render(f"High Score: {high_score}", True, (255, 255, 0))
    restart_text = font_small.render("Press R to Restart or Q to Quit", True, (200, 200, 200))

    waiting = True
    while waiting:
        screen.blit(background_image, (0, 0))

        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 150))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 250))
        screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, 300))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 400))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()  # Рестарт
                    return
                elif event.key == pygame.K_q:
                    waiting = False
                    pygame.quit()
                    return


class Main_Fish:
    def __init__(self, skin_path="assets/fish_skins/main_fish.png"):
        self.original_image_path = skin_path
        self.original_image = pygame.image.load(self.original_image_path)
        self.size = 40
        self.image = pygame.transform.scale(self.original_image, (self.size, self.size))
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2
        self.base_speed = 1
        self.speed = self.base_speed
        self.skin_change_time = None
        self.facing_left = False
        self.mode = ""
        self.mode_start_time = None
        self.current_skin_path = self.original_image_path

    def update_image(self):
        image = pygame.image.load(self.current_skin_path)
        image = pygame.transform.scale(image, (self.size, self.size))
        if self.facing_left:
            image = pygame.transform.flip(image, True, False)
        self.image = image

    def update_mode(self):
        if self.mode and self.mode_start_time:
            elapsed = pygame.time.get_ticks() - self.mode_start_time
            if elapsed > 5000:
                self.set_mode("")

    def draw_booster_timer(self):
        if self.mode and self.mode_start_time:
            elapsed = pygame.time.get_ticks() - self.mode_start_time
            remaining = max(0, 5000 - elapsed)
            seconds = remaining // 1000 + 1

            font = pygame.font.Font(None, 32)
            effect_name = self.mode.capitalize()
            text = font.render(f"{effect_name} ({seconds}s)", True, (255, 255, 255))
            shadow = font.render(f"{effect_name} ({seconds}s)", True, (0, 0, 0))

            screen.blit(shadow, (21, 21))
            screen.blit(text, (20, 20))

    def change_skin(self, new_image_path):
        self.current_skin_path = new_image_path
        self.update_image()
        self.skin_change_time = pygame.time.get_ticks()
        self.mode_start_time = pygame.time.get_ticks()

    def move(self, keys):
        old_facing = self.facing_left
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.x > 0:
            self.x -= self.speed
            self.facing_left = True
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.x < SCREEN_WIDTH - self.image.get_width():
            self.x += self.speed
            self.facing_left = False

        if old_facing != self.facing_left:
            self.update_image()

        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.y > 0:
            self.y -= self.speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.y < SCREEN_HEIGHT - self.image.get_height():
            self.y += self.speed

    def increase_size(self):
        self.size += 2
        self.original_image = pygame.image.load(self.original_image_path)
        self.update_image()

    def set_mode(self, mode_name):
        self.mode = mode_name
        if mode_name == "speed":
            self.speed = 3
        elif mode_name == "poisoned":
            self.speed = 0.5
        else:
            self.speed = self.base_speed
        if mode_name == "":
            self.current_skin_path = self.original_image_path
            self.update_image()
            self.skin_change_time = None
            self.mode_start_time = None

    def check_if_biggest(self, enemies):
        for enemy in enemies:
            if self.size < enemy.size:
                return False
        return True

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

class Booster_Fish:
    def __init__(self):
        self.name = random.choice(booster_fish_names)
        self.path = "assets/booster_fish/" + self.name + ".png"
        self.original_image = pygame.image.load(self.path)
        self.size = 60
        self.image = pygame.transform.scale(self.original_image, (self.size, self.size))
        self.x = 0 - self.image.get_width()
        self.y = random.randint(0, SCREEN_HEIGHT - self.image.get_height())
        self.speed = 0.7

    def move(self):
        self.x += self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

class Enemy_Fish:
    def __init__(self):
        self.original_image = random.choice(enemies)
        self.size = random.randint(20, 140)
        self.image = pygame.transform.scale(self.original_image, (self.size, self.size))
        self.x = 0 - self.image.get_width()
        self.y = random.randint(0, SCREEN_HEIGHT-self.image.get_height())
        self.speed = 0.5


    def move(self):
        self.x += self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


def main():
    running = True
    game_over = False
    score = 0
    time_elapsed = 0
    boosters = []
    enemies_fish = []
    selected_skin = fish_selection_menu()
    main_fish = Main_Fish(selected_skin)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(background_image, (0, 0))

        keys = pygame.key.get_pressed()

        if not game_over:
            time_elapsed += 1
            main_fish.move(keys)
            main_fish.update_mode()

        else:
            game_over_screen(score)
            return

        # Појавување на непријателски риби
        if random.random() < 0.005:
            enemies_fish.append(Enemy_Fish())

        # Појавување на booster риби
        if random.random() < 0.0002:
            boosters.append(Booster_Fish())

        # Движење и цртање непријателски риби
        for enemy in enemies_fish[:]:
            enemy.move()
            enemy.draw()
            if enemy.y > SCREEN_HEIGHT:
                enemies_fish.remove(enemy)

            collision = pygame.Rect(main_fish.x, main_fish.y, main_fish.size - 10, main_fish.size - 10).colliderect(
                pygame.Rect(enemy.x, enemy.y, enemy.size-10, enemy.size-10))

            if collision:
                if main_fish.size < enemy.size:
                    if main_fish.mode == "frenzy":
                        main_fish.increase_size()
                        score += 1
                        enemies_fish.remove(enemy)
                        eat_sound.play()

                        if main_fish.check_if_biggest(enemies_fish) and main_fish.size > 140:
                            victory_sound.play()
                            victory_screen(score)
                            return

                    elif main_fish.mode == "armored":
                        continue
                    else:
                        game_over = True
                else:
                    if main_fish.mode != "poisoned":
                        main_fish.increase_size()
                        score += 1
                        enemies_fish.remove(enemy)
                        eat_sound.play()

                        if main_fish.check_if_biggest(enemies_fish) and main_fish.size > 140:
                            victory_sound.play()
                            victory_screen(score)
                            return

        # Движење и цртање booster риби
        for booster in boosters[:]:
            booster.move()
            booster.draw()
            if booster.y > SCREEN_HEIGHT:
                boosters.remove(booster)

            collision = pygame.Rect(main_fish.x, main_fish.y, main_fish.size - 10, main_fish.size - 10).colliderect(
                pygame.Rect(booster.x, booster.y, booster.size, booster.size))

            if collision:
                # Играчот може да изеде booster само ако нема активен ефект
                if main_fish.mode == "":
                    if booster.name == "armor_fish":
                        main_fish.change_skin("assets/fish_modes/armored.png")
                        main_fish.set_mode("armored")

                    elif booster.name == "frenzy_fish":
                        main_fish.change_skin("assets/fish_modes/frenzy.png")
                        main_fish.set_mode("frenzy")

                    elif booster.name == "speed_fish":
                        main_fish.change_skin("assets/fish_modes/speed.png")
                        main_fish.set_mode("speed")

                    elif booster.name == "poison_fish":
                        main_fish.change_skin("assets/fish_modes/poisoned.png")
                        main_fish.set_mode("poisoned")
                        score = max(0, score - 5)

                    boosters.remove(booster)

        main_fish.draw()
        main_fish.draw_booster_timer()
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        score_shadow = font.render(f"Score: {score}", True, (0, 0, 0))
        score_x = SCREEN_WIDTH - score_text.get_width() - 20
        screen.blit(score_shadow, (score_x + 1, 19))
        screen.blit(score_text, (score_x, 18))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()




