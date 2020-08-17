from django.contrib import admin
from blog.models import Category, Tag, Post
from markdownx.admin import MarkdownxModelAdmin

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post, MarkdownxModelAdmin)
