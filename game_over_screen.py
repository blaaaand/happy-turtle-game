# Game Over Screen Code
# This code shows how to properly draw the game over message with an outline

# First, create the outline font
outline_font = pygame.font.Font(None, 60)

# Then render and draw the black outline in four positions around the center
outline_text = outline_font.render(message, True, (0, 0, 0))  # Black color
outline_rect = outline_text.get_rect(center=(400, 350))
# Draw outline in four positions
screen.blit(outline_text, (outline_rect.x-2, outline_rect.y-2))  # Top-left
screen.blit(outline_text, (outline_rect.x+2, outline_rect.y-2))  # Top-right
screen.blit(outline_text, (outline_rect.x-2, outline_rect.y+2))  # Bottom-left
screen.blit(outline_text, (outline_rect.x+2, outline_rect.y+2))  # Bottom-right

# Finally, draw the white message on top
font = pygame.font.Font(None, 60)
message_text = font.render(message, True, (255, 255, 255))  # White color
message_rect = message_text.get_rect(center=(400, 350))
screen.blit(message_text, message_rect)
