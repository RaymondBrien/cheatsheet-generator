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


---

{% if resources %}
{% for resource in resources %}
- [{{ resource.title }}]({{ resource.url }})
{% endfor %}
{% endif %}

---
*Last updated: {{ current_date() }}*
