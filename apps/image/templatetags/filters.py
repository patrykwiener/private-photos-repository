"""This module contains custom template filters for image application."""
import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='zip')
def zip_lists(first, second):
    """
    Zips two lists.

    :param first: first list to zip
    :param second: second list to zip
    :return: zipped two lists
    """
    first = list(first)
    second = list(second)
    return zip(first, second)


@register.filter(name='markdown')
def markdown_format(text):
    """
    Converts markdown text to HTML code.

    :param text: text to convert
    :return: converted markdown text to HTML code
    """
    return mark_safe(markdown.markdown(text))
