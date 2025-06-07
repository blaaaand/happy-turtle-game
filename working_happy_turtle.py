import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Happy Turtle")

clock = pygame.time.Clock()

# Colors
dark_blue = (0, 0, 100)
light_blue = (0, 0, 200)
white = (255, 255, 255)

class Turtle:
    def __init__(self):
        self.rect = pygame.Rect(100, 300, 50, 50)  # Start in middle of screen
        self.y_speed = 0
        self.gravity = 0.3
        self.is_alive = True
        
    def jump(self):
        self.y_speed = -10  # Jump up
        
    def update(self):
        if self.is_alive:
            self.y_speed += self.gravity
            self.rect.y += self.y_speed
            
            # Keep turtle on screen
            if self.rect.top < 0:
                self.rect.top = 0
                self.y_speed = 0
            if self.rect.bottom > 600:
                self.rect.bottom = 600
                self.y_speed = 0
                self.is_alive = False
                
    def draw(self, screen):
        # Draw turtle body
        pygame.draw.ellipse(screen, (0, 255, 0), self.rect)
        
        # Draw eyes
        pygame.draw.circle(screen, white, (self.rect.x + 10, self.rect.y + 15), 3)
        pygame.draw.circle(screen, (0, 0, 0), (self.rect.x + 10, self.rect.y + 15), 1)
        pygame.draw.circle(screen, white, (self.rect.x + 40, self.rect.y + 15), 3)
        pygame.draw.circle(screen, (0, 0, 0), (self.rect.x + 40, self.rect.y + 15), 1)
        
        # Draw legs
        pygame.draw.circle(screen, (0, 255, 0), (self.rect.x + 15, self.rect.y + 40), 5)
        pygame.draw.circle(screen, (0, 255, 0), (self.rect.x + 35, self.rect.y + 40), 5)

def game_loop():
    turtle = Turtle()
    score = 0
    game_over = False
    
    # Main game loop
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
                        # Reset game
                        turtle = Turtle()
                        score = 0
                        game_over = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    turtle.jump()
                else:
                    # Reset game
                    turtle = Turtle()
                    score = 0
                    game_over = False

        # Update game
        turtle.update()
        
        # Update score
        if turtle.is_alive:
            score += 1
        else:
            game_over = True

        # Draw everything
        screen.fill(dark_blue)
        
        # Draw ocean floor
        pygame.draw.rect(screen, light_blue, (0, 520, 800, 80))
        
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, white)
        screen.blit(score_text, (10, 10))
        
        # Draw turtle
        turtle.draw(screen)
        
        # Draw game over message
        if game_over:
            font = pygame.font.Font(None, 72)
            game_over_text = font.render("Game Over!", True, white)
            text_rect = game_over_text.get_rect(center=(400, 300))
            screen.blit(game_over_text, text_rect)
            
            # Draw restart instructions
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
