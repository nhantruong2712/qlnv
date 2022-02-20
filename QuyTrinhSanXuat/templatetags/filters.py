from django import template

register = template.Library()


def thousand_format(value):
    return '{0:,}'.format(round(value))


register.filter('thousand_format', thousand_format)