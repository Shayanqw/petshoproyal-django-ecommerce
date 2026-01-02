from django.contrib import admin
from .models import *
import admin_thumbnails


class ProductvariatnInlines(admin.TabularInline):
    model = Variants
    extra = 1

@admin_thumbnails.thumbnail('image')
class ImageInlines(admin.TabularInline):
    model = Images
    extra = 2



class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','create','update','sub_category',)
    list_filter = ('create',)
    prepopulated_fields = {
        'slug':('name',)
    }

class ChartAdmin(admin.TabularInline):
    model = Chart
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','create','update','amount','available','unit_price','discount','total_price','sell']
    # prepopulated_fields = {
    #     'slug' : ('name',)
    # }
    list_filter = ['available','create']
    list_editable = ('amount',)
    change_list_template = 'home/change.html'
    raw_id_fields = ('category',)
    inlines =[ProductvariatnInlines,ImageInlines,ChartAdmin]


class VariantsAdmin(admin.ModelAdmin):
    list_display = ['name', 'weight', 'id']

class SizeAdmin(admin.ModelAdmin):
    list_display = ['name','id']

class ColorAdmin(admin.ModelAdmin):
    list_display = ['name','id']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['user','create','rate']

class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_date']
    search_fields = ['title', 'description']
    fields = ['title', 'image', 'published_date', 'description']  # Controls the form layout


admin.site.register(Blog, BlogAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Variants,VariantsAdmin)
admin.site.register(Size,SizeAdmin)
admin.site.register(Color,ColorAdmin)
admin.site.register(Commnet,CommentAdmin)
admin.site.register(Images)
admin.site.register(Brand)
admin.site.register(Gallery)
admin.site.register(Chart)
admin.site.register(Views)


