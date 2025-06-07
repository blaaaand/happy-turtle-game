import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Turtle Test")

clock = pygame.time.Clock()

# Create turtle
turtle = pygame.Rect(100, 300, 50, 50)
y_speed = 0
gravity = 0.5
jump_speed = -10

# Game loop
def game_loop():
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    y_speed = jump_speed
        
        # Update turtle
        y_speed += gravity
        turtle.y += y_speed
        
        # Check boundaries
        if turtle.top < 0:
            turtle.top = 0
            y_speed = 0
        if turtle.bottom > 600:
            turtle.bottom = 600
            y_speed = 0
        
        # Draw everything
        screen.fill((173, 216, 230))  # Light blue background
        
        # Draw turtle body
        pygame.draw.ellipse(screen, (0, 150, 0), turtle)
        
        # Draw eyes
        pygame.draw.circle(screen, (255, 255, 255), (turtle.x + 20, turtle.y + 15), 5)
        pygame.draw.circle(screen, (255, 255, 255), (turtle.x + 30, turtle.y + 15), 5)
        pygame.draw.circle(screen, (0, 0, 0), (turtle.x + 20, turtle.y + 15), 2)
        pygame.draw.circle(screen, (0, 0, 0), (turtle.x + 30, turtle.y + 15), 2)
        
        # Draw shell
        pygame.draw.ellipse(screen, (100, 60, 0), (turtle.x, turtle.y - 20, 50, 30))
        
        # Update display
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    game_loop()
    pygame.quit()
    sys.exit()
