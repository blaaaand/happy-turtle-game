import pygame
import numpy as np
import wave
import struct
import random

# Initialize pygame mixer
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

# Function to create a playful underwater soundtrack
def create_underwater_music(filename='sounds/underwater_party.wav'):
    # Constants
    sample_rate = 44100
    duration = 60  # 60 seconds of music
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create stereo channels
    left = np.zeros_like(t)
    right = np.zeros_like(t)
    
    # Create a playful underwater atmosphere
    # Add gentle water sounds
    water_freq = 500
    water_phase = np.random.random() * 2 * np.pi
    water_envelope = np.sin(t * np.pi / duration)  # Gentle envelope
    water_sound = 0.1 * np.sin(water_freq * 2 * np.pi * t + water_phase) * water_envelope
    
    # Add playful musical elements
    # Simple happy melody using pentatonic scale
    notes = [262, 294, 330, 349, 392]  # C4, D4, E4, F4, G4
    melody = np.zeros_like(t)
    
    # Create a simple, repetitive melody
    for i in range(0, len(t), sample_rate // 4):  # Change note every quarter note
        note_idx = random.randint(0, len(notes) - 1)
        note_freq = notes[note_idx]
        note_duration = sample_rate // 4
        note_t = t[i:i+note_duration]
        
        # Add random variation to make it more playful
        freq_variation = note_freq * (1 + (random.random() - 0.5) * 0.1)
        phase = random.random() * 2 * np.pi
        
        # Create the note with a gentle envelope
        envelope = np.power(np.sin(note_t * np.pi / note_duration), 2)
        note = 0.2 * np.sin(freq_variation * 2 * np.pi * note_t + phase) * envelope
        
        melody[i:i+note_duration] += note
    
    # Add some playful bubbles
    bubble_times = np.arange(0, len(t), sample_rate // 8)  # Bubble every half second
    for bubble_time in bubble_times:
        if random.random() < 0.7:  # 70% chance of bubble
            duration = int(sample_rate * 0.05)  # 50ms
            bubble_t = t[bubble_time:bubble_time+duration]
            freq = 800 + random.random() * 400  # Random frequency between 800-1200Hz
            phase = random.random() * 2 * np.pi
            
            # Create bubble sound
            envelope = np.exp(-bubble_t * 100)
            bubble = 0.1 * np.sin(freq * 2 * np.pi * bubble_t + phase) * envelope
            
            # Add to both channels
            left[bubble_time:bubble_time+duration] += bubble
            right[bubble_time:bubble_time+duration] += bubble
    
    # Combine all elements
    left = water_sound + melody + left
    right = water_sound + melody + right
    
    # Normalize
    left = left / np.max(np.abs(left))
    right = right / np.max(np.abs(right))
    
    # Convert to 16-bit integers
    left = (left * 32767).astype(np.int16)
    right = (right * 32767).astype(np.int16)
    
    # Create the WAV file
    with wave.open(filename, 'wb') as wav_file:
        # Set the WAV file parameters
        wav_file.setnchannels(2)  # Stereo
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        
        # Write the samples
        for l, r in zip(left, right):
            wav_file.writeframesraw(struct.pack('<hh', l, r))
    
    print(f"Underwater party music created and saved to {filename}")

# Create the music
create_underwater_music()
