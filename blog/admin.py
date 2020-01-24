from django.contrib import admin
from blog.models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id','title', 'slug', 'author', 'publish','status'
        )
    list_filter = (
        'status', 'created', 'publish', 'author'
    )
    
    search_fields = (
        'title', 'body'
    )
    prepopulated_fields = {'slug': ('title',),}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish' 
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'author', 'email', 'post', 
        'created_at', 'updated_at'
        )
    
    list_filter = (
        'active', 'created_at', 'updated_at'
    )
    search_fields = (
        'author', 'email', 'body'
    )




