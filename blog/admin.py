from django.contrib import admin

from blog.models import BlogPost, Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post')
    fields = ('author', 'post', 'comment', 'created_on', 'updated_at')
    # search_fields = ('user', 'remote_addr', 'device_family')
    ordering = ('-created_on',)
    readonly_fields = ('created_on', 'updated_at')

admin.site.register(BlogPost)
admin.site.register(Comment, CommentAdmin)
