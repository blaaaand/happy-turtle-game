import pygame
import time

# Initialize pygame
pygame.init()

# Initialize mixer
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

# List of music tracks to test
music_tracks = [
    'sounds/happy-like-larry-jonny-boyle-main-version-02-09-5.mp3'
]

print("Testing music tracks...")
print("Press SPACE to play next track")
print("Press Q to quit")

# Main loop
current_track = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Stop current music
                pygame.mixer.music.stop()
                
                # Load and play next track
                current_track = (current_track + 1) % len(music_tracks)
                track = music_tracks[current_track]
                print(f"\nNow playing: {track}")
                try:
                    pygame.mixer.music.load(track)
                    pygame.mixer.music.set_volume(0.3)  # Start with 30% volume
                    pygame.mixer.music.play()
                except pygame.error as e:
                    print(f"Error playing {track}: {str(e)}")
            elif event.key == pygame.K_q:
                running = False

# Clean up
pygame.mixer.quit()
pygame.quit()
