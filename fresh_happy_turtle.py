import pygame
import sys
import time
import random

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Happy Turtle")

clock = pygame.time.Clock()

# Colors
dark_blue = (0, 0, 100)
light_blue = (0, 0, 200)
white = (255, 255, 255)
gray = (128, 128, 128)
light_gray = (200, 200, 200)
dark_gray = (100, 100, 100)
brown = (139, 69, 19)

class Turtle:
    def __init__(self):
        self.rect = pygame.Rect(100, 300, 50, 50)
        self.y_speed = 0
        self.gravity = 0.5
        self.is_alive = True
        
    def jump(self):
        self.y_speed = -10
        
    def update(self):
        if self.is_alive:
            self.y_speed += self.gravity
            self.rect.y += self.y_speed
            
            # Keep turtle on screen
            if self.rect.top < 0:
                self.rect.top = 0
                self.y_speed = 0
                self.is_alive = False
            if self.rect.bottom > 600:
                self.rect.bottom = 600
                self.y_speed = 0
                self.is_alive = False
                
    def draw(self, screen):
        # Draw head (bottom layer)
        pygame.draw.circle(screen, (0, 255, 0), (self.rect.x + 60, self.rect.y + 5), 10)  # Head moved 2 pixels left
        pygame.draw.circle(screen, (255, 255, 255), (self.rect.x + 60, self.rect.y + 5), 3)  # Eye moved 2 pixels left
        pygame.draw.circle(screen, (0, 0, 0), (self.rect.x + 60, self.rect.y + 5), 1)  # Pupil moved 2 pixels left
        
        # Draw shell (top layer)
        pygame.draw.ellipse(screen, (100, 60, 0), (self.rect.x - 5, self.rect.y - 15, 60, 30))  # Shell
        
        # Draw legs (top layer)
        pygame.draw.circle(screen, (0, 255, 0), (self.rect.x + 15, self.rect.y + 15), 6)  # Front leg attached to shell (1.5x bigger)
        pygame.draw.circle(screen, (0, 255, 0), (self.rect.x + 38, self.rect.y + 15), 6)  # Back leg attached to shell (1.5x bigger, 2 pixels left)

class Jellyfish:
    def __init__(self, x):
        self.rect = pygame.Rect(x, random.randint(50, 200), 40, 40)
        self.speed = 2
        self.bounce = 0
        self.bounce_dir = 1
        self.original_y = self.rect.y
        
    def update(self):
        self.rect.x -= self.speed
        self.bounce += 0.5 * self.bounce_dir
        if self.bounce > 10 or self.bounce < -10:
            self.bounce_dir *= -1
        self.rect.y = self.original_y + self.bounce
        
        if self.rect.right < 0:
            return False
        return True
        
    def draw(self, screen):
        # Draw jellyfish
        pygame.draw.ellipse(screen, light_gray, self.rect)
        # Draw tentacles
        for i in range(5):
            pygame.draw.line(screen, dark_gray,
                           (self.rect.x + 20, self.rect.bottom),
                           (self.rect.x + 20 + i*4, self.rect.bottom + 30),
                           2)

class Shark:
    def __init__(self, x):
        self.rect = pygame.Rect(x, random.randint(200, 400), 60, 30)
        self.speed = 3
        
    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            return False
        return True
        
    def draw(self, screen):
        # Draw shark body
        pygame.draw.rect(screen, gray, (self.rect.x, self.rect.y, 50, 30))
        # Draw tail
        pygame.draw.polygon(screen, gray, [
            (self.rect.x + 50, self.rect.y),
            (self.rect.x + 70, self.rect.y + 15),
            (self.rect.x + 50, self.rect.y + 30)
        ])
        # Draw eye
        pygame.draw.circle(screen, white, (self.rect.x + 15, self.rect.y + 10), 3)
        pygame.draw.circle(screen, (0, 0, 0), (self.rect.x + 15, self.rect.y + 10), 1)

