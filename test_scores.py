import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Create a simple high scores class
class SimpleHighScores:
    def __init__(self):
        self.scores = [
            {"name": "Happy", "score": 0},
            {"name": "Happy", "score": 0},
            {"name": "Happy", "score": 0}
        ]

    def add_score(self, score, name):
        # Add the new score
        self.scores.append({"name": name, "score": score})
        # Sort by score (highest first)
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        # Keep only top 3
        self.scores = self.scores[:3]

    def get_scores(self):
        return self.scores

def main():
    high_scores = SimpleHighScores()
    
    # Test scores
    test_scores = [
        (100, "Player1"),
        (200, "Player2"),
        (150, "Player3"),
        (250, "Player4"),
        (175, "Player5")
    ]
    
    # Add test scores
    for score, name in test_scores:
        high_scores.add_score(score, name)
        print(f"Added score: {score} by {name}")
        print("Current high scores:")
        for i, score_data in enumerate(high_scores.get_scores()):
            print(f"{i + 1}. {score_data['name']}: {score_data['score']}")
        print("-" * 50)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw background
        screen.fill((0, 0, 255))
        
        # Draw high scores
        font = pygame.font.Font(None, 36)
        scores = high_scores.get_scores()
        
        # Draw title
        title = font.render("High Scores", True, (255, 255, 255))
        screen.blit(title, (10, 10))
        
        # Draw scores
        for i, score_data in enumerate(scores):
            # Draw rank
            rank = font.render(str(i + 1), True, (255, 255, 255))
            screen.blit(rank, (10, 50 + i * 40))
            
            # Draw name and score
            score_text = font.render(f"{score_data['name']}: {score_data['score']}", True, (255, 255, 255))
            screen.blit(score_text, (50, 50 + i * 40))
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
