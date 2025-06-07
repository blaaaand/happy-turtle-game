import pygame
import random
from game_config import Config

class Obstacle:
    def __init__(self):
        self.image = pygame.Surface((50, random.randint(50, 200)))  # Random height between 50-200
        self.image.fill(Config.CORAL_COLOR)
        self.rect = self.image.get_rect()
        self.reset()
        
    def reset(self):
        # Random position from top or bottom
        if random.random() < 0.5:
            # Top obstacle
            self.rect.x = Config.SCREEN_WIDTH + 50
            self.rect.y = random.randint(0, Config.SCREEN_HEIGHT // 2)
        else:
            # Bottom obstacle
            self.rect.x = Config.SCREEN_WIDTH + 50
            self.rect.y = random.randint(Config.SCREEN_HEIGHT // 2, Config.SCREEN_HEIGHT - self.rect.height)
        
    def update(self, speed):
        self.rect.x -= speed
        if self.rect.right < 0:
            self.reset()
            return True  # Returns True when obstacle passes screen
        return False
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
    def check_collision(self, turtle_rect):
        return turtle_rect.colliderect(self.rect)


class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        self.create_new_obstacle()
        self.create_new_obstacle()  # Create two obstacles initially
        
    def create_new_obstacle(self):
        self.obstacles.append(Obstacle())
        
    def update(self, speed):
        score_increment = 0
        
        # Update all obstacles and remove those that are off screen
        for i in range(len(self.obstacles) - 1, -1, -1):
            obstacle = self.obstacles[i]
            if obstacle.update(speed):
                self.obstacles.pop(i)
                score_increment += 1
                
            # Create new obstacle when the last one is 2/3 across the screen
            if i == len(self.obstacles) - 1 and obstacle.rect.right < Config.SCREEN_WIDTH - 100 and len(self.obstacles) < 3:
                self.create_new_obstacle()
        
        return score_increment
        
    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
        
    def check_collision(self, turtle_rect):
        for obstacle in self.obstacles:
            if obstacle.check_collision(turtle_rect):
                return True
        return False
