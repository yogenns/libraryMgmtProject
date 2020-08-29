import traceback
from django import template
register = template.Library()


@register.filter()
def times(min=5):
    # print(min)
    return range(1, min)


@register.filter()
def return_book_title(l, i):
    try:
        result = list(filter(lambda x: (x.book_index == i), l))
        return result[0].book.title
    except:
        return ''


@register.filter()
def return_book_cover(l, i):
    try:
        result = list(filter(lambda x: (x.book_index == i), l))
        return result[0].book.book_cover
    except:
        return ''


@register.filter()
def return_book_author(l, i):
    try:
        result = list(filter(lambda x: (x.book_index == i), l))
        return "By "+str(result[0].book.author)
    except:
        return ''


@register.filter()
def return_book_id(l, i):
    try:
        result = list(filter(lambda x: (x.book_index == i), l))
        return result[0].book.pk
    except:
        return ''
