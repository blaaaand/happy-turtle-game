import pygame
import random

class Obstacle:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rect = pygame.Rect(screen_width, 
                               random.randint(100, screen_height - 100),
                               50, 50)
        # Use ocean colors - light brown for seaweed
        self.color = (180, 100, 0)  # Light brown for seaweed
    
    def update(self):
        self.rect.x -= 2
        return self.rect.right < 0
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class ObstacleManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.obstacles = []
        self.spawn_timer = 0
        self.spawn_interval = 1000  # milliseconds
        
    def update(self, speed):
        # Update existing obstacles
        for obstacle in self.obstacles[:]:
            if obstacle.update():
                self.obstacles.remove(obstacle)
        
        # Spawn new obstacles
        self.spawn_timer += speed
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            self.obstacles.append(Obstacle(self.screen_width, self.screen_height))
        
        # Return points for obstacles that passed
        points = 0
        for obstacle in self.obstacles:
            if obstacle.rect.right < 100:  # When obstacle passes turtle
                points += 1
        return points
    
    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
    
    def check_collision(self, player_rect):
        return any(obstacle.rect.colliderect(player_rect) for obstacle in self.obstacles)
