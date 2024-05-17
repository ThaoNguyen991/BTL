from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.safestring import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Category, House, User, Number, Room
from .dao import count_house_by_cat


# Register your models here.
class HouseAppAdminSite(admin.AdminSite):
    site_header = "HỆ THỐNG TÌM KIẾM TRỌ"

    def get_urls(self):
        return [
                   path('house-stats/', self.stats_view)
               ] + super().get_urls()

    def stats_view(self, request):
        stats = count_house_by_cat()
        return TemplateResponse(request, 'admin/stats_view.html',context={
            'stats': stats
        })


class HouseNumberInlineAdmin(admin.TabularInline):
    model = House.numbers.through

class RoomNumberInlineAdmin(admin.TabularInline):
    model = Room.numbers.through

class HouseForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = House
        fields = '__all__'

class RoomForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Room
        fields = '__all__'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    list_filter = ['id', 'name']


class HouseAdmin(admin.ModelAdmin):
    list_display = ['id', 'address', 'description']
    search_fields = ['address']
    list_filter = ['id', 'address']
    form = HouseForm
    inlines = [HouseNumberInlineAdmin]
    readonly_fields = ['ava']
    class Media:
        css = {
            'all': ('/static/css/style.css',)
        }
    def ava(self, obj):
        if obj:
            return mark_safe(
                '<img src="/static/{url}" width="120" />' \
                    .format(url=obj.image.name)
            )

class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'roomname', 'description']
    form = RoomForm
    inlines = [RoomNumberInlineAdmin]
    readonly_fields = ['ava']
    def ava(self, obj):
        if obj:
            return mark_safe(
                '<img src="/static/{url}" width="120" />' \
                    .format(url=obj.image.name)
            )

admin_site = HouseAppAdminSite(name="myapp")

admin_site.register(Category, CategoryAdmin)
admin_site.register(House, HouseAdmin)
admin_site.register(User)
admin_site.register(Number)
admin_site.register(Room, RoomAdmin)