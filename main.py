import pygame
import sys
from turtle import Turtle
from game_config import Config

print("Starting game initialization")

try:
    # Initialize Pygame
    pygame.init()
    print("Pygame initialized successfully")
    
    # Set up display
    screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
    pygame.display.set_caption("Happy Turtle")
    print(f"Window created with size {Config.SCREEN_WIDTH}x{Config.SCREEN_HEIGHT}")
    
    clock = pygame.time.Clock()
    print("Clock created")
    
    # Create game objects
    turtle = Turtle()
    print(f"Turtle created at position {turtle.rect.x},{turtle.rect.y}")
    
    # Initialize game state
    current_state = Config.GAME_RUNNING
    score = 0
    print("Game state initialized")
    
    # Game loop
    def game_loop():
        global current_state, score
        
        running = True
        frame_count = 0
        while running:
            print(f"\nFrame {frame_count}")
            frame_count += 1
            
            # Handle events
            events = pygame.event.get()
            print(f"Events received: {len(events)}")
            for event in events:
                print(f"Event type: {event.type}")
                if event.type == pygame.QUIT:
                    print("Quit event received")
                    running = False
                            
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and current_state == Config.GAME_RUNNING:
                        turtle.jump()
                    elif event.key == pygame.K_p:  # P key to pause/resume
                        if current_state == Config.GAME_RUNNING:
                            current_state = Config.GAME_PAUSED
                            pause_button.text = "Resume"
                        elif current_state == Config.GAME_PAUSED:
                            current_state = Config.GAME_RUNNING
                            pause_button.text = "Pause"
                        
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and current_state == GAME_RUNNING:
                    turtle.jump()
                elif event.key == pygame.K_p:  # P key to pause/resume
                    if current_state == GAME_RUNNING:
                        current_state = GAME_PAUSED
                        pause_button.text = "Resume"
                    elif current_state == GAME_PAUSED:
                        current_state = GAME_RUNNING
                        pause_button.text = "Pause"
                
        if current_state == GAME_RUNNING:
            # Update game state
            hit_boundary = turtle.update()
            
            # Update obstacles and check if any passed
            score_increment = obstacle_manager.update(speed)
            score += score_increment
            
            # Gradually increase speed after every 10 obstacles
            if score > 0 and score % 10 == 0:
                speed = min(speed + 0.5, 6)  # Max speed of 6
                
            # Check collisions
            if obstacle_manager.check_collision(turtle.rect) or hit_boundary:
                # Add score to leaderboard if it's a high score
                if score > 1:  # Only add if score is greater than default
                    current_state = GAME_ENTER_NAME
                    
        # Draw everything
        screen.fill(Config.BG_COLOR)
        
        if current_state == GAME_RUNNING:
            obstacle_manager.draw(screen)
            turtle.draw(screen)
            
            # Draw score
            score_text = font.render(f'Score: {score}', True, (0, 0, 0))
            screen.blit(score_text, (10, 10))
            
            # Draw pause and reset buttons
            pause_button.draw(screen)
            reset_button.draw(screen)
            
        elif current_state == GAME_PAUSED:
            # Draw "Game Paused" text
            pause_text = font.render("Game Paused", True, (0, 0, 0))
            screen.blit(pause_text, (Config.SCREEN_WIDTH//2 - 60, Config.SCREEN_HEIGHT//2 - 20))
            
            # Draw pause button
            pause_button.draw(screen)
            
        elif current_state == GAME_ENTER_NAME:
            # Draw background
            obstacle_manager.draw(screen)
            turtle.draw(screen)
            
            # Draw message
            font = pygame.font.Font(None, 48)
            message = font.render("New High Score!", True, (0, 150, 200))
            screen.blit(message, (Config.SCREEN_WIDTH//4 - 80, Config.SCREEN_HEIGHT//2 - 100))
            
            # Draw score
            score_text = font.render(f"{score} points!", True, (0, 150, 200))
            screen.blit(score_text, (Config.SCREEN_WIDTH//4 - 60, Config.SCREEN_HEIGHT//2 - 50))
            
            # Draw name input
            name_input.update()
            name_input.draw(screen)
            
            # Draw instruction
            font = pygame.font.Font(None, 36)
            instruction = font.render("Enter your name:", True, (0, 150, 200))
            screen.blit(instruction, (Config.SCREEN_WIDTH//4 - 80, Config.SCREEN_HEIGHT//2 + 20))
            
            # Draw continue button
            continue_button = Button("Continue", Config.SCREEN_WIDTH//2 - 75, Config.SCREEN_HEIGHT//2 + 100, 150, 50)
            continue_button.draw(screen)
            
        elif current_state == GAME_OVER:
            # Keep the game running in the background
            obstacle_manager.draw(screen)
            turtle.draw(screen)
            
            # Draw a decorative message
            font = pygame.font.Font(None, 48)
            message = font.render("Great Job!", True, (0, 150, 200))
            screen.blit(message, (Config.SCREEN_WIDTH//4 - 60, Config.SCREEN_HEIGHT//2 - 40))
            
            # Draw score
            score_text = font.render(f"{score} points!", True, (0, 150, 200))
            screen.blit(score_text, (Config.SCREEN_WIDTH//4 - 60, Config.SCREEN_HEIGHT//2))
            
            # Draw play again button
            play_button.draw(screen)
            
            # Draw leaderboard in the right half
            leaderboard.draw(screen, show=True)
            
        # Draw pause and reset buttons
        pause_button.draw(screen)
        reset_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(Config.FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
