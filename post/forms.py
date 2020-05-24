from django import forms
from .models import Post,Comment

class PostForm(forms.ModelForm):
	title = forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder': 'Write a Post'}))
	image = forms.ImageField(required=False)
	class Meta:
		model = Post
		fields = ('title','image')

class PostEditForm(forms.ModelForm):
	title = forms.CharField()
	image = forms.ImageField(required=False)
	class Meta:
		model = Post
		fields = ('title','image')

class CommentForm(forms.ModelForm):
	texts = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'Write a comment'}))

	class Meta:
		model = Comment
		fields = ('texts',)