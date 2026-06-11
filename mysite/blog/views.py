from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render
from .models import Post
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail
# Create your views here.

class PostListView(ListView):
    """
    Using class-based view will return 404 for pagination instead of Empty or NotInteger,
    which is more easy to handle 
    """
    queryset= Post.published.all()
    context_object_name = 'posts' # if not specify, it will be object_list
    paginate_by = 3 # ListView comes with page_obj for pagination, don't have to import anything
    template_name = 'blog/post/list.html'


# Not in use
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
      
def post_share(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data # convert data to dict
            # this line means it will have the http:// stuff
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject =(
                f"{cd['name']} ({cd['email']})"
                f"recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments: {cd['comments']}"
            )

            send_mail(
                subject=subject,
                message=message,
                from_email=None, # It will use the default one
                recipient_list= [cd['to']]
            )
            sent = True
            
            
    else:
        form = EmailPostForm()
    return render(
        request,
        'blog/post/share.html',
        {
            'post': post,
            'form': form,
            'sent' : sent
        }
    )
        
     