class Coral:
    def __init__(self, x):
        self.rect = pygame.Rect(x, 450, 50, 50)
        self.speed = 2
        self.circles = []
        
        # Create stacked circles
        for i in range(5):
            self.circles.append(
                pygame.Rect(x + 10, 450 - (i * 20), 30, 30)
            )
        
    def update(self):
        self.rect.x -= self.speed
        for circle in self.circles:
            circle.x -= self.speed
        
        if self.rect.right < 0:
            return False
        return True
        
    def draw(self, screen):
        # Draw stacked circles
        for circle in self.circles:
            pygame.draw.circle(screen, brown, circle.center, 15)
            # Add texture
            pygame.draw.circle(screen, (165, 42, 42), 
                             (circle.x + random.randint(-5, 5),
                              circle.y + random.randint(-5, 5)),
                             2)

def game_loop():
    turtle = Turtle()
    score = 0
    game_over = False
    obstacles = []
    last_obstacle_time = 0
    OBSTACLE_INTERVAL = 1500  # 1.5 seconds
    
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game_over:
                        turtle.jump()
                    else:
                        turtle = Turtle()
                        turtle.rect.y = 300
                        score = 0
                        game_over = False
                        obstacles.clear()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    turtle.jump()
                else:
                    turtle = Turtle()
                    turtle.rect.y = 300
                    score = 0
                    game_over = False
                    obstacles.clear()

            # Update game
            turtle.update()
            
            # Update score
            if turtle.is_alive:
                score += 1
            else:
                game_over = True
            score += 1
        else:
            game_over = True

        # Create new obstacle
        current_time = pygame.time.get_ticks()
        # Only create obstacle if less than 3 on screen
        if len(obstacles) < 3:
            # Prevent same obstacle 3 times in a row
            if obstacles:
                last_type = type(obstacles[-1]).__name__
                if len(obstacles) >= 2:
                    second_last_type = type(obstacles[-2]).__name__
                    if last_type == second_last_type and last_type == type(obstacles[-3]).__name__:
                        # Skip this obstacle type
                        obstacle_type = random.choice([1, 2, 3])
                        while type(obstacles[-1]).__name__ == str(obstacle_type):
                            obstacle_type = random.choice([1, 2, 3])
                    else:
                        obstacle_type = random.randint(1, 3)
                else:
                    obstacle_type = random.randint(1, 3)
            else:
                obstacle_type = random.randint(1, 3)

            if obstacle_type == 1:
                obstacles.append(Jellyfish(800))
            elif obstacle_type == 2:
                obstacles.append(Shark(800))
            else:
                obstacles.append(Coral(800))
            last_obstacle_time = current_time

        # Update obstacles
        if not game_over:
            for obstacle in obstacles[:]:
                if not obstacle.update():
                    obstacles.remove(obstacle)
                
                # Check collision
                if turtle.rect.colliderect(obstacle.rect):
                    turtle.is_alive = False
                    game_over = True

        # Draw everything
        screen.fill(dark_blue)
        
        # Draw ocean floor
        pygame.draw.rect(screen, (139, 0, 139), (0, 450, 800, 150))  # Purple ocean floor
        
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, white)
        screen.blit(score_text, (10, 10))
        
        # Draw turtle
        turtle.draw(screen)
        
        # Draw obstacles
        for obstacle in obstacles:
            obstacle.draw(screen)
        
        # Draw game over message
        if game_over:
            font = pygame.font.Font(None, 72)
            game_over_text = font.render("Game Over!", True, white)
            text_rect = game_over_text.get_rect(center=(400, 300))
            screen.blit(game_over_text, text_rect)
            
            font = pygame.font.Font(None, 36)
            restart_text = font.render("Press SPACE or click to try again!", True, white)
            text_rect = restart_text.get_rect(center=(400, 400))
            screen.blit(restart_text, text_rect)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    game_loop()
    pygame.quit()
sys.exit()
