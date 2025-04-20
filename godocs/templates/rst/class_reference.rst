{% include "heading.rst" %}
{% if class.description %}{% include "description.rst" %}{% endif %}
{% if class.properties %}{% include "property_index.rst" %}{% endif %}
{% if class.methods %}{% include "method_index.rst" %}{% endif %}
{% if class.constants %}{% include "constant_descriptions.rst" %}{% endif %}
{% if class.signals %}{% include "signal_descriptions.rst" %}{% endif %}
{% if class.properties %}{% include "property_descriptions.rst" %}{% endif %}
{% if class.methods %}{% include "method_descriptions.rst" %}{% endif %}