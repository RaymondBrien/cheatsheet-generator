# Text-to-Speech Options for Python

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

import pyttsx3

def generate_tts_pyttsx3(text, output_path="output.wav"):
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


# # Option 2: Coqui TTS (RECOMMENDED FOR QUALITY)
# # Installation: pip install TTS
# """
# PROS:
# - High-quality neural voices, completely local
# - Open source, professional-grade results
# - Many voice options and languages

# CONS:
# - ~500MB+ download for models
# - Slower than pyttsx3
# - Heavier dependency

# BEST FOR: Production applications where voice quality matters
# """

# try:
#     from TTS.api import TTS
    
#     def generate_tts_coqui(text, output_path="output.wav", model_name="tts_models/en/ljspeech/tacotron2-DDC"):
#         """Generate TTS using Coqui TTS (neural voices)"""
#         # Initialize TTS
#         tts = TTS(model_name=model_name, progress_bar=False)
        
#         # Generate speech
#         tts.tts_to_file(text=text, file_path=output_path)
#         print(f"Audio saved to: {output_path}")
    
#     # Example usage:
#     # generate_tts_coqui("Hello, this is a test voiceover script.", "voiceover.wav")
    
# except ImportError:
#     print("Coqui TTS not installed. Install with: pip install TTS")


# ## Option 3: espeak-ng (RECOMMENDED FOR CI)
# # Installation: pip install espeak-ng-python
# """
# PROS:
# - Tiny footprint, designed for automation
# - Very reliable, consistent results
# - Perfect for CI pipelines

# CONS:
# - More robotic sound
# - Limited voice options

# BEST FOR: CI/CD pipelines, automated testing, reliability over quality
# """

# try:
#     import espeakng
    
#     def generate_tts_espeak(text, output_path="output.wav"):
#         """Generate TTS using espeak-ng (lightweight, reliable)"""
#         # Initialize espeak
#         espeakng.set_voice('en')
#         espeakng.set_parameter(espeakng.Parameter.Rate, 150)
#         espeakng.set_parameter(espeakng.Parameter.Volume, 80)
        
#         # Generate speech
#         espeakng.synth_wav(text, output_path)
#         print(f"Audio saved to: {output_path}")
    
#     # Example usage:
#     # generate_tts_espeak("Hello, this is a test voiceover script.", "voiceover.wav")
    
# except ImportError:
#     print("espeak-ng-python not installed. Install with: pip install espeak-ng-python")


# ## Unified Interface
# def generate_voiceover(text, output_path="voiceover.wav", method="pyttsx3"):
#     """
#     Unified interface for generating voiceovers
    
#     Args:
#         text (str): The script text to convert to speech
#         output_path (str): Path for the output audio file
#         method (str): TTS method to use ('pyttsx3', 'coqui', 'espeak')
#     """
#     if method == "pyttsx3":
#         generate_tts_pyttsx3(text, output_path)
#     elif method == "coqui":
#         generate_tts_coqui(text, output_path)
#     elif method == "espeak":
#         generate_tts_espeak(text, output_path)
#     else:
#         raise ValueError(f"Unknown method: {method}. Use 'pyttsx3', 'coqui', or 'espeak'")


# ## Usage Examples
# if __name__ == "__main__":
#     # Sample script from your Anthropic API
#     sample_script = "Welcome to our presentation. Today we'll be discussing the latest developments in artificial intelligence."
    
#     # Try different methods (uncomment to test)
#     # generate_voiceover(sample_script, "test_pyttsx3.wav", "pyttsx3")
#     # generate_voiceover(sample_script, "test_coqui.wav", "coqui")
#     # generate_voiceover(sample_script, "test_espeak.wav", "espeak")
    
#     print("TTS options ready to use!")


# ## Recommendation Path:
# """
# 1. START WITH: pyttsx3 for immediate results and testing
# 2. UPGRADE TO: Coqui TTS when you need better voice quality
# 3. USE IN CI: espeak-ng for automated/production environments

# Installation commands:
# pip install pyttsx3                    # Start here
# pip install TTS                        # For quality
# pip install espeak-ng-python          # For CI
# """

# ## Converting WAV to MP3 (if needed)
# """
# If you need MP3 output instead of WAV:
# pip install pydub

# from pydub import AudioSegment
# audio = AudioSegment.from_wav("output.wav")
# audio.export("output.mp3", format="mp3")
# """