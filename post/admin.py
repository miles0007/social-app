from django.contrib import admin
from .models import Post, Comment
# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('title','description','created','user')
	list_filter = ('title','created','user')
	search_fields = ('title','description')

# admin.site.register(Comment)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('texts','author','created','active')
	list_filter = ('author','created','active')
	search_fields = ('texts',)