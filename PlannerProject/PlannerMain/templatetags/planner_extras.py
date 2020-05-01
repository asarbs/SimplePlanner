from django import template

register = template.Library()

@register.simple_tag
def current_login(profile):
	return profile