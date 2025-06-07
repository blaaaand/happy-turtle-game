import pygame
import sys
import time
import random
import os
import json

# HighScores class
class HighScores:
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
    
    def get_top_score(self):
        if self.high_scores:
            return self.high_scores[0]["score"]
        return 0

class Obstacle:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        
        # Create rect for collision detection
        if self.type == "coral":
            self.rect = pygame.Rect(x, y, 100, 50)
        elif self.type == "jellyfish":
            self.rect = pygame.Rect(x, y, 50, 30)
        elif self.type == "shark":
            self.rect = pygame.Rect(x, y, 80, 40)
            
    def update(self):
        self.x -= 2  # Move obstacle left
        self.rect.x = self.x  # Update rect position
            
    def draw(self, screen):
        if self.type == "coral":
            # Draw coral as stacked circles
            # Base circles
            pygame.draw.circle(screen, (150, 100, 200), (self.x + 20, self.y), 15)
            pygame.draw.circle(screen, (150, 100, 200), (self.x + 60, self.y), 15)
            
            # Middle circles
            pygame.draw.circle(screen, (150, 100, 200), (self.x + 20, self.y - 30), 12)
            pygame.draw.circle(screen, (150, 100, 200), (self.x + 60, self.y - 30), 12)
            
            # Top circles
            pygame.draw.circle(screen, (150, 100, 200), (self.x + 20, self.y - 60), 10)
            pygame.draw.circle(screen, (150, 100, 200), (self.x + 60, self.y - 60), 10)
            
            # Smaller top circles
            pygame.draw.circle(screen, (150, 100, 200), (self.x + 20, self.y - 80), 8)
            pygame.draw.circle(screen, (150, 100, 200), (self.x + 60, self.y - 80), 8)
        elif self.type == "jellyfish":
            # Draw jellyfish body
            pygame.draw.ellipse(screen, (128, 128, 128), (self.x, self.y, 60, 40))
            
            # Draw jellyfish tentacles
            for i in range(4):
                pygame.draw.line(screen, (128, 128, 128), 
                              (self.x + 15 + i*15, self.y + 40),
                              (self.x + 15 + i*15, self.y + 80),
                              2)
            
            # Draw jellyfish eyes
            pygame.draw.circle(screen, (255, 255, 255), (self.x + 20, self.y + 20), 3)
            pygame.draw.circle(screen, (255, 255, 255), (self.x + 40, self.y + 20), 3)
            
        elif self.type == "shark":
            # Draw stingray body
            pygame.draw.polygon(screen, (0, 0, 0), [
                (self.x, self.y + 20),
                (self.x + 100, self.y + 20),
                (self.x + 50, self.y)
            ])
            
            # Draw stingray tail
            pygame.draw.polygon(screen, (0, 0, 0), [
                (self.x + 100, self.y + 20),
                (self.x + 120, self.y + 10),
                (self.x + 120, self.y + 30)
            ])
            
            # Draw stingray eyes
            pygame.draw.circle(screen, (255, 255, 255), (self.x + 20, self.y + 15), 3)
            pygame.draw.circle(screen, (255, 255, 255), (self.x + 80, self.y + 15), 3)
            
    def check_collision(self, turtle_rect):
        return self.rect.colliderect(turtle_rect)

class Boundary:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
    
    def draw(self, screen):
        # Draw purple ocean floor
        pygame.draw.rect(screen, (150, 100, 200), (0, self.screen_height - 80, self.screen_width, 80))

