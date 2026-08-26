from django.contrib import admin
from .models import Request

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'request_type', 'is_active', 'created_at')
    list_filter = ('request_type', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'author__username')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_active',)