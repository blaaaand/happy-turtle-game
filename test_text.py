import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Test Text")

clock = pygame.time.Clock()

# Main game loop
def game_loop():
    running = True
    message = "Test Message"
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw background
        screen.fill((135, 206, 235))
        
        # Draw white text
        font = pygame.font.Font(None, 60)
        message_text = font.render(message, True, (255, 255, 255))
        message_rect = message_text.get_rect(center=(400, 350))
        screen.blit(message_text, message_rect)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
