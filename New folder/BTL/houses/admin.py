from django.contrib import admin
from django.template.response import TemplateResponse

from .models import Category, House, Room, Number
from django.utils.html import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.urls import path
from houses import dao


class HouseAppAdminSite(admin.AdminSite):
    site_header = 'HỆ THỐNG TÌM KIẾM TRỌ'

    def get_urls(self):
        return [
                   path('house-stats/', self.stats_view)
               ] + super().get_urls()

    def stats_view(self, request):
        return TemplateResponse(request, 'admin/stats.html', {
            'stats': dao.count_houses_by_cate()
        })


admin_site = HouseAppAdminSite(name='myapp')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']
    search_fields = ['name']
    list_filter = ['id', 'name']


class HouseForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = House
        fields = '__all__'


class NumberInlineAdmin(admin.StackedInline):
    model = House.numbers.through


class HouseAdmin(admin.ModelAdmin):
    list_display = ['pk', 'address', 'created_date', 'updated_date', 'category', 'active']
    readonly_fields = ['img']
    search_fields = ['address']
    list_filter = ['address']
    inlines = [NumberInlineAdmin]
    form = HouseForm

    def img(self, house):
        if house:
            return mark_safe(
                '<img src="/static/{url}" width="120" />'.format(url=house.image.name)
            )

    class Media:
        css = {
            'all': ('/static/css/style.css', )
        }


class RoomNumberInlineAdmin(admin.TabularInline):
    model = Room.numbers.through

class RoomForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Room
        fields = '__all__'


class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'roomname','price', 'content']
    form = RoomForm
    search_fields = ['price']
    list_filter = [ 'price']
    inlines = [RoomNumberInlineAdmin]

    def ava(self, obj):
        if obj:
            return mark_safe(
                '<img src="/static/{url}" width="120" />' \
                    .format(url=obj.image.name)
            )


admin_site.register(Category, CategoryAdmin)
admin_site.register(House, HouseAdmin)
admin_site.register(Room,RoomAdmin)
admin_site.register(Number)
