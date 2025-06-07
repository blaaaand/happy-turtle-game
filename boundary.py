import pygame

class Boundary:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.spike_height = 20
        self.spike_spacing = 50
        self.spike_color = (255, 127, 80)  # Coral pink
        
    def draw(self, screen):
        # Draw bottom boundary spikes
        for x in range(0, self.screen_width, self.spike_spacing):
            pygame.draw.line(screen, self.spike_color, (x, self.screen_height), (x, self.screen_height - self.spike_height), 2)
            pygame.draw.circle(screen, self.spike_color, (x, self.screen_height - self.spike_height), 5)
    
    def check_collision(self, player_rect):
        # Check top boundary (game over condition)
        if player_rect.top < 0:
            print("Game Over!")
            return True
        
        # Check bottom boundary
        for x in range(0, self.screen_width, self.spike_spacing):
            spike_rect = pygame.Rect(x, self.screen_height - self.spike_height, 2, self.spike_height)
            if player_rect.colliderect(spike_rect):
                return True
                
        return False
