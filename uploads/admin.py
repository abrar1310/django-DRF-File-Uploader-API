from django.contrib import admin
from .models import Upload

@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'original_name', 'extension', 'mime_type', 'size_bytes', 'is_image', 'created_at')
    list_filter = ('is_image', 'created_at', 'extension')
    search_fields = ('original_name', 'sha256')
    readonly_fields = ('sha256', 'size_bytes', 'mime_type', 'is_image', 'created_at')
