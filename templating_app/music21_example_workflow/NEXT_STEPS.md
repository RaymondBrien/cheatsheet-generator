1. Parse content 'note' from content.yaml via render_svg function in music21_example_workflow/msuic21_to_svg.py
2. redner_svg gives us an svg file
3. send that svg file to template using jinja
   1. investigate: do I need a function in templating_app/main to handle svg's?
      1. this should be async as there will be lots of file reading and writing.
      2. avoid race conditions by using an actor to gate access to the file in question before rendering.
      3. Validate the file before rendering - there should already be a function for this