class Turtle:
    def __init__(self):
        self.rect = pygame.Rect(100, 300, 50, 50)  # Start in middle of screen
        self.y_speed = 0
        self.gravity = 0.3  # Floaty gravity
        self.is_alive = True
        
    def update(self):
        self.y_speed += self.gravity
        self.rect.y += self.y_speed
        
        # Check collision with screen edges
        if self.rect.y > 520:  # Bottom edge
            self.is_alive = False
        
        # Keep turtle within visible boundaries
        if self.rect.y > 520:  # Bottom boundary
            self.rect.y = 520
            self.y_speed = 0
        elif self.rect.y < 0:  # Top boundary
            self.rect.y = 0
            self.y_speed = 0
            
    def jump(self):
        self.y_speed = -8  # Floaty jump
    
    def reset(self):
        self.rect.y = 300
        self.y_speed = 0
        self.is_alive = True
    
    def draw(self, screen):
        # Draw head first (bottom layer)
        pygame.draw.circle(screen, (0, 255, 0), (self.rect.x + 62, self.rect.y + 5), 10)  # Head
        pygame.draw.circle(screen, (255, 255, 255), (self.rect.x + 62, self.rect.y + 5), 3)  # White eye
        pygame.draw.circle(screen, (0, 0, 0), (self.rect.x + 62, self.rect.y + 5), 1)  # Black pupil
        
        # Draw shell (top layer)
        pygame.draw.ellipse(screen, (100, 60, 0), (self.rect.x - 5, self.rect.y - 15, 60, 30))  # Shell
        
        # Draw legs (bottom layer)
        pygame.draw.circle(screen, (0, 255, 0), (self.rect.x + 10, self.rect.y + 15), 6)  # Front leg
        pygame.draw.circle(screen, (0, 255, 0), (self.rect.x + 40, self.rect.y + 15), 6)  # Back leg

class Button:
    def __init__(self, text, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 36)
    
    def draw(self, screen):
        # Draw button background
        pygame.draw.rect(screen, (150, 150, 150), self.rect)
        
        # Draw text
        text = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
    
    def check_click(self, pos):
        return self.rect.collidepoint(pos)

class ObstacleManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.obstacles = []
        self.min_distance = 300
        self.max_obstacles = 3
        self.obstacle_types = ["coral", "coral", "coral", "jellyfish", "shark"]
        self.last_obstacle_type = None
        self.last_obstacle_count = 0
        self.max_same_type = 2  # Maximum of 2 same obstacles in a row
    
    def create_obstacle(self):
        if len(self.obstacles) < self.max_obstacles:
            # Choose obstacle type
            obstacle_type = random.choice(self.obstacle_types)
            
            # Prevent too many of the same type in a row
            if obstacle_type == self.last_obstacle_type:
                self.last_obstacle_count += 1
            else:
                self.last_obstacle_type = obstacle_type
                self.last_obstacle_count = 1
            
            if self.last_obstacle_count > self.max_same_type:
                # Remove current type from choices
                valid_types = [t for t in self.obstacle_types if t != obstacle_type]
                obstacle_type = random.choice(valid_types)
                self.last_obstacle_type = obstacle_type
                self.last_obstacle_count = 1
            
            # Position obstacle
            if obstacle_type == "coral":
                y = 520  # Fixed at bottom
            elif obstacle_type == "jellyfish":
                y = random.randint(100, 300)  # Random height near top
            elif obstacle_type == "shark":
                y = random.randint(200, 400)  # Random height in middle
            
            obstacle = Obstacle(self.screen_width, y, obstacle_type)
            self.obstacles.append(obstacle)
    
    def update(self):
        # Update obstacles
        for obstacle in self.obstacles:
            obstacle.update()
            
            # Remove obstacles that are off screen
            if obstacle.rect.right < 0:
                self.obstacles.remove(obstacle)
            
        # Create new obstacles
        if len(self.obstacles) < self.max_obstacles:
            self.create_obstacle()
    
    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
    
    def get_obstacles(self):
        return self.obstacles

