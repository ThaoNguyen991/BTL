from .models import Category, House
from django.db.models import Count


def load_houses(params={}):
    q = House.objects.filter(active=True)

    kw = params.get('kw')
    if kw:
        q = q.filter(address__icontains=kw)

    cate_id = params.get('cate_id')
    if cate_id:
        q = q.filter(category_id=cate_id)

    return q


def count_houses_by_cate():
    return Category.objects.annotate(count=Count('houses__id')).values("id", "name", "count").order_by('-count')