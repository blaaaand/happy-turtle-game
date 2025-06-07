import pygame
import sys
import time
import random

class Turtle:
    def __init__(self):
        self.rect = pygame.Rect(100, 300, 50, 50)
        self.y_speed = 0
        self.gravity = 0.3  # Reduced gravity for more floaty feel
        self.jump_speed = -8  # Reduced jump speed for better control
        self.is_alive = True
        
    def update(self):
        self.y_speed += self.gravity
        self.rect.y += self.y_speed
        
        # Keep turtle on screen
        if self.rect.y > 500:
            self.rect.y = 500
            self.y_speed = 0
            self.is_alive = False
        elif self.rect.y < 0:
            self.rect.y = 0
            self.y_speed = 0
            
    def jump(self):
        if self.rect.y >= 500:  # Only jump if on ground
            self.y_speed = self.jump_speed
    
    def reset(self):
        self.rect.y = 300
        self.y_speed = 0
        self.is_alive = True
    
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)

class Obstacle:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = screen_width
        self.width = 40
        
        # Create top and bottom obstacles
        self.top_height = random.randint(50, screen_height - 200)
        self.bottom_height = screen_height - self.top_height - 200
        
        # Create hitboxes
        self.top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        self.bottom_rect = pygame.Rect(self.x, self.top_height + 200, self.width, self.bottom_height)
        
    def update(self):
        self.x -= 3  # Move obstacle left
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x
        
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.top_rect)  # Red top obstacle
        pygame.draw.rect(screen, (255, 0, 0), self.bottom_rect)  # Red bottom obstacle
        
    def check_collision(self, turtle_rect):
        return self.top_rect.colliderect(turtle_rect) or self.bottom_rect.colliderect(turtle_rect)

class Button:
    def __init__(self, text, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 36)
        
    def draw(self, screen):
        pygame.draw.rect(screen, (100, 100, 255), self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def check_click(self, pos):
        return self.rect.collidepoint(pos)

def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Happy Turtle")
    clock = pygame.time.Clock()
    
    # Game states
    START = 0
    COUNTDOWN = 1
    PLAYING = 2
    GAME_OVER = 3
    current_state = START
    
    # Create game objects
    turtle = Turtle()
    obstacle = Obstacle(800, 600)
    start_button = Button("Start Game", 300, 250, 200, 50)
    retry_button = Button("Try Again", 300, 300, 200, 50)
    
    # Game variables
    score = 0
    countdown_start = 0
    
    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_state == START:
                    if start_button.check_click(event.pos):
                        current_state = COUNTDOWN
                        countdown_start = pygame.time.get_ticks()
                        turtle.reset()
                        continue
                elif current_state == GAME_OVER:
                    if retry_button.check_click(event.pos):
                        current_state = COUNTDOWN
                        countdown_start = pygame.time.get_ticks()
                        turtle.reset()
                        score = 0
                        obstacle = Obstacle(800, 600)
                        continue
                elif current_state == PLAYING:
                    turtle.jump()
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if current_state == PLAYING:
                        turtle.jump()
        
        # Update game state
        if current_state == COUNTDOWN:
            elapsed_time = (pygame.time.get_ticks() - countdown_start) / 1000
            if elapsed_time >= 3:
                current_state = PLAYING
                continue
        elif current_state == PLAYING:
            turtle.update()
            obstacle.update()
            
            # Check collision
            if obstacle.check_collision(turtle.rect):
                current_state = GAME_OVER
                continue
            
            # Update score
            if obstacle.x + obstacle.width < turtle.rect.x:
                score += 1
                obstacle = Obstacle(800, 600)
        
        # Draw screen
        screen.fill((0, 0, 255))  # Blue background
        
        if current_state == START:
            start_button.draw(screen)
        elif current_state == COUNTDOWN:
            elapsed_time = (pygame.time.get_ticks() - countdown_start) / 1000
            if elapsed_time < 1:
                countdown = "Ready?"
            elif elapsed_time < 2:
                countdown = "2..."
            elif elapsed_time < 3:
                countdown = "1..."
            else:
                countdown = "Go!"
            
            font = pygame.font.Font(None, 72)
            text = font.render(countdown, True, (255, 255, 255))
            text_rect = text.get_rect(center=(400, 300))
            screen.blit(text, text_rect)
            turtle.draw(screen)
        elif current_state == PLAYING:
            obstacle.draw(screen)
            turtle.draw(screen)
            
            # Draw score
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))
        elif current_state == GAME_OVER:
            font = pygame.font.Font(None, 72)
            game_over_text = font.render("Game Over!", True, (255, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(400, 200))
            screen.blit(game_over_text, game_over_rect)
            
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(400, 300))
            screen.blit(score_text, score_rect)
            
            retry_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
