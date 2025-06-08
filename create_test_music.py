import pygame
import numpy as np
import wave
import struct

# Initialize pygame
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

# Create a simple test WAV file
sample_rate = 44100
duration = 5  # 5 seconds
num_samples = int(sample_rate * duration)

# Create a simple melody
samples = np.zeros(num_samples)

# Add a simple melody using sine waves
for i in range(0, num_samples, sample_rate // 4):  # Change note every quarter note
    freq = 440  # A4 note
    note_duration = sample_rate // 4
    t = np.arange(i, min(i + note_duration, num_samples))
    
    # Create a simple sine wave
    samples[i:i+note_duration] = np.sin(2 * np.pi * freq * t / sample_rate)

# Normalize
samples = samples * 0.3  # Scale to 30% volume

# Convert to 16-bit integers
samples = (samples * 32767).astype(np.int16)

# Create WAV file
filename = 'sounds/test_music.wav'
with wave.open(filename, 'wb') as wav_file:
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)  # 2 bytes per sample
    wav_file.setframerate(sample_rate)
    
    # Write the samples
    for sample in samples:
        wav_file.writeframesraw(struct.pack('<h', sample))

print(f"Created test music file: {filename}")
