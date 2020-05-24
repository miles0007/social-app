from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post
from .forms import PostForm,PostEditForm,CommentForm
from django.http import JsonResponse                
from common.decorators import ajax_required
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string 
# Create your views here.

@login_required
def post_list(request):
	obj_list = Post.objects.all().order_by('-created')
	paginator = Paginator(obj_list, 5)
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	# form posting
	form = PostForm(request.POST or None, request.FILES or None)
	if request.method == "POST":
		if form.is_valid():
			obj = form.save(commit=False)
			obj.user = request.user;
			obj.save()
			messages.success(request,"Post has been added Succesfully.")
			return redirect('post:post_list_view')
		else:
			form = PostForm()
	return render(request,'post/post_view.html',
							{'posts' : posts,
							 'page' : page,
							 'form': form})
@login_required
def post_detail(request, id):
	post = get_object_or_404(Post, id=id)

	#like section
	is_liked = False
	if post.likes.filter(id=request.user.id).exists():
		is_liked = True
	total_likes = post.total_likes()

	# comment section
	comments = post.comment.filter(active=True)
	new_comment = None
	if request.method == 'POST':
		form = CommentForm(data=request.POST)
		if form.is_valid():
			data = form.cleaned_data['texts']
			post.comment.create(texts=data,author=request.user)
			# new_comment.save()
	else:
		form = CommentForm()

	return render(request,'post/post_full.html',{'post':post,
												 'is_liked':is_liked,
												 'total_likes':total_likes,
												 'form':form,
												 'comments':comments})
@login_required
def like_post(request):
	post = get_object_or_404(Post, id=request.POST.get('post_id'))
	is_liked = False
	if post.likes.filter(id=request.user.id).exists():
		post.likes.remove(request.user)
		is_liked = False 
	else:
		post.likes.add(request.user)
		is_liked = True
	context = {'post':post,
			   'is_liked':is_liked,
			   'total_likes':post.total_likes()
    }
	# return HttpResponseRedirect(post.get_absolute_url())
	if request.is_ajax():
		html = render_to_string('post/like_section.html',context,request=request)
		return JsonResponse({'form':html})

def my_post(request):
	posts = Post.objects.filter(user=request.user).order_by('-created')
	return render(request,'post/my_post.html',{'posts':posts})

def post_edit(request,id):
	post = Post.objects.get(id=id)
	if request.method == "POST":
		form = PostEditForm(request.POST, instance=post,files=request.FILES)
		if form.is_valid():
			form.save()
			return redirect('post:my_post')
		else:
			form = PostEditForm(instance=post)
	else:
		form = PostEditForm(instance=post)
	return render(request,'post/edit_form.html',
				 {'form' : form, 'post':post})

@login_required
def post_delete(request,id):
	post = Post.objects.get(id=id)
	post.delete()
	messages.success(request,"Post has been deleted Succesfully")
	return redirect('post:my_post')

