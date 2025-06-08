# Simple white text version
font = pygame.font.Font(None, 60)
message_text = font.render(message, True, (255, 255, 255))
message_rect = message_text.get_rect(center=(400, 350))
screen.blit(message_text, message_rect)
