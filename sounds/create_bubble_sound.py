import numpy as np
import wave
import struct

# Create a simple bubble sound effect
sample_rate = 44100  # CD quality
duration = 0.2  # seconds

# Generate time points
t = np.linspace(0, duration, int(sample_rate * duration), False)

# Create a simple frequency-modulated sound
# This creates a bubble-like sound effect
samples = np.sin(2 * np.pi * 1000 * t)  # Base frequency 1000 Hz

# Add frequency modulation to create a bubble effect
modulation = np.sin(2 * np.pi * 5 * t)  # 5 Hz modulation
samples = samples * (1 + 0.5 * modulation)

# Add some decay to make it sound more like a bubble popping
samples = samples * np.exp(-t * 4)

# Convert to 16-bit integers
samples = (samples * 32767).astype(np.int16)

# Create WAV file
with wave.open('bubble.wav', 'wb') as wav_file:
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(samples.tobytes())
