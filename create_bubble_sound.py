import pygame
import numpy as np
import wave
import struct

# Initialize pygame mixer
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

# Function to create and save bubble sound
def create_bubble_sound(filename='sounds/bubble_pop_final.wav'):
    # Create a numpy array of samples
    sample_rate = 44100
    duration = 0.02  # 20ms
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
    
    # Convert to 16-bit integers
    note = (note * 32767).astype(np.int16)
    
    # Create the WAV file
    with wave.open(filename, 'wb') as wav_file:
        # Set the WAV file parameters
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        
        # Write the samples
        for sample in note:
            wav_file.writeframesraw(struct.pack('<h', sample))
    
    print(f"Bubble sound created and saved to {filename}")

# Create the sound
create_bubble_sound()
