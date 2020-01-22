from django.shortcuts import render, get_object_or_404
from blog.models import Post
from django.views.generic import ListView
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Function Based View
# def post_list(request):
#     object_list = Post.published.all()
#     paginator = Paginator(object_list, 1)
#     page = request.GET.get('page')
#     print(dir(request))
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)

#     return render(
#         request, 'blog/post_list.html', {
#             'posts': posts, 'page': page,
#             }
#     )


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post_list.html'

def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post, slug=post, status='published', 
        publish__year=year, publish__month=month, 
        publish__day=day
    )
    return render(
        request, 'blog/post_detail.html', {'post': post}
    )