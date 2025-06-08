# This is the fixed version of the game over message drawing
# Draw black text first for shadow effect
font = pygame.font.Font(None, 60)
black_text = font.render(message, True, (0, 0, 0))  # Black color
black_rect = black_text.get_rect(center=(400, 350))
screen.blit(black_text, black_rect)

# Draw white text on top
white_text = font.render(message, True, (255, 255, 255))  # White color
white_rect = white_text.get_rect(center=(400, 350))
screen.blit(white_text, white_rect)
