from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'recipient', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('sender__username', 'recipient__username', 'content')
