from django import template

register = template.Library()

@register.inclusion_tag("tag_templates/btn.html")
def button(btn_context):
    return {'btn': btn_context}