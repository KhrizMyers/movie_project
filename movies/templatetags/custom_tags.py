from django.templatetags.static import register


@register.simple_tag
def active_page(request, view_name):
    from django.urls import resolve, Resolver404
    if not request:
        return ""
    try:
        return "active" if resolve(request.path_info).view_name == view_name else ""
    except Resolver404:
        return ""
