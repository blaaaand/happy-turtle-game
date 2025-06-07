import pygame
import sys
import time

class Turtle:
    def __init__(self):
        self.rect = pygame.Rect(100, 300, 50, 50)  # Start in middle of screen
        self.y_speed = 0
        self.gravity = 0.3  # Floaty gravity
        
    def update(self):
        self.y_speed += self.gravity
        self.rect.y += self.y_speed
        
        # Keep turtle on screen
        if self.rect.y > 500:
            self.rect.y = 500
            self.y_speed = 0
        elif self.rect.y < 0:
            self.rect.y = 0
            self.y_speed = 0
            
    def jump(self):
        self.y_speed = -8  # Floaty jump
    
    def draw(self, screen):
        # Draw head first (bottom layer)
        pygame.draw.circle(screen, (0, 255, 0), (self.rect.x + 62, self.rect.y + 5), 10)  # Head
        pygame.draw.circle(screen, (255, 255, 255), (self.rect.x + 62, self.rect.y + 5), 3)  # White eye
        pygame.draw.circle(screen, (0, 0, 0), (self.rect.x + 62, self.rect.y + 5), 1)  # Black pupil
        
        # Draw shell (top layer)
        pygame.draw.ellipse(screen, (100, 60, 0), (self.rect.x - 5, self.rect.y - 15, 60, 30))  # Shell
        
        # Draw legs (bottom layer)
        pygame.draw.circle(screen, (0, 255, 0), (self.rect.x + 10, self.rect.y + 15), 6)  # Front leg
        pygame.draw.circle(screen, (0, 255, 0), (self.rect.x + 40, self.rect.y + 15), 6)  # Back leg

def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Happy Turtle")
    clock = pygame.time.Clock()
    
    # Create turtle
    turtle = Turtle()
    
    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    turtle.jump()
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                turtle.jump()
                
        # Update
        turtle.update()
        
        # Draw
        screen.fill((135, 206, 235))  # Sky blue background
        turtle.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
