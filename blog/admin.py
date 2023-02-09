from django.contrib import admin
from blog.models import Post, Comment, Preference, DeletedData, ActivityLog


class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'action')


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Preference)
admin.site.register(DeletedData)
admin.site.register(ActivityLog)
