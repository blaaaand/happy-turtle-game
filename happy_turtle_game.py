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

# Obstacle class
class Obstacle:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.hitboxes = []
        self.create_hitboxes()
    
    def create_hitboxes(self):
        if self.type == "coral":
            self.hitboxes.append(pygame.Rect(self.x, self.y, 100, 50))
        elif self.type == "jellyfish":
            self.hitboxes.append(pygame.Rect(self.x, self.y, 50, 30))
        elif self.type == "shark":
            self.hitboxes.append(pygame.Rect(self.x, self.y, 80, 40))
    
    def update(self):
        self.x -= 3
        for hitbox in self.hitboxes:
            hitbox.x -= 3
    
    def draw(self, screen):
        if self.type == "coral":
            pygame.draw.rect(screen, (150, 100, 200), (self.x, self.y, 100, 50))
            pygame.draw.ellipse(screen, (150, 100, 200), (self.x, self.y - 20, 120, 40))
            pygame.draw.ellipse(screen, (150, 100, 200), (self.x + 20, self.y - 30, 140, 30))
        elif self.type == "jellyfish":
            pygame.draw.ellipse(screen, (128, 128, 128), (self.x, self.y, 50, 30))
            pygame.draw.ellipse(screen, (255, 255, 255), (self.x + 10, self.y + 10, 30, 10))
        elif self.type == "shark":
            pygame.draw.polygon(screen, (0, 0, 0), [
                (self.x, self.y),
                (self.x + 80, self.y),
                (self.x + 40, self.y + 40)
            ])

# Boundary class
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
        self.gravity = 0.3  # More floaty gravity for kids
        self.is_alive = True
        self.jump_height = -6  # More floaty jump
        self.head_x_offset = 0  # For head wiggling animation
        self.head_wiggle_timer = 0
        self.head_wiggle_direction = 1  # 1 for right, -1 for left
        
    def update(self):
        self.y_speed += self.gravity
        self.rect.y += self.y_speed
        
        # Update head wiggle animation
        if self.y_speed < 0:  # Only wiggle when jumping
            self.head_wiggle_timer += 1
            if self.head_wiggle_timer >= 10:  # Change direction every 10 frames
                self.head_wiggle_direction *= -1
                self.head_wiggle_timer = 0
            self.head_x_offset = self.head_wiggle_direction * 2  # Small wiggle offset
        else:
            self.head_x_offset = 0  # Reset when not jumping
            self.head_wiggle_timer = 0
            self.head_wiggle_direction = 1
        
        # Check collision with screen edges
        if self.rect.y >= 520:  # Bottom edge
            self.is_alive = False
        
        # Keep turtle within visible boundaries
        if self.rect.y > 520:  # Bottom boundary
            self.rect.y = 520
            self.y_speed = 0
        elif self.rect.y < 0:  # Top boundary
            self.rect.y = 0
            self.y_speed = 0
            
    def jump(self):
        self.y_speed = -6  # Slightly less floaty jump
    
    def reset(self):
        self.rect.y = 300
        self.y_speed = 0
        self.is_alive = True
        self.head_x_offset = 0
        self.head_wiggle_timer = 0
        self.head_wiggle_direction = 1
    
    def draw(self, screen):
        # Calculate head position with wiggle
        head_x = self.rect.x + 62 + self.head_x_offset
        head_y = self.rect.y + 5
        
        # Draw head first (bottom layer)
        pygame.draw.circle(screen, (0, 255, 0), (head_x, head_y), 10)  # Head
        pygame.draw.circle(screen, (255, 255, 255), (head_x, head_y), 3)  # White eye
        pygame.draw.circle(screen, (0, 0, 0), (head_x, head_y), 1)  # Black pupil
        
        # Draw shell (top layer)
        pygame.draw.ellipse(screen, (100, 60, 0), (self.rect.x - 5, self.rect.y - 15, 60, 30))  # Shell
        
        # Draw legs (bottom layer)
        pygame.draw.circle(screen, (0, 255, 0), (self.rect.x + 10, self.rect.y + 15), 6)  # Front leg
        pygame.draw.circle(screen, (0, 255, 0), (self.rect.x + 40, self.rect.y + 15), 6)  # Back leg

