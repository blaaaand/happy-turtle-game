import pygame
import sys
from turtle_minimal import Turtle

# Initialize Pygame
pygame.init()
print("Pygame initialized successfully")

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Test Turtle")
print("Window created successfully")

clock = pygame.time.Clock()

# Create turtle
turtle = Turtle()

# Game loop
def game_loop():
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quit event received")
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    turtle.jump()

        # Update game state
        hit_boundary = turtle.update()
        
        # Draw everything
        screen.fill((173, 216, 230))  # Light blue
        turtle.draw(screen)
        
        # Update display
        pygame.display.flip()
        clock.tick(Config.FPS)

if __name__ == "__main__":
    game_loop()
