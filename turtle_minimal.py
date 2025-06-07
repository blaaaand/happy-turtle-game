import pygame

class Turtle:
    def __init__(self):
        self.rect = pygame.Rect(100, 300, 50, 50)
        self.color = (0, 150, 0)  # Green color
        self.y_speed = 0
        self.gravity = 0.5
        self.jump_speed = -10
        
    def jump(self):
        self.y_speed = self.jump_speed
        
    def update(self):
        # Apply gravity
        self.y_speed += self.gravity
        self.rect.y += self.y_speed
        
        # Check boundaries
        if self.rect.top < 0:
            self.rect.top = 0
            self.y_speed = 0
            return True
        if self.rect.bottom > 600:
            self.rect.bottom = 600
            self.y_speed = 0
            return True
        return False
        
    def draw(self, screen):
        # Draw turtle body
        pygame.draw.ellipse(screen, self.color, self.rect)
        # Draw eyes
        pygame.draw.circle(screen, (255, 255, 255), (self.rect.x + 20, self.rect.y + 15), 5)
        pygame.draw.circle(screen, (255, 255, 255), (self.rect.x + 30, self.rect.y + 15), 5)
        pygame.draw.circle(screen, (0, 0, 0), (self.rect.x + 20, self.rect.y + 15), 2)
        pygame.draw.circle(screen, (0, 0, 0), (self.rect.x + 30, self.rect.y + 15), 2)
        # Draw shell
        pygame.draw.ellipse(screen, (100, 60, 0), (self.rect.x, self.rect.y - 20, 50, 30))
