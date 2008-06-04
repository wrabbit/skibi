import datetime

from django import template 
from django.template import resolve_variable
from django.conf import settings

from e_dziennik.models import Aktualnosci


register = template.Library()




@register.tag('get_yearly_archive')
def do_archive_year(parser, token):
    ''' get_yearly_archive as archive_list '''
    
    bits = token.contents.split()
    if len(bits) == 3 and bits[1] == 'as':
        return YearArchiveNode(bits[2])
    else:
        return template.TemplateSyntaxError

class YearArchiveNode(template.Node):
    def __init__(self, context_variable):
        self.context_variable = context_variable

    def render(self, context):
        date_list = Aktualnosci.objects.current_active().dates('news_date', 'month', order='DESC')
        context[self.context_variable] = date_list
        return ''

@register.filter
def year(date_list):
    return date_list[0].year
