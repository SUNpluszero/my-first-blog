from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Comment, Document
from .forms import PostForm, CommentForm, UserForm, DocumentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
	
	return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post': post, 'currentuser': request.user.pk,  'currentusername': request.user.username })

@login_required
def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.publish()
	return redirect('post_detail',pk=pk)

def publish(self):
	self.published_date = timezone.now()
	self.save()

@login_required
def post_remove(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.delete()
	return redirect('post_list')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            if request.user.is_authenticated():
            	comment.author = request.user.username
            else:
            	comment.author = "Anonymous"
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
        if request.user.is_authenticated():
            author = request.user.username
        else:
        	author = "Anonymous"
    return render(request, 'blog/add_comment_to_post.html', {'form': form, 'name' : author} )

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

def register(request):
	if request.method == 'POST':
		form = UserForm(request.POST)
		print(form)
		if form.is_valid():
			form_data = form.cleaned_data
			user = User.objects.create_user(
				username=form_data['username'],
				password=form_data['password'], 
				email=form_data['email']
			)
			user.save()
			return render(request,'blog/congrat_register.html')
		else:
			form = UserForm()
			return render(request, 'registration/register_wrong.html', {'form': form })
	else:
		form = UserForm()
		return render(request, 'registration/register.html', {'form': form })

def model_form_upload(request):
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('post_list')
	else:
		form = DocumentForm()
	return render(request, 'blog/model_form_upload.html',{'form':form})

@login_required
def mypage(request):
	userinfo = request.user
	return render(request,'blog/mypage.html', {'userinfo' : userinfo})
