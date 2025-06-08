import pygame
import sys
import time
import random
import os

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Happy Turtle")

clock = pygame.time.Clock()

class Turtle:
    def __init__(self):
        self.rect = pygame.Rect(100, 300, 50, 50)
        self.y_speed = 0
        self.gravity = 0.3
        self.is_alive = True
        self.jump_height = -6

    def update(self):
        self.y_speed += self.gravity
        self.rect.y += self.y_speed

        # Keep turtle within bounds
        if self.rect.y > 520:
            self.rect.y = 520
            self.y_speed = 0
        if self.rect.y < 0:
            self.rect.y = 0
            self.y_speed = 0

    def jump(self):
        self.y_speed = self.jump_height

    def reset(self):
        self.rect.y = 300
        self.y_speed = 0
        self.is_alive = True

def game_loop():
    running = True
    current_state = "GAME_OVER"  # Start in game over state to test
    score = 1000  # Set a score to test different messages
    turtle = Turtle()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_state == "GAME_OVER":
                    current_state = "PLAYING"
                    turtle.reset()

        if current_state == "GAME_OVER":
            # Add fun message based on score
            if score < 50:
                message = "Better luck next time!"
            elif score < 200:
                message = "You're getting the hang of it!"
            elif score < 500:
                message = "You're a turtle pro!"
            elif score < 1000:
                message = "You're swimming like a champ!"
            elif score < 2000:
                message = "You're a sea legend!"
            elif score < 3000:
                message = "You're a master of the waves!"
            else:
                message = "You're the ocean's greatest explorer!"
            
            # Draw message with larger font
            font = pygame.font.Font(None, 60)
            message_text = font.render(message, True, (255, 255, 255))
            message_rect = message_text.get_rect(center=(400, 350))
            screen.blit(message_text, message_rect)

        screen.fill((135, 206, 235))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
