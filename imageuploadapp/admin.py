from django.contrib import admin
from .models import UploadImage

class UploadImageAdmin(admin.ModelAdmin):
    list_display = ['user', 'image_type', 'created_at']  # Customize the displayed fields in the admin list view

admin.site.register(UploadImage, UploadImageAdmin)