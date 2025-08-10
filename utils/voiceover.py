#!/usr/bin/env python3
"""
Voiceover generation utilities using pyttsx3.
"""

import pyttsx3
from typing import Union
from pathlib import Path

from utils.general_utils import make_version


def generate_voiceover(content: Union[str, Path], topic: str) -> Path:
    """
    Generate voiceover recording using pyttsx3.
    
    Args:
        text: Text to convert to speech
        topic: Topic name for filename generation
        
    Returns:
        Path to the generated audio file
    """
    # Use existing pattern from file_management.py
    # TODO DRY, this file name stuff is already handled somewhere else - get it from there instead!)
    output_dir = Path("outputs/transcript-audio")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    version = make_version()
    output_path = output_dir / f"{topic}_voiceover_{version}.wav"
    
    try:
        print(f"🎵 Generating voiceover for topic: {topic}")
        if isinstance(content, Path):
            with content.open('r') as f:
                content = f.read()

        print(f"📝 Content length: {len(content)} characters")
        
        # Minimal TTS setup - just the essentials
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        
        engine.save_to_file(content, str(output_path))
        engine.runAndWait()
        
        # Verify file was created (reusing pattern from file_management.py)
        if not output_path.exists():
            raise RuntimeError(f"Failed to create voiceover file: {output_path}")
        
        file_size = output_path.stat().st_size
        print(f"✅ Voiceover saved successfully: {output_path}")
        print(f"📁 File size: {file_size} bytes")
        return output_path
            
    except Exception as e:
        raise RuntimeError(f"Failed to generate voiceover: {e}")


def generate_dry_run_voiceover(topic: str, prompt_text: str) -> Path:
    """
    Generate a voiceover for dry run mode using a sample script.
    
    Args:
        topic: Topic name for the cheatsheet
        prompt_text: The prompt text to summarize
        
    Returns:
        Path to the generated audio file
    """
    sample_script = f"""
    This is a dry run voiceover for the {topic} cheatsheet.
    
    The prompt contains {len(prompt_text)} characters and will generate a comprehensive cheatsheet covering:
    - Basic commands and syntax
    - Common use cases and examples
    - Best practices and tips
    - Troubleshooting guidance
    
    This is a test recording to verify the voiceover system is working correctly.
    """
    
    return generate_voiceover(sample_script, topic=topic) 