from music21 import *
import verovio
import os

def music21_to_svg(music21_object, output_path=None):
    """
    Convert a music21 object to SVG using Verovio
    
    Args:
        music21_object: Any music21 object (note, stream, score, etc.)
        output_path: Optional path to save SVG file
    
    Returns:
        str: SVG content as string
    """
    # Step 1: Convert music21 object to MusicXML
    print("Converting music21 object to MusicXML...")
    musicxml_path = music21_object.write('musicxml')
    print(f"MusicXML saved to: {musicxml_path}")
    
    # Read the MusicXML content
    with open(musicxml_path, 'r') as f:
        musicxml_string = f.read()
    print(f"MusicXML generated: {len(musicxml_string)} characters")
    
    # Step 2: Initialize Verovio toolkit
    print("Initializing Verovio toolkit...")
    tk = verovio.toolkit()
    
    # Step 3: Load MusicXML data into Verovio
    print("Loading MusicXML into Verovio...")
    tk.loadData(musicxml_string)
    
    # Step 4: Render to SVG
    print("Rendering to SVG...")
    svg_string = tk.renderToSVG(1)  # Render page 1
    
    # Step 5: Save to file if path provided
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg_string)
        print(f"SVG saved to: {output_path}")
    
    return svg_string

def main():
    """Main workflow demonstration"""
    print("=== Music21 to SVG Workflow ===\n")
    
    # Create a simple note
    print("1. Creating music21 note object...")
    n = note.Note('C4')
    print(f"   Note: {n}")
    
    # Convert to SVG
    print("\n2. Converting to SVG...")
    svg_content = music21_to_svg(n, 'note_c.svg')
    
    # Display some info about the SVG
    print(f"\n3. SVG generated successfully!")
    print(f"   SVG length: {len(svg_content)} characters")
    print(f"   First 200 characters: {svg_content[:200]}...")
    
    # Create a more complex example with a stream
    print("\n=== More Complex Example ===")
    print("4. Creating a stream with multiple notes...")
    s = stream.Stream()
    s.append(note.Note('C4', quarterLength=1))
    s.append(note.Note('E4', quarterLength=1))
    s.append(note.Note('G4', quarterLength=1))
    s.append(note.Note('C5', quarterLength=1))
    
    print("   Stream created with 4 notes")
    
    # Convert stream to SVG
    print("\n5. Converting stream to SVG...")
    svg_content = music21_to_svg(s, 'chord_c_major.svg')
    
    print(f"\n6. Stream SVG generated successfully!")
    print(f"   SVG length: {len(svg_content)} characters")

if __name__ == "__main__":
    main()
