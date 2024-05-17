from rest_framework.pagination import PageNumberPagination

class HousePaginator(PageNumberPagination):
    page_size = 3