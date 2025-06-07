import pygame

class Button:
    def __init__(self, text, x, y, width, height, color=(0, 150, 200), hover_color=(0, 180, 230)):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        # Adjust font size based on button width
        self.font = pygame.font.Font(None, min(48, int(width * 0.3)))  # Font size is 30% of button width
        
    def draw(self, screen):
        # Draw button background
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
            
        # Draw button border
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        
        # Draw text
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def check_click(self, pos):
        return self.rect.collidepoint(pos)
