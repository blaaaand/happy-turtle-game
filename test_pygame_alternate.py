import pygame
import sys

print("Starting Pygame test")

try:
    # Initialize Pygame
    pygame.init()
    print("Pygame initialized")
    
    # Set up display
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Alternate Pygame Test")
    print("Window created")
    
    # Create a surface
    surface = pygame.Surface((800, 600))
    surface.fill((255, 0, 0))  # Red background
    print("Surface created")
    
    # Main loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quit event received")
                running = False
            elif event.type == pygame.VIDEORESIZE:
                # Handle window resize
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                surface = pygame.Surface((event.w, event.h))
                surface.fill((255, 0, 0))
                
        # Draw surface
        screen.blit(surface, (0, 0))
        print("Surface drawn")
        
        # Update display
        pygame.display.update()
        
    # Clean up
    pygame.quit()
    print("Pygame quit")
    
except Exception as e:
    print(f"Error: {str(e)}", file=sys.stderr)
    print("Exiting due to error")
    sys.exit(1)
