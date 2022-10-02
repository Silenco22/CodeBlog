
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q

from blog.forms import CreateBlogPostForm, UpdateBlogPostForm, CommentForm, EditCommentForm
from account.models import Account
from blog.models import BlogPost, Comment
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

def create_blog_view(request):

    context = {}

    user = request.user

    if not user.is_authenticated:
        return redirect('must_authenticate')
    
    form = CreateBlogPostForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        obj = form.save(commit=False)
        author = Account.objects.filter(email=user.email).first()
        obj.author = author
        obj.save()
        form = CreateBlogPostForm()
    context['form'] = form

    return render(request, "blog/create_blog.html", context)

def detail_blog_view(request, slug):

    context = {}
    user = request.user
    blog_post = get_object_or_404(BlogPost, slug=slug)
    
    if request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            obj = comment_form.save(commit=False)
            author = Account.objects.filter(email=user.email).first()
            obj.author = author
            obj.post = blog_post 
            obj.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    
    comments = Comment.objects.filter(post=blog_post).order_by('-created_on')
    page = request.GET.get('page')
    results_per_page = 5
    paginator = Paginator(comments, results_per_page)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    
    
    context['blog_post'] = blog_post
    context['comment_form'] = comment_form
    context['comments'] = comments

    return render(request, 'blog/detail_blog.html', context)

def edit_blog_view(request, slug):

    context = {}
    user = request.user

    if not user.is_authenticated:
        return redirect("must_authenticate.html")
    
    
    blog_post = get_object_or_404(BlogPost, slug=slug)

    if blog_post.author != user:
        return HttpResponse("You are not the author of this post.")

    if request.POST:
        form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance = blog_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = "Updated"
            blog_post = obj
    form = UpdateBlogPostForm(
        initial={
            "title": blog_post.title,
            "body": blog_post.body,
            "image": blog_post.image,
        }
    )

    context['form'] = form

    return render(request, 'blog/edit_blog.html', context)


def get_blog_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = BlogPost.objects.filter(
            Q(title__icontains = q) | #q serach
            Q(body__icontains = q)
        ).distinct() #gives unique posts in that list

        for post in posts:
            queryset.append(post)
    
    return list(set(queryset))

def edit_commnet_view(request, slug, pk):

    context = {}
    user = request.user

    if not user.is_authenticated:
        return redirect("must_authenticate.html")
    
    comment = Comment.objects.filter(pk=pk)[0]

    if comment.author != user:
        return HttpResponse("You are not the author of this comment.")

    comment_form = CommentForm()
    if request.method == 'GET':
        comment_form = CommentForm(
            initial={
            "comment": comment.comment,
        }
        )
        context['comment_form'] = comment_form
        context['slug'] = slug
        return render(request, 'blog/edit_comment.html', context)
    
    if request.POST:
        comment_form = CommentForm(request.POST or None, request.FILES or None, instance = comment)
        if comment_form.is_valid():
            obj = comment_form.save(commit=False)
            obj.save()
            
    next = request.POST.get('next', '/')
    return redirect(next)

def delete_commnet_view(request, slug, pk):

    context = {}
    user = request.user
    
    if not user.is_authenticated:
        return redirect("must_authenticate.html")
    
    
    comment = Comment.objects.filter(pk=pk)[0]

    if comment.author != user:
        return HttpResponse("You are not the author of this comment.")

    if request.method == 'GET':
        context['slug'] = slug
        return render(request, 'blog/delete_comment.html', context)
    
    if request.POST:
        comment.delete()
        next = request.POST.get('next', '/')

        return redirect(next)

def add_like(request, slug, pk):

    if not request.user.is_authenticated:
        return redirect('must_authenticate')

    if request.POST:
        post = BlogPost.objects.get(pk=pk)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            post.dislikes.remove(request.user)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)

        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return redirect(next)

def add_dislike(request, slug, pk):

    if not request.user.is_authenticated:
        return redirect('must_authenticate')

    if request.POST:
        post = BlogPost.objects.get(pk=pk)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            post.likes.remove(request.user)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            post.dislikes.add(request.user)

        if is_dislike:
            post.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return redirect(next)


