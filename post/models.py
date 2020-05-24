from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.

class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='post')
	title = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	image = models.ImageField(upload_to='storage/',blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	likes = models.ManyToManyField(User,related_name='likes',
										blank=True)


	def __str__(self):
		return self.title

	def date_posted(self):
		return self.created.strftime('%b %d %Y')

	def total_likes(self):
		return self.likes.count()

	def get_absolute_url(self):
		return reverse('post:post_detail',args=[self.id])


class Comment(models.Model):
	user = models.ForeignKey(Post,on_delete=models.CASCADE,
												related_name='comment')
	texts = models.TextField()
	active = models.BooleanField(default=True,null=True)
	author = models.CharField(max_length=100,null=True)
	created = models.DateTimeField(auto_now_add=True)

	def date_commented(self):
		return self.created.strftime('%b %d')