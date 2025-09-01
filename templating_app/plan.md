# Project Structure and Template Files

## Directory Structure
```
templating_app/
├── templating_app.py              # Main application
├── requirements.txt               # Python dependencies
├── config/
│   └── global.yaml               # Global configuration
├── templates/
│   ├── base/
│   │   ├── programming_cheatsheet.md.j2
│   │   ├── music_theory.md.j2
│   │   └── common_sections.md.j2
│   └── styles/
│       ├── custom.latex          # Pandoc LaTeX template
│       └── main.css             # HTML styles
├── content/
│   ├── python_basics/
│   │   ├── config.yaml
│   │   └── content.yaml
│   └── music_intervals/
│       ├── config.yaml
│       └── content.yaml
├── output/
│   ├── pdf/
│   └── html/
└── tests/
    └── test_templates.py
```

## requirements.txt
```txt
jinja2>=3.1.0
PyYAML>=6.0
pytest>=7.0.0
pyspellchecker>=0.7.0
```

## templates/base/programming_cheatsheet.md.j2
```markdown
---
title: {{ title }}
author: {{ author }}
date: {{ current_date('%B %d, %Y') }}
---

# {{ title }}

{{ copyright_notice() }}

## Quick Reference

{% if sections %}
{% for section in sections %}
### {{ section.title }}

{% if section.description %}
{{ section.description }}
{% endif %}

{% if section.code_examples %}
{% for example in section.code_examples %}
**{{ example.name }}:**
```{{ language|default('python') }}
{{ example.code }}
```

{% if example.output %}
**Output:**
```
{{ example.output }}
```
{% endif %}

{% if example.explanation %}
*{{ example.explanation }}*
{% endif %}

{% endfor %}
{% endif %}

{% if section.tips %}
**Tips:**
{% for tip in section.tips %}
- {{ tip }}
{% endfor %}
{% endif %}

---
{% endfor %}
{% endif %}

## Additional Resources

{% if resources %}
{% for resource in resources %}
- [{{ resource.title }}]({{ resource.url }})
{% endfor %}
{% endif %}

---
*Last updated: {{ current_date() }}*
```

## templates/base/music_theory.md.j2
```markdown
---
title: {{ title }}
author: {{ author }}
date: {{ current_date('%B %d, %Y') }}
---

# {{ title }}

{{ copyright_notice() }}

## Overview

{{ overview|default('Music theory reference guide') }}

{% if concepts %}
{% for concept in concepts %}
## {{ concept.name }}

{% if concept.definition %}
**Definition:** {{ concept.definition }}
{% endif %}

{% if concept.examples %}
### Examples

{% for example in concept.examples %}
- **{{ example.name }}**: {{ example.description }}
  {% if example.notation %}
  - Notation: `{{ example.notation }}`
  {% endif %}
{% endfor %}
{% endif %}

{% if concept.audio_examples %}
### Audio Examples
{% for audio in concept.audio_examples %}
- {{ audio.description }}: `{{ audio.file }}`
{% endfor %}
{% endif %}

{% if concept.exercises %}
### Practice Exercises
{% for exercise in concept.exercises %}
{{ loop.index }}. {{ exercise }}
{% endfor %}
{% endif %}

---
{% endfor %}
{% endif %}

## Summary

{% if summary %}
{{ summary }}
{% endif %}

---
*Generated on {{ current_date() }}*
```

## content/python_basics/config.yaml
```yaml
title: "Python Basics Cheat Sheet"
template: "base/programming_cheatsheet.md.j2"
language: "python"
category: "programming"
difficulty: "beginner"
version: "1.0"
```

## content/python_basics/content.yaml
```yaml
sections:
  - title: "Variables and Data Types"
    description: "Basic variable assignment and common data types"
    code_examples:
      - name: "String Variables"
        code: |
          # String assignment
          name = "Alice"
          greeting = f"Hello, {name}!"
          print(greeting)
        output: "Hello, Alice!"
        explanation: "Use f-strings for string interpolation"
      
      - name: "Numeric Types"
        code: |
          # Integer and float
          age = 25
          height = 5.8
          print(f"Age: {age}, Height: {height}")
        output: "Age: 25, Height: 5.8"
    
    tips:
      - "Python is dynamically typed - no need to declare variable types"
      - "Use descriptive variable names for better code readability"

  - title: "Lists and Dictionaries"
    description: "Working with Python's most common data structures"
    code_examples:
      - name: "List Operations"
        code: |
          # Creating and manipulating lists
          fruits = ["apple", "banana", "cherry"]
          fruits.append("date")
          print(fruits[0])  # First element
          print(len(fruits))  # Length
        output: |
          apple
          4
      
      - name: "Dictionary Basics"
        code: |
          # Key-value pairs
          person = {"name": "Bob", "age": 30}
          person["city"] = "New York"
          print(person["name"])
        output: "Bob"

resources:
  - title: "Python Official Documentation"
    url: "https://docs.python.org/3/"
  - title: "Real Python Tutorials"
    url: "https://realpython.com/"
```

