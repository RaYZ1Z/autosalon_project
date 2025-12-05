from django import template

register = template.Library()


@register.filter
def remove_param(urlencode, param_to_remove):
    """
    Удаляет параметр из строки GET-запроса
    Использование: {{ request.GET.urlencode|remove_param:'search' }}
    """
    if not urlencode:
        return ''

    params = urlencode.split('&')
    filtered_params = []

    for param in params:
        key = param.split('=')[0] if '=' in param else param
        if key != param_to_remove:
            filtered_params.append(param)

    return '&'.join(filtered_params)