def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Happy Turtle")
    clock = pygame.time.Clock()
    
    # Initialize game objects
    turtle = Turtle()
    boundary = Boundary(800, 600)
    obstacle_manager = ObstacleManager(800, 600)
    high_scores = HighScores()
    
    # Initialize buttons
    start_button = Button("Start Game", 275, 500, 250, 60)
    retry_button = Button("Try Again", 275, 600, 250, 60)
    
    # Game states
    START = 0
    COUNTDOWN = 1
    PLAYING = 2
    GAME_OVER = 3
    
    current_state = START
    score = 0
    running = True
    countdown_time = 0
    countdown_start = 0
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if current_state == COUNTDOWN:
                        turtle.jump()
                    elif current_state == PLAYING:
                        turtle.jump()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_state == START:
                    if start_button.check_click(event.pos):
                        current_state = COUNTDOWN
                        countdown_start = time.time()
                        countdown_time = 3  # 3 seconds countdown
                        score = 0
                        turtle.reset()
                        obstacle_manager.obstacles.clear()
                elif current_state == COUNTDOWN:
                    turtle.jump()
                elif current_state == PLAYING:
                    turtle.jump()
                elif current_state == GAME_OVER:
                    if retry_button.check_click(event.pos):
                        current_state = COUNTDOWN
                        countdown_start = time.time()
                        countdown_time = 3  # 3 seconds countdown
                        score = 0
                        turtle.reset()
                        obstacle_manager.obstacles.clear()
        
        # Update game
        if current_state == COUNTDOWN:
            current_time = time.time()
            remaining_time = max(0, int(countdown_time - (current_time - countdown_start)))
            
            if remaining_time <= 0:
                current_state = PLAYING
                obstacle_manager.create_obstacle()
        
        elif current_state == PLAYING:
            turtle.update()
            obstacle_manager.update()
            
            # Check collisions
            if turtle.rect.y >= 500:
                # Save high score
                name = "Player"
                high_scores.add_score(score, name)
                current_state = GAME_OVER
            
            for obstacle in obstacle_manager.obstacles:
                if obstacle.check_collision(turtle.rect):
                    # Save high score
                    name = "Player"
                    high_scores.add_score(score, name)
                    current_state = GAME_OVER
                    break
            
            # Update score
            score += 1
        
        # Draw everything
        screen.fill((135, 206, 235))  # Sky blue background
        
        # Draw game elements based on state
        if current_state == START:
            # Draw start screen
            font = pygame.font.Font(None, 72)
            title_text = font.render("Happy Turtle", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(400, 150))
            screen.blit(title_text, title_rect)
            
            # Draw turtle
            turtle_start_rect = pygame.Rect(350, 250, 50, 50)
            # Draw head
            pygame.draw.circle(screen, (0, 255, 0), (turtle_start_rect.x + 62, turtle_start_rect.y + 5), 10)
            pygame.draw.circle(screen, (255, 255, 255), (turtle_start_rect.x + 62, turtle_start_rect.y + 5), 3)
            pygame.draw.circle(screen, (0, 0, 0), (turtle_start_rect.x + 62, turtle_start_rect.y + 5), 1)
            
            # Draw shell
            pygame.draw.ellipse(screen, (100, 60, 0), (turtle_start_rect.x - 5, turtle_start_rect.y - 15, 60, 30))
            
            # Draw legs
            pygame.draw.circle(screen, (0, 255, 0), (turtle_start_rect.x + 10, turtle_start_rect.y + 15), 6)
            pygame.draw.circle(screen, (0, 255, 0), (turtle_start_rect.x + 40, turtle_start_rect.y + 15), 6)
            
            # Draw instructions
            font = pygame.font.Font(None, 36)
            instructions_text = font.render("Press SPACE or TAP to swim!", True, (255, 255, 255))
            instructions_rect = instructions_text.get_rect(center=(400, 400))
            screen.blit(instructions_text, instructions_rect)
            
            start_button.draw(screen)
            
        elif current_state == COUNTDOWN:
            # Draw countdown
            current_time = time.time()
            remaining_time = max(0, int(countdown_time - (current_time - countdown_start)))
            
            if remaining_time <= 0:
                current_state = PLAYING
                obstacle_manager.create_obstacle()
            else:
                font = pygame.font.Font(None, 120)
                countdown_text = font.render(str(remaining_time), True, (255, 255, 255))
                text_rect = countdown_text.get_rect(center=(400, 300))
                screen.blit(countdown_text, text_rect)
            
        elif current_state == PLAYING:
            # Draw game elements
            boundary.draw(screen)
            obstacle_manager.draw(screen)
            turtle.draw(screen)
            
            # Draw score
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {score}", True, (0, 0, 0))
            screen.blit(score_text, (10, 10))
            
        elif current_state == GAME_OVER:
            # Draw game over screen
            font = pygame.font.Font(None, 72)
            game_over_text = font.render("O Oh!", True, (255, 255, 255))
            text_rect = game_over_text.get_rect(center=(400, 300))
            screen.blit(game_over_text, text_rect)
            
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            text_rect = score_text.get_rect(center=(400, 400))
            screen.blit(score_text, text_rect)
            
            # Show high score
            top_score = high_scores.get_top_score()
            high_score_text = font.render(f"High Score: {top_score}", True, (255, 255, 255))
            text_rect = high_score_text.get_rect(center=(400, 450))
            screen.blit(high_score_text, text_rect)
            
            retry_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
