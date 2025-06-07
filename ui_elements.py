import pygame
from game_config import Config

class InputBox:
    def __init__(self, x, y, width, height, color=(0, 150, 200), active_color=(0, 180, 230)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.active_color = active_color
        self.text = ""
        self.font = pygame.font.Font(None, 36)
        self.active = False
        self.max_length = 10
        self.cursor_position = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input box
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return self.text
            elif event.key == pygame.K_BACKSPACE:
                if self.cursor_position > 0:
                    self.text = self.text[:self.cursor_position-1] + self.text[self.cursor_position:]
                    self.cursor_position -= 1
            elif event.key == pygame.K_LEFT:
                self.cursor_position = max(0, self.cursor_position - 1)
            elif event.key == pygame.K_RIGHT:
                self.cursor_position = min(len(self.text), self.cursor_position + 1)
            else:
                if len(self.text) < self.max_length:
                    self.text = self.text[:self.cursor_position] + event.unicode + self.text[self.cursor_position:]
                    self.cursor_position += 1
        return None

    def update(self):
        pass

    def draw(self, screen):
        # Draw the box
        pygame.draw.rect(screen, self.active_color if self.active else self.color, self.rect, 2)
        
        # Render the text
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))
        
        # Draw cursor
        if self.active:
            cursor_x = self.rect.x + 5 + self.font.size(self.text[:self.cursor_position])[0]
            pygame.draw.line(screen, (0, 0, 0), (cursor_x, self.rect.y + 5), (cursor_x, self.rect.y + self.rect.height - 5), 2)   

class Button:
    def __init__(self, text, x, y, width, height, color=(100, 100, 100), hover_color=(150, 150, 150)):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.Font(None, 36)
        self.hovering = False
        
    def draw(self, screen):
        color = self.hover_color if self.hovering else self.color
        pygame.draw.rect(screen, color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def check_hover(self, pos):
        self.hovering = self.rect.collidepoint(pos)
        
    def check_click(self, pos):
        return self.rect.collidepoint(pos)

class Leaderboard:
    def __init__(self):
        self.scores = []
        self.load_scores()
        
    def load_scores(self):
        try:
            with open('scores.txt', 'r') as f:
                lines = f.readlines()
                self.scores = [tuple(line.strip().split(',')) for line in lines]
        except:
            # Default scores
            self.scores = [('Player 1', '1')] * 8
            self.save_scores()
            
    def save_scores(self):
        with open('scores.txt', 'w') as f:
            for name, score in self.scores:
                f.write(f"{name},{score}\n")
                
    def add_score(self, name, score):
        new_score = (name, str(score))
        self.scores.append(new_score)
        self.scores.sort(key=lambda x: int(x[1]), reverse=True)
        self.scores = self.scores[:8]  # Keep only top 8
        self.save_scores()
        
    def draw(self, screen, show=False):
        if not show:
            return
            
        # Draw a decorative frame
        frame_rect = pygame.Rect(Config.SCREEN_WIDTH // 2 + 20, 20, Config.SCREEN_WIDTH // 2 - 40, Config.SCREEN_HEIGHT - 40)
        pygame.draw.rect(screen, (255, 255, 255), frame_rect)
        pygame.draw.rect(screen, (0, 150, 200), frame_rect, 3)
        
        # Draw title
        font = pygame.font.Font(None, 48)
        title = font.render("Happy Turtle Hall of Fame!", True, (0, 150, 200))
        screen.blit(title, (Config.SCREEN_WIDTH // 2 + 30, 30))
        
        # Draw scores
        font = pygame.font.Font(None, 36)
        y = 80
        for i, (name, score) in enumerate(self.scores):
            rank = font.render(f"#{i + 1}", True, (0, 150, 200))
            screen.blit(rank, (Config.SCREEN_WIDTH // 2 + 30, y))
            
            name_text = font.render(name, True, (0, 0, 0))
            screen.blit(name_text, (Config.SCREEN_WIDTH // 2 + 80, y))
            
            score_text = font.render(f"{score} points!", True, (0, 0, 0))
            screen.blit(score_text, (Config.SCREEN_WIDTH // 2 + 200, y))
            
            y += 40
            
        # Draw a decorative border
        for i in range(10):
            pygame.draw.circle(screen, (0, 150, 200), (Config.SCREEN_WIDTH // 2 + 30 + i * 50, 40), 5)
            pygame.draw.circle(screen, (0, 150, 200), (Config.SCREEN_WIDTH // 2 + 30 + i * 50, Config.SCREEN_HEIGHT - 20), 5)