class Obstacle:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.float_timer = 0  # For jellyfish floating animation
        self.float_direction = 1  # 1 for up, -1 for down
        self.float_offset = 0  # Current float position offset
        self.tail_wag_timer = 0  # For shark tail wag animation
        self.tail_wag_direction = 1  # 1 for right, -1 for left
        self.tail_wag_offset = 0  # Current tail wag position offset
        self.coral_sway_timer = 0  # For coral swaying animation
        self.coral_sway_direction = 1  # 1 for right, -1 for left
        self.coral_sway_offset = 0  # Current coral sway position offset
        
        # Create rect for collision detection
        if self.type == "coral":
            self.rect = pygame.Rect(x, y, 100, 50)
        elif self.type == "jellyfish":
            self.rect = pygame.Rect(x, y, 50, 30)
        elif self.type == "shark":
            self.rect = pygame.Rect(x, y, 80, 40)
            
    def update(self, speed):
        self.x -= speed  # Move obstacle left at specified speed
        self.rect.x = self.x  # Update rect position
        
        # Update jellyfish floating animation
        if self.type == "jellyfish":
            self.float_timer += 1
            if self.float_timer >= 10:  # Change direction every 10 frames
                self.float_direction *= -1
                self.float_timer = 0
            self.float_offset = self.float_direction * 2  # Small float offset
            self.rect.y = self.y + self.float_offset  # Update rect position with float offset
        
        # Update shark tail wag animation
        if self.type == "shark":
            self.tail_wag_timer += 1
            if self.tail_wag_timer >= 5:  # Change direction every 5 frames for faster wag
                self.tail_wag_direction *= -1
                self.tail_wag_timer = 0
            self.tail_wag_offset = self.tail_wag_direction * 3  # Slightly larger wag offset
        
        # Update coral swaying animation
        if self.type == "coral":
            self.coral_sway_timer += 1
            if self.coral_sway_timer >= 15:  # Change direction every 15 frames for slower sway
                self.coral_sway_direction *= -1
                self.coral_sway_timer = 0
            self.coral_sway_offset = self.coral_sway_direction * 2  # Gentle sway offset
            
    def draw(self, screen):
        if self.type == "coral":
            # Draw coral with swaying animation
            coral_sway_x = self.x + self.coral_sway_offset
            
            # Draw coral as stacked circles with sway
            # Base circles
            pygame.draw.circle(screen, (150, 100, 200), (coral_sway_x + 20, self.y), 15)
            pygame.draw.circle(screen, (150, 100, 200), (coral_sway_x + 60, self.y), 15)
            
            # Middle circles with sway
            pygame.draw.circle(screen, (150, 100, 200), (coral_sway_x + 20, self.y - 30), 12)
            pygame.draw.circle(screen, (150, 100, 200), (coral_sway_x + 60, self.y - 30), 12)
            
            # Top circles with sway
            pygame.draw.circle(screen, (150, 100, 200), (coral_sway_x + 20, self.y - 60), 10)
            pygame.draw.circle(screen, (150, 100, 200), (coral_sway_x + 60, self.y - 60), 10)
            
            # Smaller top circles with sway
            pygame.draw.circle(screen, (150, 100, 200), (coral_sway_x + 20, self.y - 80), 8)
            pygame.draw.circle(screen, (150, 100, 200), (coral_sway_x + 60, self.y - 80), 8)
        elif self.type == "jellyfish":
            # Draw jellyfish with float animation
            float_y = self.y + self.float_offset
            
            # Draw jellyfish body
            pygame.draw.ellipse(screen, (128, 128, 128), (self.x, float_y, 60, 40))
            
            # Draw jellyfish tentacles with float animation
            for i in range(4):
                pygame.draw.line(screen, (128, 128, 128), 
                              (self.x + 15 + i*15, float_y + 40),
                              (self.x + 15 + i*15, float_y + 80),
                              2)
            
            # Draw jellyfish eyes with float animation
            pygame.draw.circle(screen, (255, 255, 255), (self.x + 20, float_y + 20), 3)
            pygame.draw.circle(screen, (255, 255, 255), (self.x + 40, float_y + 20), 3)
            
        elif self.type == "shark":
            # Draw shark with tail wag animation
            tail_wag_x = self.x + self.tail_wag_offset
            
            # Draw shark body
            pygame.draw.polygon(screen, (0, 0, 0), [
                (tail_wag_x, self.y + 20),
                (tail_wag_x + 100, self.y + 20),
                (tail_wag_x + 50, self.y)
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

class ObstacleManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.obstacles = []
        self.min_distance = 300
        self.max_obstacles = 3  # Default value
        self.obstacle_types = ["coral", "coral", "coral", "jellyfish", "shark"]
        self.last_obstacle_type = None
        self.last_obstacle_count = 0
        self.max_same_type = 2  # Maximum of 2 same obstacles in a row
        self.obstacle_speed = 2  # Default obstacle speed
        self.difficulty_level = 1  # Track current difficulty level
        self.score_thresholds = {
            1000: {'max_obstacles': 4, 'speed': 3.0, 'level': 2},
            2000: {'max_obstacles': 5, 'speed': 4.0, 'level': 3},
            3000: {'max_obstacles': 6, 'speed': 5.0, 'level': 4},
            4000: {'max_obstacles': 6, 'speed': 6.0, 'level': 5}
        }
        
    def update_difficulty(self, score):
        # Update max obstacles and speed based on score
        for threshold, settings in self.score_thresholds.items():
            if score >= threshold:
                self.max_obstacles = settings['max_obstacles']
                self.obstacle_speed = settings['speed']
            else:
                break
    
    def create_obstacle(self):
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
            obstacle.update(self.obstacle_speed)  # Pass speed to obstacle
            
            # Remove obstacles that are off screen
            if obstacle.rect.right < 0:
                self.obstacles.remove(obstacle)
            
        # Create new obstacles if we have space
        if len(self.obstacles) < self.max_obstacles:
            
            # Remove obstacles that are off screen
            if obstacle.rect.right < 0:
                self.obstacles.remove(obstacle)
                
        # Create new obstacles based on distance
        if not self.obstacles or self.screen_width - self.obstacles[-1].rect.x > self.min_distance:
            self.create_obstacle()
            
    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
            
    def get_obstacles(self):
        return self.obstacles

class Button:
    def __init__(self, text, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 36)
    
    def draw(self, screen):
        # Draw button background with rounded corners
        pygame.draw.rect(screen, (150, 100, 200), self.rect)  # Purple background
        
        # Draw white border
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        
        # Draw button text
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def check_click(self, pos):
        return self.rect.collidepoint(pos)

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
    retry_button = Button("Try Again", 275, 500, 250, 60)
    
    # Game states
    START = 0
    COUNTDOWN = 1
    PLAYING = 2
    GAME_OVER = 3
    
    current_state = START
    score = 0
    running = True
    countdown_time = 3  # Default countdown time
    countdown_start = 0  # Initialize with 0, will be set when countdown starts
    countdown_active = False  # Track if countdown is active
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if current_state == PLAYING:
                        turtle.jump()
                    elif current_state == START:
                        current_state = COUNTDOWN
                        countdown_start = time.time()
                        countdown_active = True
                        score = 0
                        turtle.reset()
                        obstacle_manager.obstacles.clear()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_state == START:
                    if start_button.check_click(event.pos):
                        current_state = COUNTDOWN
                        countdown_start = time.time()
                        countdown_active = True
                        score = 0
                        turtle.reset()
                        obstacle_manager.obstacles.clear()
                elif current_state == COUNTDOWN:
                    # Don't allow jumping during countdown
                    pass
                elif current_state == PLAYING:
                    turtle.jump()
                elif current_state == GAME_OVER:
                    if retry_button.check_click(event.pos):
                        current_state = COUNTDOWN
                        countdown_start = time.time()
                        countdown_active = True
                        score = 0
                        turtle.reset()
                        obstacle_manager.obstacles.clear()
        
        # Update game
        if current_state == PLAYING:
            turtle.update()
            obstacle_manager.update()
            
            # Update difficulty based on score
            obstacle_manager.update_difficulty(score)
            
            # Check collisions
            if turtle.rect.y <= 0:  # Top edge
                # Save high score
                name = "Player"
                high_scores.add_score(score, name)
                current_state = GAME_OVER
                continue  # Skip rest of loop
            
            for obstacle in obstacle_manager.obstacles:
                if obstacle.check_collision(turtle.rect):
                    # Save high score
                    name = "Player"
                    high_scores.add_score(score, name)
                    current_state = GAME_OVER
                    continue  # Skip rest of loop
            
            # Update score
            score += 1
            
            # Update difficulty based on score
            obstacle_manager.update_difficulty(score)
            
            # Draw difficulty level
            font = pygame.font.Font(None, 24)
            difficulty_text = font.render(f"Difficulty: {obstacle_manager.difficulty_level}", True, (255, 255, 255))
            screen.blit(difficulty_text, (10, 40))
        
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
            if countdown_active:
                current_time = time.time()
                remaining_time = max(0, int(countdown_time - (current_time - countdown_start)))
                
                if remaining_time <= 0:
                    current_state = PLAYING
                    countdown_active = False
                    obstacle_manager.create_obstacle()
                else:
                    font = pygame.font.Font(None, 120)
                    countdown_text = font.render(str(remaining_time), True, (255, 255, 255))
                    text_rect = countdown_text.get_rect(center=(400, 300))
                    screen.blit(countdown_text, text_rect)
            
            # Draw difficulty level
            font = pygame.font.Font(None, 24)
            difficulty_text = font.render(f"Difficulty: {obstacle_manager.difficulty_level}", True, (255, 255, 255))
            screen.blit(difficulty_text, (10, 40))
            
        elif current_state == PLAYING:
            # Draw game elements
            boundary.draw(screen)
            obstacle_manager.draw(screen)
            turtle.draw(screen)
            
            # Draw score
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))
            
        elif current_state == GAME_OVER:
            # Draw game over screen
            font = pygame.font.Font(None, 48)
            
            # Add fun message based on score
            if score < 100:
                message = "Oops! The jellyfish were faster this time!"
            elif score < 200:
                message = "You're wiggling like a baby octopus!"
            elif score < 500:
                message = "Whoa! You're a speedy sea-snail!"
            elif score < 1000:
                message = "You're splashing like a turbo turtle!"
            elif score < 2000:
                message = "You're zooming like a dolphin on roller skates!"
            elif score < 3000:
                message = "You've become King Crabby, ruler of the reef!"
            else:
                message = "HOLY SEA CUCUMBERS! You're the Ocean Overlord!"
            
            message_text = font.render(message, True, (255, 255, 255))
            text_rect = message_text.get_rect(center=(400, 300))
            screen.blit(message_text, text_rect)
            
            # Show score
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            text_rect = score_text.get_rect(center=(400, 400))
            screen.blit(score_text, text_rect)
            
            # Show high score
            top_score = high_scores.get_top_score()
            high_score_text = font.render(f"High Score: {top_score}", True, (255, 255, 255))
            text_rect = high_score_text.get_rect(center=(400, 450))
            screen.blit(high_score_text, text_rect)
            
            # Draw retry button
            retry_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
