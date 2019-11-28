from django import template
import markdown
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='zip')
def zip_lists(a, b):
    a = list(a)
    b = list(b)
    return zip(a, b)


@register.filter(name='add_css')
def add_css(value, arg):
    css_classes = value.field.widget.attrs.get('class', '')
    css_classes_list = css_classes.split(' ')
    if arg not in css_classes:
        if css_classes == '':
            css_classes = arg
        else:
            css_classes_list.append(arg)
            css_classes = ''
            for css_class in css_classes_list:
                css_classes = '{} {}'.format(css_classes, css_class)
    value.field.widget.attrs['class'] = css_classes
    return value


@register.filter(name='sub_or_zero')
def sub_or_zero(a, b):
    return a - b if a > b else 0


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.filter(name='fourth_objects')
def fourth_objects(object_list):
    return [instance for idx, instance in enumerate(object_list) if idx % 4 == 3]


@register.filter(name='third_objects')
def third_objects(object_list):
    return [instance for idx, instance in enumerate(object_list) if idx % 4 == 2]


@register.filter(name='second_objects')
def second_objects(object_list):
    return [instance for idx, instance in enumerate(object_list) if idx % 4 == 1]


@register.filter(name='first_objects')
def first_objects(object_list):
    return [instance for idx, instance in enumerate(object_list) if idx % 4 == 0]
