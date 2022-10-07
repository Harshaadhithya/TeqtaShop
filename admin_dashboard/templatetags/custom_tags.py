from django import template

register = template.Library()

@register.simple_tag(name = 'get_list_ele')
def get_list_ele(value,index):
    return value[int(index)]

# register.filter('get_list_ele', get_list_ele)
