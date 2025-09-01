# Overview
"For local text-to-speech generation without heavy dependencies or subscription requirements."

## Option 1: pyttsx3 (RECOMMENDED FOR START)
# Installation: pip install pyttsx3
"""
PROS:
- Lightweight, uses system TTS engines
- No internet required, works cross-platform
- Simple API, immediate generation

CONS:
- Voice quality depends on system voices (can be robotic)

BEST FOR: Quick implementation, testing, lightweight applications
"""

from pathlib import Path

import pyttsx3


async def generate_tts_pyttsx3(text: str, output_path: Path):
    """Generate TTS using pyttsx3 (system voices)"""
    engine = pyttsx3.init()

    # Optional: Configure voice settings
    voices = engine.getProperty('voices')
    print(f"Available voices: {len(voices)}")
    print("Voice options:")
    for i, voice in enumerate(voices):
        print(f"{i}: {voice.name} ({voice.languages})")

    if voices:
        engine.setProperty('voice', voices[0].id)  # Use first available voice
    
    engine.setProperty('rate', 150)    # Speed of speech
    engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)
    
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    print(f"Audio saved to: {output_path}")

# Example usage:
# generate_tts_pyttsx3("Hello, this is a test voiceover script.", "voiceover.wav")