"""
Reusable function to convert music21 objects to SVG using Verovio
"""
from music21 import *
import verovio
import tempfile
import os

def music21_to_svg(music21_object, output_path=None, scale=100):
    """
    Convert a music21 object to SVG using Verovio
    
    Args:
        music21_object: Any music21 object (note, stream, score, etc.)
        output_path: Optional path to save SVG file
        scale: Scale factor for the SVG (default: 100)
    
    Returns:
        str: SVG content as string
    """
    # Step 1: Convert music21 object to MusicXML
    musicxml_path = music21_object.write('musicxml')
    
    # Read the MusicXML content
    with open(musicxml_path, 'r') as f:
        musicxml_string = f.read()
    
    # Step 2: Initialize Verovio toolkit
    tk = verovio.toolkit()
    
    # Step 3: Set options (optional)
    options = {
        "scale": scale,
        "pageWidth": 200,  # Much smaller for web display
        "pageHeight": 100,  # Much smaller for web display
        "adjustPageHeight": True,
        "adjustPageWidth": True
    }
    tk.setOptions(options)
    
    # Step 4: Load MusicXML data into Verovio
    tk.loadData(musicxml_string)
    
    # Step 5: Render to SVG
    svg_string = tk.renderToSVG(1)  # Render page 1
    
    # Step 6: Save to file if path provided
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg_string)
    
    return svg_string

def create_note_svg(pitch, duration:int = 1, output_path=None, *args, **kwargs):
    """
    Convenience function to create SVG from a single note
    
    Args:
        pitch: Note pitch (e.g., 'C4', 'F#5')
        duration: Note duration (default: 1)
        output_path: Optional path to save SVG file
    
    Returns:
        str: SVG content as string
    """
    if not output_path:
        output_path = tempfile.mktemp(suffix='.svg')
    n = note.Note(pitch, quarterLength=duration)
    return music21_to_svg(n, output_path)

def create_chord_svg(pitches: list[str], duration=1, output_path=None):
    """
    Convenience function to create SVG from a chord
    
    Args:
        pitches: List of note pitches (e.g., ['C4', 'E4', 'G4'])
        duration: Chord duration (default: 1)
        output_path: Optional path to save SVG file
    
    Returns:
        str: SVG content as string
    """
    chord_obj = chord.Chord(pitches)
    chord_obj.quarterLength = duration
    return music21_to_svg(chord_obj, output_path)

# Example usage
if __name__ == "__main__":
    print("=== Music21 to SVG Examples ===\n")
    
    # Example 1: Single note
    print("1. Creating single note SVG...")
    svg1 = create_note_svg('C4', output_path='example_note.svg')
    print(f"   SVG length: {len(svg1)} characters")
    
    # Example 2: Chord
    print("\n2. Creating chord SVG...")
    svg2 = create_chord_svg(['C4', 'E4', 'G4'], output_path='example_chord.svg')
    print(f"   SVG length: {len(svg2)} characters")
    
    # Example 3: Custom stream
    print("\n3. Creating custom stream SVG...")
    s = stream.Stream()
    s.append(note.Note('C4', quarterLength=0.5))
    s.append(note.Note('D4', quarterLength=0.5))
    s.append(note.Note('E4', quarterLength=1))
    s.append(note.Note('F4', quarterLength=1))
    
    svg3 = music21_to_svg(s, output_path='example_melody.svg')
    print(f"   SVG length: {len(svg3)} characters")
    
    print("\nAll examples completed successfully!")