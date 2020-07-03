from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog, Comment
from .form import PostForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.
def post_list(request):
    posts = Blog.objects.all()
    for post in posts:
        post.represent_user = ""
        if len(post.like_users.all()) > 0:
            post.represent_user = post.like_users.all()[0].username

    return render(request, 'post_list.html', {'posts': posts})


def detail(request, post_id):
    post = get_object_or_404(Blog, pk=post_id)
    comments = Comment.objects.filter(blog=post)
    post.represent_user = ""
    if len(post.like_users.all()) > 0:
        post.represent_user = post.like_users.all()[0].username
    return render(request, 'detail.html', {'post': post, 'comments': comments})


@login_required(login_url='/account/login/')
def commenting(request, post_id):
    new_comment = Comment()
    new_comment.blog = get_object_or_404(Blog, pk=post_id)
    new_comment.author = request.user
    new_comment.body = request.POST.get('body')
    new_comment.save()
    return redirect('/blog/' + str(post_id))


@login_required(login_url='/account/login/')
def like(request):
    # ajax 통신을 통해서 template에서 POST방식으로 전달
    post_id = request.POST.get('post_id', None)

    post = get_object_or_404(Blog, pk=post_id)

    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
        message = "좋아요 취소"
    else:
        post.like_users.add(request.user)
        message = "좋아요"
    
    represent_user = ""
    if len(post.like_users.all()) > 0:
        represent_user = post.like_users.all()[0].username


    context = {'like_count': str(post.like_count()),
               'message': message,
               'username': str(request.user.username),
               'represent_user': represent_user}
    
    return HttpResponse(json.dumps(context), content_type="application/json")


@login_required(login_url='/account/login/')
def new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.save(commit=False)
            content.published_at = timezone.datetime.now()
            content.publisher = request.user.username
            content.save()
            return redirect('post_list')
    else:
        form = PostForm()
        return render(request, 'new.html', {'form': form})


@login_required(login_url='/account/login/')
def edit(request, post_id):
    user = request.user
    form = PostForm(instance=Blog.objects.get(pk=post_id))
    if user.is_authenticated and Blog.objects.get(pk=post_id).publisher == user.username:
        return render(request, 'edit.html', {'form': form, 'post_id': post_id})
    elif user.is_authenticated:
        return redirect('/')
    else:
        return redirect("login")


def update(request, post_id):
    update_blog = get_object_or_404(Blog, pk=post_id)
    update_blog.title = request.POST['title']
    update_blog.body = request.POST['body']
    try:
        update_blog.rep_img = request.FILES['rep_img']
    except:
        pass
    update_blog.hashtag = request.POST['hashtag']
    update_blog.save()
    return redirect('detail', update_blog.id)


@login_required(login_url='/account/login/')
def delete(request, post_id):
    user = request.user
    if user.is_authenticated and Blog.objects.get(pk=post_id).publisher == user.username:
        delete_blog = get_object_or_404(Blog, pk=post_id)
        delete_blog.delete()
        return redirect('/')
    elif user.is_authenticated:
        return redirect('/')
    else:
        return redirect("login")
