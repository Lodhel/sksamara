from django.contrib import admin
from html_mailer.models import Message, DontSendEntry, MessageLog


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'to_address', 'subject', 'when_added', 'priority')
    search_fields = ('to_address',)
    list_filter = ('priority',)

class DontSendEntryAdmin(admin.ModelAdmin):
    list_display = ('to_address', 'when_added')
    search_fields = ('to_address',)

class MessageLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'to_address', 'subject', 'when_attempted', 'result')
    search_fields = ('to_address',)

admin.site.register(Message, MessageAdmin)
admin.site.register(DontSendEntry, DontSendEntryAdmin)
admin.site.register(MessageLog, MessageLogAdmin)


