import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Working Turtle")

clock = pygame.time.Clock()

# Colors
blue = (0, 0, 255)
white = (255, 255, 255)

class Turtle:
    def __init__(self):
        self.rect = pygame.Rect(100, 300, 50, 50)
        self.y_speed = 0
        self.gravity = 0.5
        self.is_alive = True
        
    def jump(self):
        self.y_speed = -10
        
    def update(self):
        if self.is_alive:
            self.y_speed += self.gravity
            self.rect.y += self.y_speed
            
            # Keep turtle on screen
            if self.rect.top < 0:
                self.rect.top = 0
                self.y_speed = 0
                self.is_alive = False
            if self.rect.bottom > 600:
                self.rect.bottom = 600
                self.y_speed = 0
                self.is_alive = False
                
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)

def game_loop():
    turtle = Turtle()
    game_over = False
    
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game_over:
                        turtle.jump()
                    else:
                        turtle = Turtle()
                        game_over = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    turtle.jump()
                else:
                    turtle = Turtle()
                    game_over = False

        # Update game
        turtle.update()
        
        # Draw everything
        screen.fill((0, 0, 0))
        
        # Draw turtle
        turtle.draw(screen)
        
        # Draw game over message
        if game_over:
            font = pygame.font.Font(None, 72)
            game_over_text = font.render("Game Over!", True, white)
            text_rect = game_over_text.get_rect(center=(400, 300))
            screen.blit(game_over_text, text_rect)
            
            font = pygame.font.Font(None, 36)
            restart_text = font.render("Press SPACE or click to try again!", True, white)
            text_rect = restart_text.get_rect(center=(400, 400))
            screen.blit(restart_text, text_rect)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    game_loop()
    pygame.quit()
sys.exit()
