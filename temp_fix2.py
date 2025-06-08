# This is the exact change we need to make
# Change this block:
# Draw message with larger font
font = pygame.font.Font(None, 60)  # Larger font size for better visibility
message_text = font.render(message, True, (255, 255, 255))
message_rect = message_text.get_rect(center=(400, 350))
screen.blit(message_text, message_rect)

# Add black outline for better visibility
outline_text = font.render(message, True, (0, 0, 0))
outline_rect = outline_text.get_rect(center=(400, 350))
screen.blit(outline_text, (outline_rect.x-2, outline_rect.y-2))  # Top-left
screen.blit(outline_text, (outline_rect.x+2, outline_rect.y-2))  # Top-right
screen.blit(outline_text, (outline_rect.x-2, outline_rect.y+2))  # Bottom-left
screen.blit(outline_text, (outline_rect.x+2, outline_rect.y+2))  # Bottom-right

# To this:
# Draw message with larger font
font = pygame.font.Font(None, 60)  # Larger font size for better visibility
message_text = font.render(message, True, (255, 255, 255))
message_rect = message_text.get_rect(center=(400, 350))
screen.blit(message_text, message_rect)
