import pygame
pygame.init()

red=(250, 0, 0)
green = (0, 250, 0)
blue = (0, 0, 250)

font = pygame.font.SysFont('Monaco', 26)

def draw_text(text, surface, font,text_col,x,y):
    img = font.render(text, True, text_col)
    surface.blit(img,(x,y))


class Pointer():

    def __init__(self, surface, image, x, y,):
        
        self.image = pygame.transform.scale_by(image, (2, 2))
        self.surface = surface
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def update_position(self, current_button):
        self.rect.topleft = (buttons[current_button].rect.x - self.rect.width - 5, buttons[current_button].rect.y + 5)

    def draw(self):
        self.surface.blit(self.image, (self.rect.x, self.rect.y))
        return 
    
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
    def __init__(self, screen, pointer, buttons):
        self.screen = screen
        self.pointer_img= pointer
        self.buttons = buttons
        self.current_button = 0
        self.pointer = Pointer(screen, pointer, self.buttons[self.current_button].rect.x- 60, self.buttons[self.current_button].rect.y)
        
    def draw(self):
        for button in self.buttons:
            if hasattr(button, 'hp'):
                button.draw(button.hp)
            else:
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
            self.pointer.rect.x = self.buttons[self.current_button].rect.x - self.pointer.rect.width - 20
            self.pointer.rect.y = self.buttons[self.current_button].rect.y + 5

            # handle button click
            if event.key == pygame.K_x:
                for bar in Fighter.all_healthbars:
                    window.blit(bar.image, bar.rect)

    def set_buttons(self, buttons):   
        
        self.buttons = buttons
        self.current_button = 0
       
