import pygame
pygame.init()

red=(250, 0, 0)
green = (0, 250, 0)
blue = (0, 0, 250)
bottom_panel = 150
screen_width = 640
screen_height = 480 + bottom_panel
font = pygame.font.SysFont('Monaco', 26)

def draw_text(text, surface, font,text_col,x,y):
    img = font.render(text, True, text_col)
    surface.blit(img,(x,y))



    
class Button():

    def __init__(self, image, surface, x, y, text, action=None):
        
        self.image = pygame.transform.scale_by(image, (2,2))
        self.rect = self.image.get_rect()
        self.text = text
        self.rect.topleft = (x, y)
        self.active = False
        self.clicked = False
        self.action = action
        self.surface = surface

    def draw(self):
        self.surface.blit(self.image,(self.rect.x, self.rect.y))
        draw_text(self.text, self.surface, font, blue, self.rect.x + 10, self.rect.y+ 10)
        return
    
class Menu:
    
    def __init__(self, screen, pointer_img, buttons, button_img):
        self.screen = screen
        self.pointer_img= pointer_img
        self.buttons = buttons
        self.button_img=button_img
        self.current_button = 0
        self.pointer = Menu.Pointer(self.screen, self.pointer_img, self.buttons[self.current_button].rect.x- 50, self.buttons[self.current_button].rect.y)
        self.main_buttons = [
    Button(
        self.button_img, self.screen, 50, screen_height - bottom_panel + 15, "Attack", lambda menu: menu.set_buttons(atk_buttons),),
    Button(self.button_img, self.screen, 250, screen_height - bottom_panel + 15, "Defend"),
    Button(self.button_img, self.screen, 50, screen_height - bottom_panel + 70, "Tech"),
    Button(self.button_img, self.screen, 250, screen_height - bottom_panel + 70, "Item"),
]    
    def draw(self):
        for button in self.buttons:
                button.draw()
                self.pointer.draw()
        

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                if self.current_button %2==0:
                    self.current_button +=1
                else: 
                    self.current_button -=1
            elif event.key == pygame.K_UP:
                self.current_button -= 2
                if self.current_button < 0:
                    self.current_button = len(self.buttons)-self.current_button*-1
            elif event.key == pygame.K_DOWN:
                self.current_button += 2
                if self.current_button > len(self.buttons) - 1:
                    self.current_button = self.current_button - len(self.buttons)

            # update pointer position
            self.pointer.rect.x = self.buttons[self.current_button].rect.x - 50
            self.pointer.rect.y = self.buttons[self.current_button].rect.y 

            # handle button click
            if event.key == pygame.K_x:
                self.buttons[self.current_button].action(self)

    def set_buttons(self, buttons):   
        self.buttons = buttons
        if "return" not in [button.text for button in self.buttons] and len(self.buttons)<4:
            self.buttons.append(Button(
            self.button_img,
            self.screen,
            250,
            screen_height - bottom_panel + 70,
            "return",
            lambda menu: menu.set_buttons(self.main_buttons),
            ),)
        for count, button in enumerate(self.buttons):
            if count % 2 == 0: 
                button.rect.x=50
                
            else:
                button.rect.x=250
            if count > 1:
                button.rect.y = screen_height - bottom_panel + 70
            else:
                screen_height - bottom_panel + bottom_panel*0.25
        self.current_button = 0
    class Pointer():

        def __init__(self, surface, image, x, y,):
            
            self.image = pygame.transform.scale_by(image, (2, 2))
            self.surface = surface
            self.x = x
            self.y = y
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)

        def update_position(self, current_button):
            self.rect.topleft = (self.buttons[current_button].rect.x - self.rect.width - 5, self.buttons[current_button].rect.y + 5)

        def draw(self):
            self.surface.blit(self.image, (self.rect.x, self.rect.y))
            return 


