# Music21 to SVG Workflow

This project demonstrates how to convert music21 objects to SVG images using Verovio.

## Workflow Overview

```
music21 Object → MusicXML → Verovio → SVG
```

## Basic Usage

### Simple Note to SVG
```python
from music21 import note
import verovio

# Create a note
n = note.Note('C4')

# Convert to MusicXML
musicxml_path = n.write('musicxml')
with open(musicxml_path, 'r') as f:
    musicxml = f.read()

# Convert to SVG with Verovio
tk = verovio.toolkit()
tk.loadData(musicxml)
svg = tk.renderToSVG(1)

# Save SVG
with open('note.svg', 'w') as f:
    f.write(svg)
```

### Using the Reusable Function
```python
from music21_to_svg import music21_to_svg, create_note_svg, create_chord_svg

# Single note
svg = create_note_svg('C4', output_path='note.svg')

# Chord
svg = create_chord_svg(['C4', 'E4', 'G4'], output_path='chord.svg')

# Any music21 object
from music21 import stream
s = stream.Stream()
s.append(note.Note('C4'))
s.append(note.Note('E4'))
s.append(note.Note('G4'))

svg = music21_to_svg(s, output_path='melody.svg')
```

## Files

- `simple_example.py` - Minimal working example
- `test.py` - Comprehensive workflow demonstration
- `music21_to_svg.py` - Reusable functions for your projects
- `requirements.txt` - Required dependencies

## Dependencies

- music21
- verovio

## Installation

```bash
pip install music21 verovio
```

## Key Points

1. **music21.write('musicxml')** returns a file path, not a string
2. **Verovio** handles the MusicXML → SVG conversion
3. **SVG output** is ready for embedding in HTML/PDF documents
4. **No external dependencies** like MuseScore or LilyPond required

## Integration with Pandoc

The generated SVG files can be directly embedded in Markdown documents and converted to PDF with Pandoc:

```markdown
# My Music Document

Here's a C major chord:

![C Major Chord](chord.svg)

And a simple melody:

![Melody](melody.svg)
```

```bash
pandoc document.md -o document.pdf
```