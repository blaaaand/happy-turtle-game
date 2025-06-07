import pygame
import sys
import time
import random
    def __init__(self):
        self.filename = "high_scores.json"
        self.high_scores = []
        self.load_scores()
    
    def load_scores(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    self.high_scores = json.load(f)
            else:
                self.high_scores = []
        except Exception as e:
            print(f"Error loading high scores: {e}")
            self.high_scores = []
    
    def add_score(self, score, name):
        try:
            high_scores = self.get_high_scores()
            high_scores.append({"name": name, "score": score})
            high_scores.sort(key=lambda x: x["score"], reverse=True)
            high_scores = high_scores[:10]
            
            with open(self.filename, 'w') as f:
                json.dump(high_scores, f)
        except Exception as e:
            print(f"Error saving high score: {e}")
    
    def get_high_scores(self):
        return self.high_scores

class Turtle:
    def __init__(self):
        self.rect = pygame.Rect(100, 300, 50, 50)
        self.y_speed = 0
        self.gravity = 0.5
        self.jump_speed = -15
        self.is_alive = True
        
    def update(self):
        self.y_speed += self.gravity
        self.rect.y += self.y_speed
        
        # Keep turtle within screen bounds
        if self.rect.y > 500:
            self.rect.y = 500
            self.y_speed = 0
            self.is_alive = False
        elif self.rect.y < 0:
            self.rect.y = 0
            self.y_speed = 0
            self.is_alive = False
        
    def jump(self):
        if self.rect.y >= 500:  # Only jump if on ground
            self.y_speed = self.jump_speed
            
    def reset(self):
        self.rect.x = 100
        self.rect.y = 300
        self.y_speed = 0
        self.is_alive = True
        
    def draw(self, screen):
        # Draw turtle body
        pygame.draw.rect(screen, (0, 255, 0), self.rect)
        # Draw head
        pygame.draw.circle(screen, (0, 255, 0), (self.rect.x + 15, self.rect.y - 10), 10)
        # Draw eyes
        pygame.draw.circle(screen, (255, 255, 255), (self.rect.x + 13, self.rect.y - 12), 3)
        pygame.draw.circle(screen, (0, 0, 0), (self.rect.x + 13, self.rect.y - 12), 1)
        # Draw legs
        pygame.draw.circle(screen, (0, 255, 0), (self.rect.x + 10, self.rect.y + 10), 5)
        pygame.draw.circle(screen, (0, 255, 0), (self.rect.x + 40, self.rect.y + 10), 5)

class Obstacle:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.hitboxes = []
        self.create_hitboxes()
        
    def create_hitboxes(self):
        if self.type == "coral":
            # Create hitbox for coral
            self.hitboxes.append(pygame.Rect(self.x, self.y, 100, 50))
        elif self.type == "jellyfish":
            # Create hitbox for jellyfish
            self.hitboxes.append(pygame.Rect(self.x, self.y, 50, 30))
        elif self.type == "shark":
            # Create hitbox for shark
            self.hitboxes.append(pygame.Rect(self.x, self.y, 80, 40))
            
    def update(self):
        self.x -= 3  # Move obstacle left at 3 pixels per frame
        for hitbox in self.hitboxes:
            hitbox.x -= 3
            
    def draw(self, screen):
        if self.type == "coral":
            # Draw coral
            pygame.draw.rect(screen, (150, 100, 200), (self.x, self.y, 100, 50))
            # Draw coral fans
            pygame.draw.ellipse(screen, (150, 100, 200), (self.x, self.y - 20, 120, 40))
            pygame.draw.ellipse(screen, (150, 100, 200), (self.x + 20, self.y - 30, 140, 30))
            
            # Draw debug hitboxes
            for hitbox in self.hitboxes:
                pygame.draw.rect(screen, (255, 0, 0), hitbox, 2)
        elif self.type == "jellyfish":
            # Draw jellyfish
            pygame.draw.ellipse(screen, (128, 128, 128), (self.x, self.y, 50, 30))
            pygame.draw.ellipse(screen, (255, 255, 255), (self.x + 10, self.y + 10, 30, 10))
            
            # Draw debug hitboxes
            for hitbox in self.hitboxes:
                pygame.draw.rect(screen, (255, 0, 0), hitbox, 2)
        elif self.type == "shark":
            # Draw shark
            pygame.draw.polygon(screen, (0, 0, 0), [
                (self.x, self.y),
                (self.x + 80, self.y),
                (self.x + 40, self.y + 40)
            ])
            
            # Draw debug hitboxes
            for hitbox in self.hitboxes:
                pygame.draw.rect(screen, (255, 0, 0), hitbox, 2)

class ObstacleManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.obstacles = []
        self.min_distance = 300
        self.max_obstacles = 2
        self.obstacle_types = ["coral", "jellyfish", "shark"]
        
    def create_obstacle(self):
        if len(self.obstacles) < self.max_obstacles:
            obstacle_type = random.choice(self.obstacle_types)
            
            # Create obstacle at right edge of screen
            if obstacle_type == "coral":
                # Coral sticks out from bottom
                y = self.screen_height - 50
            elif obstacle_type == "jellyfish":
                # Jellyfish floats at top
                y = 100
            elif obstacle_type == "shark":
                # Shark swims in middle
                y = 250
            
            obstacle = Obstacle(self.screen_width, y, obstacle_type)
            self.obstacles.append(obstacle)
            
    def update(self):
        # Update all obstacles
        for obstacle in self.obstacles:
            obstacle.update()
            
            # Remove obstacles that have moved off screen
            if obstacle.x + 100 < 0:  # 100 is width of obstacle
                self.obstacles.remove(obstacle)
                
        # Create new obstacles based on distance
        if not self.obstacles or self.screen_width - self.obstacles[-1].x > self.min_distance:
            self.create_obstacle()
            
    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Happy Turtle")
    clock = pygame.time.Clock()
    
    current_state = START
    score = 0
    
    # Initialize turtle
    turtle = Turtle()
    
    # Initialize obstacle manager
    obstacle_manager = ObstacleManager(800, 600)
    obstacle_manager.obstacles.clear()
    
    # Initialize buttons
    start_button = Button("Start Game", 275, 400, 250, 60)
    retry_button = Button("Try Again", 275, 500, 250, 60)
    submit_button = Button("Submit Score", 275, 400, 250, 60)
    
    # Initialize high scores
    high_scores = HighScores()
    
    # Initialize countdown
    countdown = None
    countdown_start = None
    player_name = ""
    
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            
            # Handle state-specific events
            if current_state == 0:  # START
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    current_state = 1  # COUNTDOWN
                    countdown = 3
                    countdown_start = pygame.time.get_ticks()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.check_click(event.pos):
                        current_state = 1  # COUNTDOWN
                        countdown = 3
                        countdown_start = pygame.time.get_ticks()
            
            elif current_state == 1:  # COUNTDOWN
                # Don't allow skipping countdown with space
                pass
            
            elif current_state == 2:  # PLAYING
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    turtle.jump()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    turtle.jump()
            
            elif current_state == 3:  # GAME_OVER
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    current_state = 0  # START
                    score = 0
                    turtle.reset()
                    obstacle_manager.obstacles.clear()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_button.check_click(event.pos):
                        current_state = 0  # START
                        score = 0
                        turtle.reset()
                        obstacle_manager.obstacles.clear()
            
            elif current_state == 4:  # NAME_ENTRY
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and player_name:
                        current_state = 3  # GAME_OVER
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode
        
        # Update game state
        if current_state == 1:  # COUNTDOWN
            if countdown is not None:
                elapsed_time = (pygame.time.get_ticks() - countdown_start) / 1000
                if elapsed_time >= 1:
                    countdown -= 1
                    countdown_start = pygame.time.get_ticks()
                    
                if countdown <= 0:
                    current_state = 2  # PLAYING
                    score = 0
                    turtle.reset()
                    obstacle_manager.obstacles.clear()
                    obstacle_manager.create_obstacle()
                    countdown = None
                    countdown_start = None
        
        elif current_state == 2:  # PLAYING
            # Update turtle
            turtle.update()
            
            # Check for boundary collisions
            if turtle.rect.y >= 500 or turtle.rect.y <= 0:
                turtle.is_alive = False
                current_state = 3  # GAME_OVER
            
            # Update obstacles
            obstacle_manager.update()
            
            # Check for obstacle collisions
            for obstacle in obstacle_manager.obstacles:
                for hitbox in obstacle.hitboxes:
                    if turtle.rect.colliderect(hitbox):
                        turtle.is_alive = False
                        current_state = 3  # GAME_OVER
                        break
            
            # Update score
            score += 1
        
        # Draw everything
        screen.fill((135, 206, 235))  # Sky blue background
        
        if current_state == 0:
            # Draw start screen
            font = pygame.font.Font(None, 72)
            title_text = font.render("Happy Turtle", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(400, 200))
            screen.blit(title_text, title_rect)
            
            subtitle_font = pygame.font.Font(None, 36)
            subtitle_text = subtitle_font.render("Tap to Start", True, (255, 255, 255))
            subtitle_rect = subtitle_text.get_rect(center=(400, 300))
            screen.blit(subtitle_text, subtitle_rect)
            
            start_button.draw(screen)
            
        elif current_state == 1:
            # Draw countdown
            if countdown is not None:
                elapsed_time = (pygame.time.get_ticks() - countdown_start) / 1000
                if elapsed_time < 1:
                    countdown = "Ready?"
                elif elapsed_time < 2:
                    countdown = "2..."
                elif elapsed_time < 3:
                    countdown = "1..."
                else:
                    countdown = "Go!"
                
                font = pygame.font.Font(None, 72)
                text = font.render(countdown, True, (255, 255, 255))
                text_rect = text.get_rect(center=(400, 300))
                screen.blit(text, text_rect)
            
        elif current_state == 2:
            # Draw turtle
            turtle.draw(screen)
            
            # Draw obstacles
            obstacle_manager.draw(screen)
            
            # Draw score
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {score}", True, (0, 0, 0))
            screen.blit(score_text, (10, 10))
            
        elif current_state == 3:
            # Draw game over screen
            font = pygame.font.Font(None, 72)
            game_over_text = font.render("Game Over!", True, (255, 255, 255))
            game_over_rect = game_over_text.get_rect(center=(400, 200))
            screen.blit(game_over_text, game_over_rect)
            
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(400, 300))
            screen.blit(score_text, score_rect)
            
            retry_button.draw(screen)
            
            # Draw high scores
            high_scores = high_scores.get_high_scores()
            if high_scores:
                high_scores_font = pygame.font.Font(None, 36)
                high_scores_text = high_scores_font.render("High Scores:", True, (255, 255, 255))
                high_scores_rect = high_scores_text.get_rect(center=(400, 400))
                screen.blit(high_scores_text, high_scores_rect)
                
                y_offset = 450
                for score in high_scores[:5]:
                    score_text = high_scores_font.render(f"{score['name']}: {score['score']}", True, (255, 255, 255))
                    score_rect = score_text.get_rect(center=(400, y_offset))
                    screen.blit(score_text, score_rect)
                    y_offset += 40
        
        elif current_state == 4:
            # Draw name entry screen
            font = pygame.font.Font(None, 72)
            name_text = font.render("Enter your name:", True, (0, 0, 0))
            name_rect = name_text.get_rect(center=(400, 200))
            screen.blit(name_text, name_rect)
            
            # Draw current name
            name_input_text = font.render(player_name, True, (0, 0, 0))
            # Check for retry button click
            name_input_text = font.render(player_name, True, (255, 255, 255))
            name_input_rect = name_input_text.get_rect(center=(400, 300))
            screen.blit(name_input_text, name_input_rect)
            
            # Draw submit button
            submit_button.draw(screen)
        
        # Draw coral at the bottom
        pygame.draw.rect(screen, (150, 100, 200), (0, 550, 800, 50))  # Purple coral base
        
        # Draw coral shapes
        coral_color = (150, 100, 200)
        # Draw coral fans
        for x in range(50, 800, 150):
            pygame.draw.ellipse(screen, coral_color, (x, 520, 100, 40))
            pygame.draw.ellipse(screen, coral_color, (x + 20, 530, 80, 30))

        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit(0)

if __name__ == "__main__":
    main()
