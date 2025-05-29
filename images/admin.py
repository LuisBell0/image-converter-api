from django.contrib import admin

from .models import ImageConversion


class ImageConversionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'converted_image', 'conversion_format', 'created_at', 'updated_at')


admin.site.register(ImageConversion, ImageConversionAdmin)
