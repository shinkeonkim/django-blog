from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog
from .form import PostForm
from django.utils import timezone

# Create your views here.
def post_list(request):
    posts = Blog.objects.all()
    return render(request, 'post_list.html', {'posts': posts})


def detail(request, post_id):
    post = get_object_or_404(Blog, pk =  post_id)
    return render(request, 'detail.html', {'post':post})


def new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.save(commit = False)
            content.published_at = timezone.datetime.now()
            content.save()
            return redirect('post_list')
    else:
        form = PostForm()
        return render(request, 'new.html', {'form':form})


def create(request):
    new_blog = Blog()
    new_blog.title = request.POST['title']
    new_blog.body = request.POST['body']
    new_blog.publisher = request.POST['publisher']
    new_blog.rep_img = request.FILES['rep_img']
    new_blog.hashtag = request.POST['hashtag']
    new_blog.published_at = timezone.datetime.now()
    new_blog.save()
    return redirect('/blog/'+str(new_blog.id))


def edit(request, post_id):
    form = PostForm(instance=Blog.objects.get(pk=post_id))
    return render(request, 'edit.html', {'form':form, 'post_id':post_id})

def update(request, post_id):
    update_blog = get_object_or_404(Blog, pk = post_id)
    update_blog.title = request.POST['title']
    update_blog.body = request.POST['body']
    update_blog.publisher = request.POST['publisher']
    try:
        update_blog.rep_img = request.FILES['rep_img']
    except:
        pass
    update_blog.hashtag = request.POST['hashtag']
    update_blog.save()
    return redirect('detail', update_blog.id)


def delete(request,post_id):
    delete_blog  = get_object_or_404(Blog, pk = post_id)
    delete_blog.delete()
    return redirect('/')