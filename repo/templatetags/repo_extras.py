from django import template

register = template.Library()


@register.filter
def one_more(_chordchoices, _keyindex):
    return _chordchoices, _keyindex


def return_item(l, i):
    return l[i]


# usage {{_1 | one_more: _2 | return_item: _3}}
