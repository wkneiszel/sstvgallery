from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Image, Comment

# Register your models here.
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    fields = ['photo', 'receive_date', 'votes', 'rating', 'image_preview']
    readonly_fields = ['image_preview']
    inlines = [CommentInline]
    list_display = ['image_name', 'image_preview']

    # Allows for the name (string representation) of the image to be displayed in the list display
    def image_name(self, obj):
        return str(obj)

    # Allows for a preview of the image to show up when viewing the image on the admin page. https://books.agiliq.com/projects/django-admin-cookbook/en/latest/imagefield.html
    def image_preview(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                url = obj.photo.url,
                width = obj.photo.width,
                height = obj.photo.height,
            )
        )