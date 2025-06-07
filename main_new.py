import pygame
import sys
from turtle import Turtle
from obstacles import ObstacleManager
from game_config import Config
from ui_elements import Button, Leaderboard, InputBox

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
pygame.display.set_caption("Happy Turtle")

clock = pygame.time.Clock()

# Create UI elements
play_button = Button("Try Again!", Config.SCREEN_WIDTH//2 - 75, Config.SCREEN_HEIGHT//2, 150, 50, color=(0, 150, 200), hover_color=(0, 180, 230))
pause_button = Button("Pause", Config.SCREEN_WIDTH - 150, 20, 130, 40, color=(0, 150, 200), hover_color=(0, 180, 230))
reset_button = Button("New Game", Config.SCREEN_WIDTH - 290, 20, 130, 40, color=(0, 150, 200), hover_color=(0, 180, 230))
leaderboard = Leaderboard()

# Game states
GAME_RUNNING = 0
GAME_PAUSED = 1
GAME_OVER = 2
GAME_ENTER_NAME = 3
GAME_SKIN_SELECT = 4

def game_loop():
    global current_state, turtle, obstacle_manager, score, speed, selected_skin
    
    # Initialize game objects
    turtle = Turtle()
    obstacle_manager = ObstacleManager()
    score = 0
    speed = Config.OBSTACLE_SPEED
    running = True
    current_state = GAME_SKIN_SELECT
    selected_skin = 'default'
    
    # Create skin selection buttons
    skin_buttons = [
        Button("Blue", Config.SCREEN_WIDTH//4, Config.SCREEN_HEIGHT//2 - 50, 100, 40, color=(0, 0, 255), hover_color=(0, 0, 200)),
        Button("Green", Config.SCREEN_WIDTH//4, Config.SCREEN_HEIGHT//2, 100, 40, color=(0, 255, 0), hover_color=(0, 200, 0)),
        Button("Red", Config.SCREEN_WIDTH//4, Config.SCREEN_HEIGHT//2 + 50, 100, 40, color=(255, 0, 0), hover_color=(200, 0, 0)),
        Button("Play!", Config.SCREEN_WIDTH//4 + 150, Config.SCREEN_HEIGHT//2, 100, 40, color=(0, 150, 200), hover_color=(0, 180, 230))
    ]
    
    # Initialize game objects
    turtle = Turtle()
    obstacle_manager = ObstacleManager()
    score = 0
    speed = Config.OBSTACLE_SPEED
    running = True
    current_state = GAME_RUNNING
    
    # Create name input box
    name_input = InputBox(Config.SCREEN_WIDTH//2 - 100, Config.SCREEN_HEIGHT//2 + 50, 200, 40)
    
    font = pygame.font.Font(None, 36)

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if current_state == GAME_RUNNING:
                    if pause_button.check_click(mouse_pos):
                        current_state = GAME_PAUSED
                    elif reset_button.check_click(mouse_pos):
                        score = 0
                        speed = Config.OBSTACLE_SPEED
                        turtle.reset()
                        obstacle_manager = ObstacleManager()
                    else:
                        turtle.jump()
                        
                elif current_state == GAME_PAUSED:
                    if pause_button.text == "Pause":
                        pause_button.text = "Resume"
                        current_state = GAME_RUNNING
                    else:
                        pause_button.text = "Pause"
                        current_state = GAME_RUNNING
                        
                elif current_state == GAME_OVER:
                    if play_button.check_click(mouse_pos):
                        score = 0
                        speed = Config.OBSTACLE_SPEED
                        turtle.reset()
                        obstacle_manager = ObstacleManager()
                        current_state = GAME_RUNNING
                        
                elif current_state == GAME_ENTER_NAME:
                    name = name_input.handle_event(event)
                    if name is not None and name.strip():
                        leaderboard.add_score(name, score)
                        current_state = GAME_OVER
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if continue_button.check_click(mouse_pos):
                            leaderboard.add_score(name_input.get_text(), score)
                            current_state = GAME_OVER
                            name_input.clear_text()
                        
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
                elif current_state == GAME_ENTER_NAME:
                    if event.key == pygame.K_RETURN:
                        name = name_input.get_text()
                        if name.strip():
                            leaderboard.add_score(name, score)
                            current_state = GAME_OVER
                    elif event.key == pygame.K_BACKSPACE:
                        name_input.delete_last_char()
                    elif event.key == pygame.K_ESCAPE:
                        current_state = GAME_OVER
                        name_input.clear_text()
                    else:
                        name_input.handle_event(event)
                
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
            if obstacle_manager.check_collision(turtle.rect):
                # Add score to leaderboard if it's a high score
                if score > 1:  # Only add if score is greater than default
                    current_state = GAME_ENTER_NAME
            
            # Check for boundary collision
            if turtle.rect.top < 0 or turtle.rect.bottom > Config.SCREEN_HEIGHT:
                # Add score to leaderboard if it's a high score
                if score > 1:  # Only add if score is greater than default
                    current_state = GAME_ENTER_NAME
                else:
                    current_state = GAME_OVER
                    score = 0
                    speed = Config.OBSTACLE_SPEED
                    turtle.reset()
                    obstacle_manager = ObstacleManager()
                    
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
            message_rect = message.get_rect(center=(Config.SCREEN_WIDTH//2, Config.SCREEN_HEIGHT//2 - 100))
            screen.blit(message, message_rect)
            
        elif current_state == GAME_SKIN_SELECT:
            # Draw background
            screen.fill(Config.BG_COLOR)
            
            # Draw turtle preview
            turtle.draw(screen)
            
            # Draw skin selection text
            font = pygame.font.Font(None, 48)
            title = font.render("Choose Your Turtle!", True, (0, 150, 200))
            title_rect = title.get_rect(center=(Config.SCREEN_WIDTH//2, 100))
            screen.blit(title, title_rect)
            
            # Draw skin buttons
            for button in skin_buttons:
                button.draw(screen)
            
            # Handle skin selection
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in skin_buttons:
                    if button.check_click(mouse_pos):
                        if button.text in ["Blue", "Green", "Red"]:
                            # Update turtle color based on selected skin
                            if button.text == "Blue":
                                Config.TURTLE_COLOR = (0, 0, 255)
                            elif button.text == "Green":
                                Config.TURTLE_COLOR = (0, 255, 0)
                            elif button.text == "Red":
                                Config.TURTLE_COLOR = (255, 0, 0)
                            turtle = Turtle()  # Create new turtle with updated color
                        elif button.text == "Play!":
                            current_state = GAME_RUNNING
            
            # Draw score
            score_text = font.render(f"{score} points!", True, (0, 150, 200))
            score_rect = score_text.get_rect(center=(Config.SCREEN_WIDTH//2, Config.SCREEN_HEIGHT//2 - 50))
            screen.blit(score_text, score_rect)
            
            # Draw name input
            name_input.update()
            name_input.draw(screen)
            
            # Draw instruction
            font = pygame.font.Font(None, 36)
            instruction = font.render("Enter your name:", True, (0, 150, 200))
            instruction_rect = instruction.get_rect(center=(Config.SCREEN_WIDTH//2, Config.SCREEN_HEIGHT//2 + 20))
            screen.blit(instruction, instruction_rect)
            
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
            message_rect = message.get_rect(center=(Config.SCREEN_WIDTH//2, Config.SCREEN_HEIGHT//2 - 40))
            screen.blit(message, message_rect)
            
            # Draw score
            score_text = font.render(f"{score} points!", True, (0, 150, 200))
            score_rect = score_text.get_rect(center=(Config.SCREEN_WIDTH//2, Config.SCREEN_HEIGHT//2))
            screen.blit(score_text, score_rect)
            
            # Draw play again button
            play_button.draw(screen)
            
            # Draw leaderboard in the right half
            leaderboard.draw(screen, show=True)
            
        # Draw pause and reset buttons
        pause_button.draw(screen)
        reset_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(Config.FPS)

if __name__ == "__main__":
    game_loop()
