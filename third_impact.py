import pygame
import time

pygame.init()

# Set up the window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Game")


# Set up the buttons
button_font = pygame.font.SysFont("Arial", 24)
button_texts = ["Attack 1", "Attack 2", "Attack 3", "Attack 4"]
button_images = []
button_rects = []
for i, text in enumerate(button_texts):
    button_image = button_font.render(text, True, (255, 255, 255))
    button_rect = button_image.get_rect(
        center=(
            WINDOW_WIDTH // 4 + ((i % 2) * (WINDOW_WIDTH // 2)),
            WINDOW_HEIGHT - (WINDOW_HEIGHT // 3) + ((i // 2) * 50),
        )
    )
    button_images.append(button_image)
    button_rects.append(button_rect)


# Set up the fighter images and rects for each fighter. In the future, this should happen inside class init, so we can have animations

player_figure_image = pygame.Surface((100, 100))
player_figure_image.fill((255, 0, 0))
player_figure_rect = player_figure_image.get_rect(
    center=(WINDOW_WIDTH // 3, WINDOW_HEIGHT // 2)
)


fighter2_figure_image = pygame.Surface((100, 100))
fighter2_figure_image.fill((0, 0, 255))
fighter2_figure_rect = fighter2_figure_image.get_rect(
    center=(2 * WINDOW_WIDTH // 3, WINDOW_HEIGHT // 2)
)


# Set up the attack animation
attack_image = pygame.Surface((100, 100))
attack_image.fill((255, 255, 0))
attack_rect = attack_image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

# Set up the timer
attack_time = 2000  # in milliseconds
attack_start_time = None

# Set up the game loop
clock = pygame.time.Clock()
running = True
show_menu = True
clock.tick(60)


class Fighter:
    all_fighters = []
    all_healthbars = []

    def __init__(self, image, idle, x, y, name, max_hp, strength, moves):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.idle = idle
        self.strength = strength
        self.moves = moves
        self.alive = True
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.healthbar = self.HealthBar(
            self.rect.x,
            0,
        )
        Fighter.all_fighters.append(self)

    class HealthBar:
        def __init__(self, x, y):
            self.image = pygame.Surface((100, 20))
            self.image.fill((0, 255, 0))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            Fighter.all_healthbars.append(self)

        def __str__(self):
            return "MyClass(x=" + str(self.rect.x) + " ,y=" + str(self.rect.y) + ")"


player = Fighter(
    player_figure_image,
    player_figure_image,
    200,
    200,
    "Fighter 1",
    100,
    10,
    ["Attack 1", "Attack 2"],
)
player.rect.x = 200
fighter2 = Fighter(
    fighter2_figure_image,
    fighter2_figure_image,
    250,
    200,
    "Fighter 2",
    120,
    8,
    ["Attack 1", "Attack 3"],
)

current_fighter = 0


fighter3 = Fighter(
    fighter2_figure_image,
    fighter2_figure_image,
    250,
    200,
    "Fighter 2",
    120,
    8,
    ["Attack 1", "Attack 3"],
)

for count, fighter in enumerate(Fighter.all_fighters):
    fighter.rect.x += count * 200
    fighter.healthbar.rect.x = fighter.rect.x

for bar in Fighter.all_healthbars:
    print(bar.rect.x)
# gameloop
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the user clicked on a button
            for i, button_rect in enumerate(button_rects):
                if button_rect.collidepoint(event.pos):
                    # Start the attack animation and timer
                    attack_start_time = pygame.time.get_ticks()
                    show_menu = False

    # Draw the fighters
    window.fill((0, 0, 0))
    for fighter in Fighter.all_fighters:
        window.blit(fighter.image, fighter.rect)
    # Draw the health bars
    if not show_menu:
        for bar in Fighter.all_healthbars:
            window.blit(bar.image, bar.rect)

    # Draw the buttons or the attack animation
    if show_menu:
        for button_image, button_rect in zip(button_images, button_rects):
            window.blit(button_image, button_rect)
    else:
        Fighter.all_fighters[current_fighter].image = attack_image
        if (
            attack_start_time is not None
            and pygame.time.get_ticks() - attack_start_time >= attack_time
        ):
            print(current_fighter)
            Fighter.all_fighters[current_fighter].image = Fighter.all_fighters[
                current_fighter
            ].idle
            current_fighter += 1
            if current_fighter == len(Fighter.all_fighters):
                current_fighter = 0
                for fighter in Fighter.all_fighters:
                    fighter.image = fighter.idle
                show_menu = True
                attack_start_time = None
                continue
            attack_start_time = pygame.time.get_ticks()

            Fighter.all_fighters[current_fighter].image = attack_image
    pygame.display.update()

pygame.quit()
