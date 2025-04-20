{% include "heading.rst" %}
{% if class.description %}{% include "description.rst" %}{% endif %}
{% if class.properties %}{% include "property_index.rst" %}{% endif %}
{% if class.methods %}{% include "method_index.rst" %}{% endif %}
{% if class.properties %}{% include "property_descriptions.rst" %}{% endif %}