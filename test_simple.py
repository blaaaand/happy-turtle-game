import pygame
import sys
import time
from turtle_simple import Turtle
from obstacle import ObstacleManager
from high_scores import HighScores
from boundary import Boundary
from button import Button

# Initialize Pygame and create screen
def game_loop():
    global current_state, score, obstacle_manager
    
    # Initialize Pygame and create screen
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Happy Turtle")
    clock = pygame.time.Clock()
    
    # Create game objects
    turtle = Turtle()
    boundary = Boundary(800, 600)
    obstacle_manager = ObstacleManager(800, 600)
    high_scores = HighScores()
    retry_button = Button("Try Again?", 275, 300, 250, 60)
    start_button = Button("Start Game", 300, 250, 200, 50)
    submit_button = Button("Submit Score", 275, 400, 250, 60)
    
    # Game states
    GAME_START = 0
    GAME_DELAY = 1
    GAME_RUNNING = 2
    GAME_OVER = 3
    NAME_ENTRY = 4
    current_state = GAME_START
    score = 0
    delay_start_time = 0
    player_name = ""
    name_input_active = False
    
    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue
            
            # Handle keyboard events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if current_state == GAME_START:
                        current_state = GAME_DELAY
                        score = 0
                        turtle.start_game()
                        obstacle_manager = ObstacleManager(800, 600)
                        delay_start_time = time.time()
                    elif current_state == GAME_RUNNING:
                        turtle.jump()
                    elif current_state == GAME_OVER:
                        current_state = GAME_DELAY
                        score = 0
                        turtle.start_game()
                        obstacle_manager = ObstacleManager(800, 600)
                        delay_start_time = time.time()
                        name_input_active = False
                elif current_state == NAME_ENTRY:
                    if event.key == pygame.K_RETURN:
                        if player_name:  # Only save if name is not empty
                            # Submit name and start new game
                            high_scores.add_score(score, player_name)
                            current_state = GAME_DELAY
                            score = 0
                            turtle.start_game()
                            obstacle_manager = ObstacleManager(800, 600)
                            delay_start_time = time.time()
                            name_input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        # Only allow alphanumeric characters
                        if event.unicode.isalnum() and len(player_name) < 10:  # Limit to 10 characters
                            player_name += event.unicode
            
            # Handle mouse events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_state == GAME_START:
                    if start_button.check_click(event.pos):
                        current_state = GAME_DELAY
                        score = 0
                        turtle.start_game()
                        obstacle_manager = ObstacleManager(800, 600)
                        delay_start_time = time.time()
                        continue
                elif current_state == GAME_OVER:
                    if retry_button.check_click(event.pos):
                        current_state = GAME_DELAY
                        score = 0
                        turtle.start_game()
                        obstacle_manager = ObstacleManager(800, 600)
                        delay_start_time = time.time()
                        name_input_active = False
                        continue
                elif current_state == NAME_ENTRY:
                    if submit_button.check_click(event.pos):
                        if player_name:  # Only save if name is not empty
                            # Submit name and start new game
                            high_scores.add_score(score, player_name)
                            current_state = GAME_DELAY
                            score = 0
                            turtle.start_game()
                            obstacle_manager = ObstacleManager(800, 600)
                            delay_start_time = time.time()
                            name_input_active = False
                            continue

        # Update game state
        if current_state == GAME_DELAY:
            current_time = time.time()
            elapsed_time = current_time - delay_start_time
            
            # Calculate countdown
            if elapsed_time < 1:
                countdown = "Ready?"
            elif elapsed_time < 2:
                countdown = "2..."
            elif elapsed_time < 3:
                countdown = "1..."
            else:
                countdown = "Go!"
                current_state = GAME_RUNNING
                
            # Draw delay screen
            font = pygame.font.Font(None, 72)
            countdown_text = font.render(countdown, True, (255, 255, 255))
            text_rect = countdown_text.get_rect(center=(400, 200))
            screen.blit(countdown_text, text_rect)
            
            # Draw turtle in fixed starting position
            turtle.rect.y = 300  # Fixed position during countdown
            turtle.draw(screen)
            
            # Don't process any other events during countdown
            continue

        # Draw screen based on state
        screen.fill((0, 0, 255))  # Blue background
        
        if current_state == GAME_START:
            # Draw start screen
            font = pygame.font.Font(None, 72)
            title_text = font.render("Happy Turtle", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(400, 100))
            screen.blit(title_text, title_rect)
            
            start_button.draw(screen)
            
            font = pygame.font.Font(None, 36)
            instructions_text = font.render("Press SPACE or click to start", True, (255, 255, 255))
            instructions_rect = instructions_text.get_rect(center=(400, 400))
            screen.blit(instructions_text, instructions_rect)

        elif current_state == GAME_RUNNING:
            # Draw game elements
            boundary.draw(screen)
            obstacle_manager.draw(screen)
            turtle.draw(screen)
            
            # Draw score
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))
            
            # Update game elements
            turtle.update()
            obstacle_manager.update()
            
            # Check for collisions
            if turtle.check_collision(obstacle_manager.get_obstacles()):
                current_state = GAME_OVER

        elif current_state == GAME_OVER:
            # Draw game over screen
            font = pygame.font.Font(None, 72)
            game_over_text = font.render("Oh oh!", True, (255, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(400, 100))
            screen.blit(game_over_text, game_over_rect)
            
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(400, 200))
            screen.blit(score_text, score_rect)
            
            retry_button.draw(screen)
            
            high_scores_text = font.render("High Scores:", True, (255, 255, 255))
            high_scores_rect = high_scores_text.get_rect(center=(400, 300))
            screen.blit(high_scores_text, high_scores_rect)
            
            high_scores_list = high_scores.get_high_scores()
            for i, score_data in enumerate(high_scores_list):
                rank_text = font.render(str(i + 1), True, (255, 255, 255))
                rank_rect = rank_text.get_rect(center=(300, 330 + i * 50))
                screen.blit(rank_text, rank_rect)
                
                score_text = font.render(f"{score_data['name']}: {score_data['score']}", True, (255, 255, 255))
                score_rect = score_text.get_rect(center=(500, 330 + i * 50))
                screen.blit(score_text, score_rect)
            
            if high_scores_list and score > high_scores_list[-1]['score']:
                current_state = NAME_ENTRY
                player_name = ""
                name_input_active = True

        elif current_state == NAME_ENTRY:
            # Draw name entry screen
            font = pygame.font.Font(None, 72)
            new_high_text = font.render("New High Score!", True, (255, 255, 0))
            new_high_rect = new_high_text.get_rect(center=(400, 100))
            screen.blit(new_high_text, new_high_rect)
            
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(400, 200))
            screen.blit(score_text, score_rect)
            
            name_input_text = font.render(f"Enter your name: {player_name}_", True, (255, 255, 255))
            name_input_rect = name_input_text.get_rect(center=(400, 300))
            screen.blit(name_input_text, name_input_rect)
            
            submit_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit(0)

if __name__ == "__main__":
    game_loop()
