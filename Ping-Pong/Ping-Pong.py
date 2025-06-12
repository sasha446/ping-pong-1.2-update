import pygame
import sys
import random
import os

pygame.init()
WIDTH, HEIGHT = 1300, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Мой Ping Pong")
clock = pygame.time.Clock()

MENU = 0
GAME = 1
SETTINGS = 2
game_state = MENU

settings = {
    "sound": True,
    "music": True,
    "current_ball_skin": 1,
    "background": None
}

font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)
menu_font = pygame.font.Font(None, 48)

def load_resources():
    resources = {
        "images": {},
        "sounds": {}
    }
    
    try:
        resources["images"]["background"] = pygame.image.load("background.jpg").convert()
        resources["images"]["background"] = pygame.transform.scale(resources["images"]["background"], (WIDTH, HEIGHT))
    except:
        resources["images"]["background"] = None
    
    try:
        pygame.mixer.init()
        resources["sounds"]["hit"] = pygame.mixer.Sound("hit.wav")
        pygame.mixer.music.load("background_music.mp3")
        pygame.mixer.music.set_volume(0.5)
    except Exception as e:
        resources["sounds"]["hit"] = None
    
    try:
        resources["images"]["paddle"] = pygame.image.load("paddle.png").convert_alpha()
        resources["images"]["paddle"] = pygame.transform.scale(resources["images"]["paddle"], 
                                                           (resources["images"]["paddle"].get_width()//4, 
                                                            resources["images"]["paddle"].get_height()//4))
        
        ball_skins = ["ball.png", "ball2.png", "ball3.png"]
        for i, skin in enumerate(ball_skins, 1):
            try:
                resources["images"][f"ball_{i}"] = pygame.image.load(skin).convert_alpha()
                resources["images"][f"ball_{i}"] = pygame.transform.scale(resources["images"][f"ball_{i}"], 
                                                                      (resources["images"][f"ball_{i}"].get_width()//5, 
                                                                       resources["images"][f"ball_{i}"].get_height()//5))
            except:
                pass
    except Exception as e:
        sys.exit()
    
    return resources

resources = load_resources()

def init_game():
    global player1, player2, ball, ball_speed_x, ball_speed_y, score_left, score_right
    
    paddle_img = resources["images"]["paddle"]
    ball_img = resources["images"].get(f"ball_{settings['current_ball_skin']}", resources["images"].get("ball_1"))
    
    player1 = paddle_img.get_rect(left=10, centery=HEIGHT//2)
    player2 = paddle_img.get_rect(right=WIDTH-10, centery=HEIGHT//2)
    ball = ball_img.get_rect(center=(WIDTH//2, HEIGHT//2))
    
    ball_speed_x = 7 * random.choice((1, -1))
    ball_speed_y = 7 * random.choice((1, -1))
    
    score_left = 0
    score_right = 0

init_game()

class Button:
    def __init__(self, x, y, width, height, text, color=(100, 100, 100), hover_color=(150, 150, 150)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
    
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        
        text_surf = menu_font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
    
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

start_button = Button(WIDTH//2 - 100, HEIGHT//2 - 100, 200, 50, "Начать игру")
settings_button = Button(WIDTH//2 - 100, HEIGHT//2, 200, 50, "Настройки")
exit_button = Button(WIDTH//2 - 100, HEIGHT//2 + 100, 200, 50, "Выход")
back_button = Button(50, HEIGHT - 100, 200, 50, "Назад")

sound_toggle = Button(WIDTH//2 - 100, 200, 200, 50, "Звук: Вкл")
music_toggle = Button(WIDTH//2 - 100, 300, 200, 50, "Музыка: Вкл")
ball_skin_button = Button(WIDTH//2 - 100, 400, 200, 50, "Скин мяча: 1")

while True:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if game_state == MENU:
            start_button.check_hover(mouse_pos)
            settings_button.check_hover(mouse_pos)
            exit_button.check_hover(mouse_pos)
            
            if start_button.is_clicked(mouse_pos, event):
                game_state = GAME
            elif settings_button.is_clicked(mouse_pos, event):
                game_state = SETTINGS
            elif exit_button.is_clicked(mouse_pos, event):
                pygame.quit()
                sys.exit()
        
        elif game_state == SETTINGS:
            back_button.check_hover(mouse_pos)
            sound_toggle.check_hover(mouse_pos)
            music_toggle.check_hover(mouse_pos)
            ball_skin_button.check_hover(mouse_pos)
            
            if back_button.is_clicked(mouse_pos, event):
                game_state = MENU
            elif sound_toggle.is_clicked(mouse_pos, event):
                settings["sound"] = not settings["sound"]
                sound_toggle.text = f"Звук: {'Вкл' if settings['sound'] else 'Выкл'}"
            elif music_toggle.is_clicked(mouse_pos, event):
                settings["music"] = not settings["music"]
                music_toggle.text = f"Музыка: {'Вкл' if settings['music'] else 'Выкл'}"
                if settings["music"]:
                    pygame.mixer.music.play(-1)
                else:
                    pygame.mixer.music.stop()
            elif ball_skin_button.is_clicked(mouse_pos, event):
                settings["current_ball_skin"] = settings["current_ball_skin"] % 3 + 1
                ball_skin_button.text = f"Скин мяча: {settings['current_ball_skin']}"
                init_game()
        
        elif game_state == GAME:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = MENU
                elif event.key == pygame.K_m:
                    settings["music"] = not settings["music"]
                    if settings["music"]:
                        pygame.mixer.music.play(-1)
                    else:
                        pygame.mixer.music.stop()
    
    if resources["images"]["background"]:
        screen.blit(resources["images"]["background"], (0, 0))
    else:
        screen.fill((0, 0, 0))
    
    if game_state == MENU:
        title = font.render("Ping Pong", True, (255, 255, 255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        
        start_button.draw(screen)
        settings_button.draw(screen)
        exit_button.draw(screen)
        
        hint = small_font.render("Нажмите ESC в игре для возврата в меню", True, (255, 255, 255))
        screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT - 50))
    
    elif game_state == SETTINGS:
        title = font.render("Настройки", True, (255, 255, 255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        
        sound_toggle.draw(screen)
        music_toggle.draw(screen)
        ball_skin_button.draw(screen)
        back_button.draw(screen)
    
    elif game_state == GAME:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player1.top > 0:
            player1.y -= 8
        if keys[pygame.K_s] and player1.bottom < HEIGHT:
            player1.y += 8
        if keys[pygame.K_UP] and player2.top > 0:
            player2.y -= 8
        if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
            player2.y += 8
        
        ball.x += ball_speed_x
        ball.y += ball_speed_y
        
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1
        
        if ball.colliderect(player1) or ball.colliderect(player2):
            ball_speed_x *= -1
            if settings["sound"] and resources["sounds"]["hit"]:
                resources["sounds"]["hit"].play()
        
        if ball.left <= 0:
            score_right += 1
            ball.center = (WIDTH//2, HEIGHT//2)
            ball_speed_x = 7 * random.choice((1, -1))
            ball_speed_y = 7 * random.choice((1, -1))
        
        if ball.right >= WIDTH:
            score_left += 1
            ball.center = (WIDTH//2, HEIGHT//2)
            ball_speed_x = 7 * random.choice((1, -1))
            ball_speed_y = 7 * random.choice((1, -1))
        
        screen.blit(resources["images"]["paddle"], player1)
        screen.blit(resources["images"]["paddle"], player2)
        ball_img = resources["images"].get(f"ball_{settings['current_ball_skin']}", resources["images"].get("ball_1"))
        screen.blit(ball_img, ball)
        
        score_text = font.render(f"{score_left} - {score_right}", True, (255, 255, 255))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 10))
        
        settings_hint = small_font.render("ESC: Меню", True, (255, 255, 255))
        screen.blit(settings_hint, (WIDTH - settings_hint.get_width() - 20, 20))
    
    pygame.display.flip()
    clock.tick(60)