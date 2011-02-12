from django.contrib import admin
from todo.models import Item, User, List, Comment, Effort

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'list', 'priority', 'due_date')
    list_filter = ('list',)
    ordering = ('priority',)
    search_fields = ('name',)


admin.site.register(List)
admin.site.register(Comment)
admin.site.register(Effort)
admin.site.register(Item,ItemAdmin)
