import pygame
import sys
import time
import random

class Turtle:
    def __init__(self):
        self.rect = pygame.Rect(100, 300, 50, 50)
        self.y_speed = 0
        self.gravity = 0.3  # Floaty gravity
        self.jump_speed = -8  # Floaty jump
        self.is_alive = True
        
    def update(self):
        self.y_speed += self.gravity
        self.rect.y += self.y_speed
        
        # Keep turtle on screen
        if self.rect.y > 500:
            self.rect.y = 500
            self.y_speed = 0
            self.is_alive = False
        elif self.rect.y < 0:
            self.rect.y = 0
            self.y_speed = 0
            
    def jump(self):
        if self.rect.y >= 500:  # Only jump if on ground
            self.y_speed = self.jump_speed
    
    def start_game(self):
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
        self.x -= 3  # Move obstacle left
        for hitbox in self.hitboxes:
            hitbox.x -= 3
            
    def draw(self, screen):
        if self.type == "coral":
            # Draw coral
            pygame.draw.rect(screen, (150, 100, 200), (self.x, self.y, 100, 50))
            # Draw coral fans
            pygame.draw.ellipse(screen, (150, 100, 200), (self.x, self.y - 20, 120, 40))
            pygame.draw.ellipse(screen, (150, 100, 200), (self.x + 20, self.y - 30, 140, 30))
        elif self.type == "jellyfish":
            # Draw jellyfish
            pygame.draw.ellipse(screen, (128, 128, 128), (self.x, self.y, 50, 30))
            pygame.draw.ellipse(screen, (255, 255, 255), (self.x + 10, self.y + 10, 30, 10))
        elif self.type == "shark":
            # Draw shark
            pygame.draw.polygon(screen, (0, 0, 0), [
                (self.x, self.y),
                (self.x + 80, self.y),
                (self.x + 40, self.y + 40)
            ])
            
    def check_collision(self, turtle_rect):
        return any(hitbox.colliderect(turtle_rect) for hitbox in self.hitboxes)

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
            
    def get_obstacles(self):
        return self.obstacles

class Button:
    def __init__(self, text, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 36)
        
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 128, 128), self.rect)  # Ocean blue button
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def check_click(self, pos):
        return self.rect.collidepoint(pos)

def game_loop():
    # Initialize Pygame and create screen
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Happy Turtle")
    clock = pygame.time.Clock()
    
    # Create game objects
    turtle = Turtle()
    obstacle_manager = ObstacleManager(800, 600)
    retry_button = Button("Try Again", 275, 300, 250, 60)
    start_button = Button("Start Game", 300, 250, 200, 50)
    
    # Game states
    GAME_START = 0
    GAME_DELAY = 1
    GAME_RUNNING = 2
    GAME_OVER = 3
    current_state = GAME_START
    score = 0
    delay_start_time = 0
    
    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue
                
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
                        continue
                elif current_state == GAME_RUNNING:
                    turtle.jump()
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if current_state == GAME_RUNNING:
                        turtle.jump()
        
        # Update game state
        if current_state == GAME_DELAY:
            current_time = time.time()
            elapsed_time = current_time - delay_start_time
            
            if elapsed_time >= 3:
                current_state = GAME_RUNNING
                continue
            
            # Draw delay screen
            screen.fill((135, 206, 235))  # Sky blue background
            
            if elapsed_time < 1:
                countdown = "Ready?"
            elif elapsed_time < 2:
                countdown = "2..."
            elif elapsed_time < 3:
                countdown = "1..."
            else:
                countdown = "Go!"
                
            font = pygame.font.Font(None, 72)
            countdown_text = font.render(countdown, True, (255, 255, 255))
            text_rect = countdown_text.get_rect(center=(400, 200))
            screen.blit(countdown_text, text_rect)
            
            # Draw turtle in fixed starting position
            turtle.rect.y = 300  # Fixed position during countdown
            turtle.draw(screen)
            
            continue

        # Draw screen based on state
        screen.fill((135, 206, 235))  # Sky blue background
        
        if current_state == GAME_START:
            # Draw start screen
            font = pygame.font.Font(None, 72)
            title_text = font.render("Happy Turtle", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(400, 100))
            screen.blit(title_text, title_rect)
            
            start_button.draw(screen)
            
            font = pygame.font.Font(None, 36)
            instructions_text = font.render("Tap to Start", True, (255, 255, 255))
            instructions_rect = instructions_text.get_rect(center=(400, 400))
            screen.blit(instructions_text, instructions_rect)

        elif current_state == GAME_RUNNING:
            # Draw game elements
            obstacle_manager.draw(screen)
            turtle.draw(screen)
            
            # Draw score
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {score}", True, (0, 0, 0))
            screen.blit(score_text, (10, 10))
            
            # Update game elements
            turtle.update()
            obstacle_manager.update()
            
            # Check for collisions
            if any(obstacle.check_collision(turtle.rect) for obstacle in obstacle_manager.get_obstacles()):
                current_state = GAME_OVER
            
            # Update score
            score += 1

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
            
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    game_loop()
