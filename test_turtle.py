import pygame
import sys
from turtle_simple import Turtle

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Turtle Test")

clock = pygame.time.Clock()

turtle = Turtle()

running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                turtle.jump()
                print("Space pressed - Jump!")
    
    # Update
    turtle.update()
    
    # Draw
    screen.fill((0, 0, 255))
    turtle.draw(screen)
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
