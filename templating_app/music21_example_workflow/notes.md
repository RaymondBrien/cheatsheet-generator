steps:

1. render a note
2. render as svg
3. inject into a pdf
4. integrate into full worksheet genreation workflow: 
   1. refine music cheatsheet template
   2. hook up to yaml config setup 
   3. define request template for claude api (or LOCAL???) to genereate a series of templates: nice to have
5. write tests for integration between components: 
   1. happy path: 
      1. config file: (define contents):
         1. title, subtitle, purpose, musical notation, description, category (interval), subcategory (interval type) - could a lot of the theory be done by music21 such as defining the interval from a note etc, turn into different clefs?
      2. make the music21 object
      3. render as svg with verivio workflow
      4. take that rendered svg, with metadata from config file (description, what it is etc, category defined by music21 eg interval type) and put all injected into markdown template, then render as pdf as an interval 'card'.
   2. Define a series of intervals, generate multiple cards in one commmand. 
   3. Ensure file cleanup and zip file utils so not loads of assets clogging up space
   4. Start generating baby! Refine design first, add option for dark mode or dyslexic text, then start making a huge amount of cheatsheets, worksheets and cards to start selling!
      1. ensure integration testing is robust. Test extremeties, timeout and async handling. Optimise with multithreading for all filewriting and awaiting the reponses from llm's.
