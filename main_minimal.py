import pygame
import sys

# Initialize Pygame
pygame.init()
print("Pygame initialized successfully")

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Test Window")
print("Window created successfully")

clock = pygame.time.Clock()

# Game loop
def game_loop():
    running = True
    frame_count = 0
    while running:
        print(f"Frame {frame_count}")
        frame_count += 1
        
        # Handle events
        events = pygame.event.get()
        print(f"Events received: {len(events)}")
        for event in events:
            print(f"Event type: {event.type}")
            if event.type == pygame.QUIT:
                print("Quit event received")
                running = False
                pygame.quit()
                sys.exit()

        # Draw background using rect
        pygame.draw.rect(screen, (173, 216, 230), (0, 0, 800, 600))
        print("Rectangle drawn")
        
        # Update display
        pygame.display.flip()
        print("Display updated")
        clock.tick(30)

if __name__ == "__main__":
    print("Starting game loop")
    game_loop()
