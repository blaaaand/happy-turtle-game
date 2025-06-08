import pygame
import numpy as np
import time

# Initialize pygame
pygame.init()

# Initialize mixer with specific settings
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
print("Mixer initialized successfully")

# Function to create and play a bubble sound
def create_bubble_sound(duration=0.02, volume=0.1):
    # Create a numpy array of samples
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create a very gentle pop sound
    note = np.zeros_like(t)
    
    # Create a very soft pop sound with gentle frequencies
    base_freq = 500  # Even lower base frequency
    high_freq = 1200  # Even lower high frequency
    phase = np.random.random() * 2 * np.pi
    
    # Create a very gentle envelope with a slow attack and decay
    # Use a smoother cosine shape
    envelope = (1 + np.cos(np.pi * t / duration)) / 2  # Cosine shape
    envelope = envelope * envelope * envelope  # Cube it for extremely gentle attack/decay
    
    # Create the pop sound with very soft frequencies
    pop = 0.3 * np.sin(base_freq * 2 * np.pi * t + phase)  # Base frequency
    # Add an extremely gentle high frequency component
    pop += 0.03 * np.sin(high_freq * 2 * np.pi * t + phase)  # Very soft high frequency
    
    # Add very gentle random variation
    variation = np.random.normal(0, 0.02, len(t))  # Very reduced variation
    
    # Combine with envelope and variation
    note = (pop + variation) * envelope
    
    # Normalize
    note = note / np.max(np.abs(note))
    
    # Normalize the sound
    note = note / np.max(np.abs(note))
    
    # Convert to 16-bit integers
    note = (note * 32767).astype(np.int16)
    
    # Create sound object
    sound = pygame.mixer.Sound(note)
    sound.set_volume(volume)
    return sound

# Main test loop
print("Press space to play a bubble sound, or q to quit")
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Create and play a new bubble sound
                bubble_sound = create_bubble_sound()
                bubble_sound.play()
                print("Played bubble sound")
            elif event.key == pygame.K_q:
                running = False

# Clean up
pygame.mixer.quit()
pygame.quit()
