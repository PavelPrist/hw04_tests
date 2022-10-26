from django.conf import settings
from django.core.paginator import Paginator


def paginator_page(request, queryset):
    '''
    Make paginator with queryset
    '''
    paginator = Paginator(queryset, settings.POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
