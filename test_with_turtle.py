import pygame
import sys
import time

class Turtle:
    def __init__(self):
        self.rect = pygame.Rect(100, 300, 50, 50)
        self.y_speed = 0
        self.gravity = 0.5
        self.jump_speed = -15
        
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
        if self.rect.y >= 500:  # Only jump if on ground
            self.y_speed = self.jump_speed
    
    def start_game(self):
        self.rect.y = 300
        self.y_speed = 0
    
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)

def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Test Game")
    clock = pygame.time.Clock()
    
    # Create game objects
    turtle = Turtle()
    
    # Game states
    START = 0
    COUNTDOWN = 1
    PLAYING = 2
    current_state = START
    
    # Create simple button class
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
    
    # Create start button
    start_button = Button("Start Game", 300, 250, 200, 50)
    
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
                        print("Start button clicked")
                        current_state = COUNTDOWN
                        start_time = pygame.time.get_ticks()
                        turtle.start_game()
                        continue
                elif current_state == PLAYING:
                    if event.button == 1:  # Left mouse button
                        turtle.jump()
                        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if current_state == PLAYING:
                        turtle.jump()

        # Update game state
        if current_state == COUNTDOWN:
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
            if elapsed_time >= 3:
                current_state = PLAYING
                continue
        elif current_state == PLAYING:
            turtle.update()

        # Draw screen
        screen.fill((0, 0, 255))
        
        if current_state == START:
            start_button.draw(screen)
        elif current_state == COUNTDOWN:
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
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
        elif current_state == PLAYING:
            # Draw playing screen
            font = pygame.font.Font(None, 36)
            text = font.render("Playing...", True, (255, 255, 255))
            screen.blit(text, (10, 10))
            
            # Draw turtle
            turtle.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit(0)

if __name__ == "__main__":
    main()
