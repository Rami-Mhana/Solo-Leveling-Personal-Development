"""Create gaming sound effects for the Solo Leveling platform."""

import wave
import math
import os

def create_achievement_sound(filename):
    """Create a cheerful ascending tone for achievements."""
    sample_rate = 44100
    duration = 0.5
    num_samples = int(sample_rate * duration)
    
    waves = []
    # Two ascending notes (C5, E5)
    for freq in [523, 659]:
        sub_duration = num_samples // 2
        for i in range(sub_duration):
            value = int(32767.0 * 0.3 * math.sin(2.0 * math.pi * freq * i / sample_rate))
            waves.append(value)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        for val in waves:
            wav_file.writeframes(val.to_bytes(2, byteorder='little', signed=True))


def create_levelup_sound(filename):
    """Create ascending tones for level-ups."""
    sample_rate = 44100
    duration = 1.0
    num_samples = int(sample_rate * duration)
    
    waves = []
    # Three ascending notes (C5, E5, G5)
    for freq in [523, 659, 784]:
        sub_duration = num_samples // 3
        for i in range(sub_duration):
            value = int(32767.0 * 0.3 * math.sin(2.0 * math.pi * freq * i / sample_rate))
            waves.append(value)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        for val in waves:
            wav_file.writeframes(val.to_bytes(2, byteorder='little', signed=True))


def create_quest_complete_sound(filename):
    """Create a success tone for quest completion."""
    sample_rate = 44100
    duration = 0.6
    num_samples = int(sample_rate * duration)
    
    waves = []
    # Solid note (G4)
    freq = 392
    for i in range(num_samples):
        value = int(32767.0 * 0.3 * math.sin(2.0 * math.pi * freq * i / sample_rate))
        waves.append(value)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        for val in waves:
            wav_file.writeframes(val.to_bytes(2, byteorder='little', signed=True))


if __name__ == '__main__':
    sounds_dir = os.path.join(os.path.dirname(__file__), 'app', 'static', 'sounds')
    os.makedirs(sounds_dir, exist_ok=True)
    
    # Create achievement sound
    achievement_file = os.path.join(sounds_dir, 'achievement.wav')
    create_achievement_sound(achievement_file)
    print(f"✓ Created {achievement_file}")
    
    # Create levelup sound
    levelup_file = os.path.join(sounds_dir, 'levelup.wav')
    create_levelup_sound(levelup_file)
    print(f"✓ Created {levelup_file}")
    
    # Create quest complete sound
    quest_file = os.path.join(sounds_dir, 'quest_complete.wav')
    create_quest_complete_sound(quest_file)
    print(f"✓ Created {quest_file}")
    
    print("\n✓ All sound effects created successfully!")
