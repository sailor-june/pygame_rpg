import pygame
import time

pygame.init()

# Set up the window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Game')

# Set up the figure
figure_image = pygame.Surface((100, 100))
figure_image.fill((255, 0, 0))
figure_rect = figure_image.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))

# Set up the health bar
health_bar_image = pygame.Surface((300, 20))
health_bar_image.fill((0, 255, 0))
health_bar_rect = health_bar_image.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))

# Set up the buttons
button_font = pygame.font.SysFont('Arial', 24)
button_texts = ['Attack 1', 'Attack 2', 'Attack 3', 'Attack 4']
button_images = []
button_rects = []


for i, text in enumerate(button_texts):
    button_image = button_font.render(text, True, (255, 255, 255))
    button_rect = button_image.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + i*50))
    button_images.append(button_image)
    button_rects.append(button_rect)

# Set up the attack animation
attack_image = pygame.Surface((100, 100))
attack_image.fill((255, 255, 0))
attack_rect = attack_image.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))

# Set up the timer
attack_time = 2000  # in milliseconds
attack_start_time = None

# Set up the game loop
clock = pygame.time.Clock()
running = True
show_menu = True

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
                    break

    # Draw the figure
    window.fill((0, 0, 0))
    window.blit(figure_image, figure_rect)

    # Draw the health bar
    if not show_menu:
        window.blit(health_bar_image, health_bar_rect)

    # Draw the buttons or the attack animation
    if show_menu:
        for button_image, button_rect in zip(button_images, button_rects):
            window.blit(button_image, button_rect)
    else:
        window.blit(attack_image, attack_rect)

    # Check if the attack animation is finished
    if attack_start_time is not None and pygame.time.get_ticks() - attack_start_time >= attack_time:
        show_menu = True
        attack_start_time = None

    pygame.display.update()
    clock.tick(60)

pygame.quit()