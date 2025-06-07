import pygame
import sys

print("Starting Pygame test")

try:
    # Initialize Pygame
    pygame.init()
    print("Pygame initialized")
    
    # Set up display in fullscreen mode
    screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
    pygame.display.set_caption("Simple Pygame Test")
    print("Window created")
    
    # Main loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quit event received")
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
        # Fill screen with color
        screen.fill((255, 0, 0))  # Red background
        print("Screen filled with red")
        
        # Update display
        pygame.display.flip()
        
    # Clean up
    pygame.quit()
    print("Pygame quit")
    
except Exception as e:
    print(f"Error: {str(e)}", file=sys.stderr)
    print("Exiting due to error")
    sys.exit(1)
