import pygame
from game_config import Config

class Turtle:
    def __init__(self, skin='default'):
        self.skin = skin
        self.rect = pygame.Rect(100, Config.SCREEN_HEIGHT // 2, Config.TURTLE_WIDTH, Config.TURTLE_HEIGHT)
        self.y_speed = 0
        self.gravity = Config.GRAVITY
        self.jump_speed = Config.JUMP_SPEED
        self.skin_color = Config.TURTLE_COLOR
        
    def jump(self):
        self.velocity = Config.JUMP_STRENGTH
        
    def update(self):
        if self.is_jumping:
            self.velocity = 0
            self.is_jumping = False
        else:
            self.velocity += Config.GRAVITY
        
        self.velocity = min(self.velocity, Config.MAX_FALL_SPEED)
        self.rect.y += self.velocity
        
        # Check for boundary collisions
        if self.rect.y < 0 or self.rect.y > Config.SCREEN_HEIGHT - self.rect.height:
            return True
        
        return False
    
    def reset(self):
        self.rect.x = 100
        self.rect.y = Config.SCREEN_HEIGHT // 2
        self.velocity = 0
        self.is_jumping = False
            
    def reset(self):
        self.rect.y = Config.SCREEN_HEIGHT // 2
        self.velocity = 0
        self.is_jumping = False
        self.rect.x = 100
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
    def check_collision(self, obstacle):
        return self.rect.colliderect(obstacle.rect)
