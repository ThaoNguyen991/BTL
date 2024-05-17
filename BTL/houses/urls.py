from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('houses/', views.index, name="index"),
    path('houses/<int:house_id>', views.list, name="list"),
    path('category/', views.CategoryView.as_view())
]