from django.db.models import Count

from .models import Category, House


def load_house(params = {}):
    q = House.objects.all()
    kw = params.get('kw')
    if kw:
        q = q.objects.filter(address__icontains=kw)
    cate = params.get('cate_id')
    if cate:
        q = q.objects.filter(category_id=cate)


def count_house_by_cat():
    return Category.objects.annotate(count = Count('house__id')).values('id', 'name', 'count')
