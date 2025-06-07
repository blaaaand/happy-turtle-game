import pygame

class Turtle:
    def __init__(self):
        self.rect = pygame.Rect(100, 300, 50, 50)
        self.y_speed = 0
        self.gravity = 0.5
        self.jump_speed = -10
        self.is_jumping = False
        self.head_offset = 0
        self.head_offset_amount = 10  # Amount to move head up when jumping
        self.is_starting = False

    def jump(self):
        # When jumping, set head offset and vertical speed
        self.is_jumping = True
        self.y_speed = self.jump_speed
        
    def update(self):
        # Apply gravity
        self.y_speed += self.gravity
        self.rect.y += self.y_speed
        
        # Reset jumping state when falling back down
        if self.y_speed > 0:  # If falling
            self.is_jumping = False
        
        # Check boundaries
        if self.rect.top < 0:
            self.rect.top = 0
            self.y_speed = 0
            self.is_jumping = False
            return True
        if self.rect.bottom > 590:
            self.rect.bottom = 590
            self.y_speed = 0

    def draw_normal(self, screen):
        # Draw head first (top layer)
        head_y = self.rect.y + 10  # Base head position
        head_x = self.rect.x + 45  # Base head position
        
        # Draw head and eye
        pygame.draw.circle(screen, (0, 255, 0), (head_x, head_y), 10)  # Head
        pygame.draw.circle(screen, (255, 255, 255), (head_x, head_y), 3)  # White eye
        pygame.draw.circle(screen, (0, 0, 0), (head_x, head_y), 1)  # Black pupil
        
        # Draw shell second (middle layer)
        pygame.draw.ellipse(screen, (100, 60, 0), (self.rect.x, self.rect.y - 10, 50, 20))  # Shell
        
        # Draw legs last (bottom layer)
        pygame.draw.circle(screen, (0, 255, 0), (self.rect.x + 15, self.rect.y + 5), 5)  # Front leg
        pygame.draw.circle(screen, (0, 255, 0), (self.rect.x + 35, self.rect.y + 5), 5)  # Back leg

    def draw_jumping(self, screen):
        # Draw head first (top layer)
        head_y = self.rect.y + 10 - self.head_offset_amount  # Move head up
        head_x = self.rect.x + 45  # Base head position
        
        # Draw head and eye
        pygame.draw.circle(screen, (0, 255, 0), (head_x, head_y), 10)  # Head
        pygame.draw.circle(screen, (255, 255, 255), (head_x, head_y), 3)  # White eye
        pygame.draw.circle(screen, (0, 0, 0), (head_x, head_y), 1)  # Black pupil
        
        # Draw shell second (middle layer)
        pygame.draw.ellipse(screen, (100, 60, 0), (self.rect.x, self.rect.y - 10, 50, 20))  # Shell
        
        # Draw legs last (bottom layer)
        pygame.draw.circle(screen, (0, 255, 0), (self.rect.x + 15, self.rect.y + 5), 5)  # Front leg
        pygame.draw.circle(screen, (0, 255, 0), (self.rect.x + 35, self.rect.y + 5), 5)  # Back leg

    def draw(self, screen):
        if self.is_jumping:
            self.draw_jumping(screen)
        else:
            self.draw_normal(screen)

    def start_game(self):
        """Called when game starts to reset"""
        self.rect.y = 300
        self.y_speed = 0
        self.is_jumping = False
        self.head_offset = 0
        self.is_starting = False
