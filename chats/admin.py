from django.contrib import admin
from .models import Chat, Message

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('sender', 'content', 'timestamp')
    can_delete = True
    
    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'participants_list', 'last_message_preview', 'updated_at')
    list_filter = ('updated_at', 'created_at')
    search_fields = ('participants__username',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [MessageInline]
    
    def participants_list(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])
    participants_list.short_description = 'Participants'
    
    def last_message_preview(self, obj):
        last_msg = obj.messages.last()
        if last_msg:
            return f"{last_msg.sender.username}: {last_msg.content[:30]}"
        return "No messages"
    last_message_preview.short_description = 'Last Message'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'sender', 'content_preview', 'timestamp')
    list_filter = ('timestamp', 'sender')
    search_fields = ('content', 'sender__username', 'chat__id')
    readonly_fields = ('timestamp',)
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'