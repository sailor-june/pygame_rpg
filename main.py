import pygame
import random
import button

pygame.init()

clock = pygame.time.Clock()
fps = 60

# game_window
bottom_panel = 150
screen_width = 640
screen_height = 480 + bottom_panel
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption('Battle')

current_fighter=1
total_fighters = 3
action_cooldown = 0
action_wait_time=90

font= pygame.font.SysFont('Times New Roman', 26)

red=(250, 0, 0)
green = (0, 250, 0)
blue = (0, 0, 250)


# load images
potion_img=pygame.image.load("img/potion.png")
# background image
background_img = pygame.image.load("img/bg.png").convert_alpha()
panel_img = pygame.image.load("img/panel.png").convert_alpha()



def draw_text(text,font,text_col,x,y):
    img = font.render(text, True, text_col)
    screen.blit(img,(x,y))

# draw bg
def draw_bg():
    screen.blit(background_img, (0, 0))


def draw_panel():
    screen.blit(panel_img, (0, screen_height - bottom_panel))

    draw_text(f'{hero.name} HP: {hero.hp}', font, red, 100, screen_height-bottom_panel+10)
    for count, i in enumerate(bunny_list):
        draw_text(f'{i.name} HP: {i.hp}', font, red, 400, (screen_height-bottom_panel+10) + count * 60)
run = True


class Fighter():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.update_time = pygame.time.get_ticks()
        self.alive = True
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
        rand=random.randint(-5,5)
        damage = self.strength + rand
        target.hp -= damage


    def draw(self):
        screen.blit(self.image, self.rect)

    def imgflip(self):
        flip_image = pygame.transform.flip(self.image, True, False)
        screen.blit(flip_image, self.rect)

class HealthBar():
    def __init__(self,x,y,hp,max_hp):
        self.x=x
        self.y=y
        self.hp=hp
        self.max_hp=max_hp

    def draw(self, hp):
        self.hp=hp
        ratio= self.hp/self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, (0,0,250), (self.x, self.y, 150*ratio, 20))






greenboy = Fighter(400, 260, 'green', 30, 10, 3)
blueboy = Fighter(460, 300, 'blue', 30, 10, 2)
hero = Fighter(100, 300, 'hero', 50, 20, 6)

bunny_list = [greenboy, blueboy]

hero_bar = HealthBar(100, (screen_height - bottom_panel + 40), hero.hp, hero.max_hp)

print(bunny_list)
bunny_bars = {}
for count, Fighter in enumerate(bunny_list):
    y = screen_height - bottom_panel + 40 + count * 60
    bunny_bars[Fighter.name + '_bar'] = HealthBar(400, y, Fighter.hp, Fighter.max_hp)



# potion_button = button.Button(screen, 100, screen_height-bottom_panel +70, potion_img, 32,32)
#



while run:

    clock.tick(fps)

    # draw bg
    draw_bg()
    draw_panel()
    hero_bar.draw(hero.hp)
    for bunny in bunny_list:
        bunny_bars[bunny.name + '_bar'].draw(bunny.hp)


    # draw fighters
    hero.update()
    hero.imgflip()
    for bunny in bunny_list:
        bunny.update()
        bunny.draw()

    # action
    if hero.alive==True:
        if current_fighter == 1:
            action_cooldown +=1
            if action_cooldown >= action_wait_time:
                #look for action
                #attack
                hero.attack(blueboy)
                current_fighter+=1
                action_cooldown=0
    for count, bunny in enumerate(bunny_list):
        if current_fighter == 2+ count:
            if bunny.alive == True:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    # look for action
                    # attack
                    bunny.attack(hero)
                    current_fighter += 1
                    action_cooldown = 0
            else:
                current_fighter +=1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit
