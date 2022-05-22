from django.contrib import admin
from .models import Post, Comment
from re import search
# Register your models here.

admin.site.site_header= "Bloging"
admin.site.site_title= "Durjoy's world"
admin.site.index_title= "Manage Now"

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display= ('title','slug','author', 'publish', 'status')
    list_fields =('title','body')
    list_filter = ('status','created', 'publish','author')
    prepopulated_fields= {'slug':('title',)}
    raw_id_fields= ('author',)
    date_hierarchy= 'publish'
    ordering= ('status','publish')
    search_fields= ('title',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display= ('name','email', 'post', 'created', 'active')
    list_filter= ('active','created', 'updated')
    search_fields= ('name', 'email', 'body')