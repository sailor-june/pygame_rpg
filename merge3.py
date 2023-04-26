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
        self.target = None
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
        temp_list = []
        
        for i in range(7):
            img = pygame.image.load(f"img/{self.name}/dead/{i}.png")
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
        if self.hp <=0:
            self.action=2
        # update sprite
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # restart animation
        if self.frame_index >= len(self.animation_list[self.action]):
            self.idle()

    def idle(self):
        if self.alive == True:
            self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self):
        self.update_time = pygame.time.get_ticks()
        self.action = 1
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        self.target.hp -= damage
        self.frame_index = 0
        print(f"{self.name} attacks {self.target.name} for {damage}")
        if self.target.hp <= 0:
            self.target.alive = False
            for button in enemy_buttons:
                if button.text == self.target.name:
                    (enemy_buttons.remove(button))
        self.target = None

    def draw(self):
        screen.blit(self.image, self.rect)

    def imgflip(self):
        flip_image = pygame.transform.flip(self.image, True, False)
        self.image = flip_image

    class HealthBar:
        def __init__(self, x, y, fighter):
            self.rect = (1, 1)

            self.fighter = fighter
            self.x = self.fighter.rect.x
            self.y = self.fighter.rect.y - 50
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


def atk(target):
    global show_menu
    global attack_start_time
    for fighter in Fighter.all_fighters:
        if fighter.name == "hero":
            fighter.target = target
        else:
            fighter.target = hero
    print("its happening")
    show_menu = False
    attack_start_time = pygame.time.get_ticks()
def defend():
    print("defend")
    pass

atk_buttons = [
    menu_sys.Button(
        button_img,
        screen,
        50,
        screen_height - bottom_panel + 15,
        "Atk1",
        lambda menu: menu.set_buttons(enemy_buttons),
    ),
    menu_sys.Button(
        button_img,
        screen,
        250,
        screen_height - bottom_panel + 15,
        "atk2",
        lambda menu: menu.set_buttons(enemy_buttons),
    ),
    menu_sys.Button(
        button_img,
        screen,
        50,
        screen_height - bottom_panel + 70,
        "atk3",
        lambda menu: menu.set_buttons(enemy_buttons),
    ),
    
]


enemy_buttons = []

for count, fighter in enumerate(Fighter.all_fighters):
    if not fighter.name == "hero":
        enemy_buttons.append(
            menu_sys.Button(
                button_img,
                screen,
                50 + 200 * count,
                screen_height - bottom_panel + 15,
                fighter.name,
                lambda *args, fighter=fighter: atk(fighter),
            )
        )
main_buttons = [
    menu_sys.Button(
        button_img, screen, 50, screen_height - bottom_panel + 15, "Attack", lambda menu: menu.set_buttons(atk_buttons),),
    menu_sys.Button(button_img, screen, 250, screen_height - bottom_panel + 15, "Defend"),
    menu_sys.Button(button_img, screen, 50, screen_height - bottom_panel + 70, "Tech"),
    menu_sys.Button(button_img, screen, 250, screen_height - bottom_panel + 70, "Item"),
]


menu = menu_sys.Menu(screen, pointer_img, main_buttons, button_img)
show_menu = True
attack_start_time = None
round_start = None
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

    if (
        round_start is not None
        and pygame.time.get_ticks() - round_start >= action_wait_time
    ):
        round_start = None
    if show_menu:
        menu.draw()
        if round_start is not None:
            for bar in Fighter.all_healthbars:
                bar.draw()

    else:
        round_start = pygame.time.get_ticks()
        
        for bar in Fighter.all_healthbars:
            bar.draw()
        
        if current_fighter >= len(Fighter.all_fighters):
                current_fighter = 0
                for fighter in Fighter.all_fighters:
                    if fighter.alive == True:
                        fighter.action = 0
                    # else:
                    #     fighter.action = 2
                show_menu = True
                attack_start_time = None
                menu.set_buttons(main_buttons)
                continue
        
        if Fighter.all_fighters[current_fighter].alive == True:
            Fighter.all_fighters[current_fighter].action = 1
        else:
            Fighter.all_fighters[current_fighter].action = 2
            current_fighter+=1

        if (
            attack_start_time is not None
            and pygame.time.get_ticks() - attack_start_time >= action_wait_time
        ):
            # if Fighter.all_fighters[current_fighter].alive == True:
            Fighter.all_fighters[current_fighter].attack()
            
            print(current_fighter)

            current_fighter += 1
            

            attack_start_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        else:
            menu.handle_event(event)

    pygame.display.update()


pygame.quit()