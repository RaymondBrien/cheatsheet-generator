title: {{ title }}
author: {{ author }}
date: {{ current_date('%B %d, %Y') }}

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


{% endfor %}
{% endif %}

## Summary

{% if summary %}
{{ summary }}
{% endif %}


*Generated on {{ current_date() }}*
