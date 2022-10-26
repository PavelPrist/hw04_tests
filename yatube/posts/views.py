from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .utils import paginator_page

from .models import Group, Post, User


def index(request):
    posts = Post.objects.select_related("group")
    page_obj = paginator_page(request, posts)

    template = 'posts/index.html'
    context = {
        'page_obj': page_obj
    }
    return render(request, template, context)


def group_posts(request, slug):

    group = get_object_or_404(Group, slug=slug)
    posts = group.groups.filter(group=group)
    page_obj = paginator_page(request, posts)
    template = 'posts/group_list.html'
    context = {
        'group': group,
        'page_obj': page_obj
    }
    return render(request, template, context)


def profile(request, username):

    users = get_object_or_404(User, username=username)
    posts = users.posts.all()
    page_obj = paginator_page(request, posts)
    count = posts.count
    template = 'posts/profile.html'
    context = {
        'page_obj': page_obj,
        'count': count,
        'author': users,
    }
    return render(request, template, context)


def post_detail(request, post_id):

    post = Post.objects.get(id=post_id)
    template = 'posts/post_detail.html'
    context = {
        'post': post,
    }
    return render(request, template, context)


@login_required
def post_create(request):

    form = PostForm(request.POST or None)

    if form.is_valid():
        form = form.save(commit=False)
        form.author = request.user
        form.save()
        return redirect('posts:profile', request.user.username)

    template = 'posts/create_post.html'
    context = {
        'form': form,
        'is_edit': False
    }
    return render(request, template, context)


@login_required
def post_edit(request, post_id):

    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:

        return redirect('posts:post_detail', post.id)

    form = PostForm(request.POST or None, instance=post)

    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post.id)

    template = 'posts/create_post.html'
    context = {
        'form': form,
        'is_edit': True
    }
    return render(request, template, context)
