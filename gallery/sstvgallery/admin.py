from django.contrib import admin

from .models import Image, Comment

# Register your models here.
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class ImageAdmin(admin.ModelAdmin):
    fields = ['photo', 'receive_date', 'votes', 'rating']
    inlines = [CommentInline]

admin.site.register(Image, ImageAdmin)