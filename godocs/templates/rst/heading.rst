
{{ "=" * class.name|length }}
{{ class.name }}
{{ "=" * class.name|length }}

**Inherits:** {% for parent in class.parents %}{% with title=parent, target=parent %}{% include "ref.rst" with context %}{% endwith %}{% if not loop.last %} **<** {% endif %}{% endfor %}

{{ class.brief_description }}
