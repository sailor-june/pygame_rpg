import pygame
import random
import menu_sys

pygame.init()
font = pygame.font.SysFont("Monaco", 26)
clock = pygame.time.Clock()
fps = 60
idle = True
# game_window
bottom_panel = 150
screen_width = 640
screen_height = 480 + bottom_panel
screen = pygame.display.set_mode((screen_width, screen_height))
run = True
pygame.display.set_caption("Battle")

current_fighter = 0

action_cooldown = 0
action_wait_time = 3000


font = pygame.font.SysFont("Monaco", 26)


red = (250, 0, 0)
green = (0, 250, 0)
blue = (0, 0, 250)


# background image
background_img = pygame.image.load("img/bg.png").convert_alpha()
panel_img = pygame.image.load("img/panel.png").convert_alpha()
button_img = pygame.image.load("img/button.png").convert_alpha()
pointer_img = pygame.image.load("img/pointer.png").convert_alpha()


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# draw bg
def draw_bg():
    screen.blit(background_img, (0, 0))


def draw_panel():
    screen.blit(panel_img, (0, screen_height - bottom_panel))

    # draw_text(f'{hero.name} HP: {hero.hp}', font, red, 100, screen_height-bottom_panel+10)
    # for count, i in enumerate(bunny_list):
    #     draw_text(f'{i.name} HP: {i.hp}', font, red, 400, (screen_height-bottom_panel+10) + count * 60)


class Fighter:
    all_fighters = []
    all_healthbars = []
    def __init__(self, x, y, name, max_hp, strength, moves):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.moves = moves
        self.alive = True
        # animation nightmare ahead
        self.update_time = pygame.time.get_ticks()
        self.animation_list = []
        self.frame_index = 0
        # 0 idle 1 attack 2 hurt 3 dead
        self.action = 0
        temp_list = []

        for i in range(7):
            img = pygame.image.load(f"img/{self.name}/idle/{i}.png")
            temp_list.append(img)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(7):
            img = pygame.image.load(f"img/{self.name}/hit/{i}.png")
            temp_list.append(img)

        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.healthbar = self.HealthBar(self.rect.x, 0, self)
        Fighter.all_fighters.append(self)

    def update(self):
        animation_cooldown = 100
        # handle animation

        # update sprite
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # restart animation
        if self.frame_index >= len(self.animation_list[self.action]):
            self.idle()

    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage
        print(f"{self.name}, attack {target.name}")

    def draw(self):
        screen.blit(self.image, self.rect)

    def imgflip(self):
        flip_image = pygame.transform.flip(self.image, True, False)
        self.image=flip_image

    class HealthBar:
        def __init__(self, x, y, fighter):
            self.rect = (1, 1)
           
            self.fighter = fighter 
            self.x = self.fighter.rect.x
            self.y = self.fighter.rect.y-50
            Fighter.all_healthbars.append(self)

        def draw(self):
            ratio = self.fighter.hp / self.fighter.max_hp
            pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
            pygame.draw.rect(screen, (0, 0, 250), (self.x, self.y, 150 * ratio, 20))


# instantiate fighters
greenboy = Fighter(400, 260, "green", 30, 10, 3)
blueboy = Fighter(460, 300, "blue", 30, 10, 2)
hero = Fighter(100, 300, "hero", 50, 20, 6)
bunny_list = [greenboy, blueboy]


atk_buttons = [
    menu_sys.Button(button_img, screen, 50, screen_height - bottom_panel + 15, "Atk1", lambda menu: menu.set_buttons(enemy_buttons) ),
    menu_sys.Button(button_img, screen, 220, screen_height - bottom_panel + 15, "atk2"),
    menu_sys.Button(button_img, screen, 50, screen_height - bottom_panel + 70, "atk3"),
    menu_sys.Button(
        button_img,
        screen,
        220,
        screen_height - bottom_panel + 70,
        "return",
        lambda menu: menu.set_buttons(main_buttons),
    ),
]


enemy_buttons = []

for count, fighter in enumerate(Fighter.all_fighters):
    if not fighter.name == "hero":
        enemy_buttons.append(menu_sys.Button(button_img, screen, 200+ count *200, screen_height - bottom_panel + 15, fighter.name, lambda *args, fighter=fighter : atk(Fighter.all_fighters, fighter)))

main_buttons = [
    menu_sys.Button(
        button_img,
        screen,
        50,
        screen_height - bottom_panel + 15,
        "Attack",
        lambda menu: menu.set_buttons(atk_buttons),
    ),
    menu_sys.Button(
        button_img, screen, 220, screen_height - bottom_panel + 15, "Defend"
    ),
    menu_sys.Button(button_img, screen, 50, screen_height - bottom_panel + 70, "Tech"),
    menu_sys.Button(button_img, screen, 220, screen_height - bottom_panel + 70, "Item"),
]


menu = menu_sys.Menu(screen, pointer_img, main_buttons)
show_menu=True
attack_start_time = None


def atk(fighters, target):
    current_fighter= 0
    global show_menu
    global attack_start_time
    show_menu=False
    for fighter in fighters:
        if fighter.name != "hero":
            print(Fighter.all_fighters[current_fighter].name)
            attack_start_time=pygame.time.get_ticks()
            fighter.attack(hero)
            if (
            attack_start_time is not None
            and pygame.time.get_ticks() - attack_start_time >= action_wait_time
            ):
                continue
        else: 
            attack_start_time=pygame.time.get_ticks()
            fighter.attack(target)   
        current_fighter += 1
        if current_fighter == len(Fighter.all_fighters):
            current_fighter = 0
            for fighter in Fighter.all_fighters:
                fighter.action=0
            show_menu = True
            attack_start_time = None
            menu.set_buttons(main_buttons)
            continue
        




while run:
    current_time = pygame.time.get_ticks()
    clock.tick(fps)

    # draw bg
    draw_bg()
    draw_panel()
    # draw fighters
    hero.imgflip()
    
    for fighter in Fighter.all_fighters:
            fighter.update()
            fighter.draw()

            
        
    if show_menu:
        menu.draw()
    else:
        for bar in Fighter.all_healthbars:
            bar.draw()
            Fighter.all_fighters[current_fighter].action = 1
        # if (
        #     attack_start_time is not None
        #     and pygame.time.get_ticks() - attack_start_time >= action_wait_time
        #     ):
        #     print(current_fighter)
        #     Fighter.all_fighters[current_fighter].action=0
        #     current_fighter += 1
        #     if current_fighter == len(Fighter.all_fighters):
        #         current_fighter = 0
        #         for fighter in Fighter.all_fighters:
        #             fighter.action=0
        #         show_menu = True
        #         attack_start_time = None
        # #         menu.set_buttons(main_buttons)
        # #         continue
            
        #     attack_start_time = pygame.time.get_ticks()
        #     Fighter.all_fighters[current_fighter].action=1
        #     # handle events

        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        else:
            menu.handle_event(event)

    pygame.display.update()


pygame.quit()