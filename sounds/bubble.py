import numpy as np
import soundfile as sf

# Create a bubble sound effect
sample_rate = 44100
duration = 0.2  # seconds

# Generate time points
t = np.linspace(0, duration, int(sample_rate * duration), False)

# Create a simple frequency-modulated sound
frequency = 1000  # Hz
samples = np.sin(2 * np.pi * frequency * t)

# Add frequency modulation
modulation = np.sin(2 * np.pi * 5 * t)  # 5 Hz modulation
samples = samples * (1 + 0.5 * modulation)

# Add amplitude envelope (attack and decay)
envelope = np.zeros_like(t)
envelope[:len(t)//2] = np.linspace(0, 1, len(t)//2)  # Attack
envelope[len(t)//2:] = np.linspace(1, 0, len(t)//2)  # Decay
samples = samples * envelope

# Convert to 16-bit integers
samples = (samples * 32767).astype(np.int16)

# Save as WAV file
sf.write('bubble.wav', samples, sample_rate, subtype='PCM_16')