## content/music_intervals/config.yaml
```yaml
title: "Music Intervals Guide"
template: "base/music_theory.md.j2"
category: "music_theory"
difficulty: "intermediate"
version: "1.0"
```

## content/music_intervals/content.yaml
```yaml
overview: "A comprehensive guide to understanding musical intervals and their applications"

concepts:
  - name: "Perfect Intervals"
    definition: "Intervals that maintain the same quality in major and minor scales"
    examples:
      - name: "Perfect Unison"
        description: "Same note, 0 semitones"
        notation: "C to C"
      - name: "Perfect Fourth"
        description: "5 semitones apart"
        notation: "C to F"
      - name: "Perfect Fifth"
        description: "7 semitones apart" 
        notation: "C to G"
    exercises:
      - "Identify perfect intervals in the C major scale"
      - "Play perfect fifths starting from each note of the chromatic scale"

  - name: "Major and Minor Intervals"
    definition: "Intervals that change quality between major and minor scales"
    examples:
      - name: "Major Second"
        description: "2 semitones (whole step)"
        notation: "C to D"
      - name: "Minor Second"
        description: "1 semitone (half step)"
        notation: "C to Db"
      - name: "Major Third"
        description: "4 semitones"
        notation: "C to E"
      - name: "Minor Third"
        description: "3 semitones"
        notation: "C to Eb"

summary: |
  Understanding intervals is fundamental to music theory. Perfect intervals (unison, 4th, 5th, octave) 
  remain constant, while major/minor intervals change based on the key signature. Practice identifying 
  these by ear and on your instrument for better musical understanding.
```

## templates/styles/custom.latex
```latex
\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{microtype}
\usepackage[margin=1in]{geometry}
\usepackage{xcolor}
\usepackage{listings}
\usepackage{fancyhdr}
\usepackage{titlesec}

% Color scheme
\definecolor{codegreen}{rgb}{0,0.6,0}
\definecolor{codegray}{rgb}{0.5,0.5,0.5}
\definecolor{codepurple}{rgb}{0.58,0,0.82}
\definecolor{backcolour}{rgb}{0.95,0.95,0.92}

% Code listing style
\lstdefinestyle{mystyle}{
    backgroundcolor=\color{backcolour},   
    commentstyle=\color{codegreen},
    keywordstyle=\color{magenta},
    numberstyle=\tiny\color{codegray},
    stringstyle=\color{codepurple},
    basicstyle=\ttfamily\footnotesize,
    breakatwhitespace=false,         
    breaklines=true,                 
    captionpos=b,                    
    keepspaces=true,                 
    numbers=left,                    
    numbersep=5pt,                  
    showspaces=false,                
    showstringspaces=false,
    showtabs=false,                  
    tabsize=2
}
\lstset{style=mystyle}

% Headers and footers
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\leftmark}
\fancyhead[R]{\thepage}
\fancyfoot[C]{$copyright$}

% Title formatting
\titleformat{\section}{\Large\bfseries}{\thesection}{1em}{}
\titleformat{\subsection}{\large\bfseries}{\thesubsection}{1em}{}

\begin{document}

$if(title)$
\title{$title$}
$endif$

$if(author)$
\author{$author$}
$endif$

$if(date)$
\date{$date$}
$endif$

$if(title)$
\maketitle
$endif$

$body$

\end{document}
```

## templates/styles/main.css
```css
/* Modern, clean CSS for HTML output */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    color: #333;
}

h1, h2, h3, h4, h5, h6 {
    color: #2c3e50;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
}

h1 {
    border-bottom: 3px solid #3498db;
    padding-bottom: 10px;
}

h2 {
    border-bottom: 2px solid #ecf0f1;
    padding-bottom: 5px;
}

code {
    background-color: #f8f9fa;
    padding: 2px 4px;
    border-radius: 3px;
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
}

pre {
    background-color: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 5px;
    padding: 15px;
    overflow-x: auto;
}

pre code {
    background-color: transparent;
    padding: 0;
}

blockquote {
    border-left: 4px solid #3498db;
    margin: 0;
    padding-left: 20px;
    font-style: italic;
    color: #555;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
}

th, td {
    border: 1px solid #ddd;
    padding: 8px 12px;
    text-align: left;
}

th {
    background-color: #f8f9fa;
    font-weight: bold;
}

.copyright {
    text-align: center;
    font-size: 0.9em;
    color: #666;
    border-top: 1px solid #eee;
    padding-top: 20px;
    margin-top: 40px;
}
```

## Usage Instructions

1. **Setup:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create content:**
   - Add directories under `content/`
   - Each directory needs `config.yaml` and `content.yaml`

3. **Process documents:**
   ```bash
   # Process all documents
   python templating_app.py batch
   
   # Process single document
   python templating_app.py single content/python_basics
   ```

4. **Customize templates:**
   - Edit templates in `templates/base/`
   - Modify styles in `templates/styles/`
   - Update global config in `config/global.yaml`

This structure scales exponentially - just add new content directories with their YAML files, and the batch processor handles the rest!
