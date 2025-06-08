import numpy as np
import wave
import struct

# Create a simple beep sound
sample_rate = 44100  # CD quality
duration = 0.1  # seconds
frequency = 1000  # Hz

# Generate time points
t = np.linspace(0, duration, int(sample_rate * duration), False)

# Create a simple sine wave
samples = np.sin(2 * np.pi * frequency * t)

# Convert to 16-bit integers
samples = (samples * 32767).astype(np.int16)

# Create WAV file
with wave.open('beep.wav', 'wb') as wav_file:
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(samples.tobytes())
