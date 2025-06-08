import pygame
import time

# Initialize pygame
pygame.init()

# Initialize mixer with specific settings
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
print("Mixer initialized successfully")
print(f"Mixer channels: {pygame.mixer.get_num_channels()}")
print(f"Mixer channels busy: {pygame.mixer.get_busy()}")

# Try loading a simple test sound
try:
    # Create a simple sine wave
    sample_rate = 44100
    duration = 1.0  # 1 second
    
    # Create a numpy array of samples
    import numpy as np
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    note = np.sin(440 * 2 * np.pi * t)  # 440 Hz A note
    
    # Convert to 16-bit integers
    note = (note * 32767).astype(np.int16)
    
    # Create sound object
    test_sound = pygame.mixer.Sound(note)
    print("Successfully created test sound")
    print(f"Sound duration: {test_sound.get_length()} seconds")
    
    # Play the sound
    test_sound.play()
    print("Playing test sound...")
    
    # Wait for sound to finish
    while pygame.mixer.get_busy():
        time.sleep(0.1)
    
    print("Test sound finished playing")
    
except Exception as e:
    print(f"Error playing test sound: {str(e)}")
finally:
    # Clean up
    pygame.mixer.quit()
    pygame.quit()
