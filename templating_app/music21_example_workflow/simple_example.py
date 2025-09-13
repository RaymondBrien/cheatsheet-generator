"""
Minimal example: music21 Note -> SVG using Verovio
"""
from music21 import note
import verovio

# Step 1: Create a music21 note
n = note.Note('C4')
print(f"Created note: {n}")

# Step 2: Convert to MusicXML
musicxml_path = n.write('musicxml')
print(f"MusicXML saved to: {musicxml_path}")

# Read the MusicXML content
with open(musicxml_path, 'r') as f:
    musicxml = f.read()
print(f"MusicXML length: {len(musicxml)} characters")

# Step 3: Initialize Verovio and render SVG
tk = verovio.toolkit()
tk.loadData(musicxml)
svg = tk.renderToSVG(1)

# Step 4: Save SVG
with open('simple_note.svg', 'w') as f:
    f.write(svg)

print("SVG saved as 'simple_note.svg'")
print(f"SVG length: {len(svg)} characters")