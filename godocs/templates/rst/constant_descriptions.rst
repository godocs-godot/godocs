
{% set title = "Constant Descriptions" -%}
{{ title }}
{{ "=" * title | length }}

{% for constant in class.constants %}
.. _{{ constant.name | join_code_member_name(class.name) | make_code_member_label_target(ref_prefix) }}:

{% set signature = constant.name | join_code_member_name(class.name) | make_property_signature(constant.type, ref_prefix, constant.value, False, False) -%}
{{ signature }}
{{ "-" * signature | length }}

{{ constant.description }}

{% endfor %}
