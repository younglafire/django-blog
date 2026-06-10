from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render
from .models import Post
# Create your views here.

def post_list(request):
    post_list = Post.published.all()
# Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1) # get the page, default 1
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        # If page number is out of range, get the last page of results
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        # Get the first page
        posts = paginator.page(1)
    return render(
        request,
        'blog/post/list.html',
        {'posts': posts}
    )
    
    
def post_detail(request, year, month, day, post):

    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
    )
      
