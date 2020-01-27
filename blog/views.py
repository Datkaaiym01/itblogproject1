from django.shortcuts import render, get_object_or_404
from blog.models import Post, Comment
from django.views.generic import ListView
from blog.forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.contrib.auth.models import User
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Function Based View
def post_list(request, pk=None):
    object_list = Post.published.all()
    tag = None
    # print(tag_slug)
    if pk:
        tag = get_object_or_404(Tag, pk=pk)
        object_list = object_list.filter(tags__in=[tag])
    # print(tag_slug)
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    # print(dir(request))
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(
        request, 'blog/post_list.html', {
            'posts': posts, 'page': page,
            'tag': tag
            }
    )


# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post_list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post, slug=post, status='published', 
        publish__year=year, publish__month=month, 
        publish__day=day
    )
    comments = post.comments.filter(active=True) 
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            user = User.objects.get(pk=request.user.pk)
            print(user)
            new_comment.author = user
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(
        request, 'blog/post_detail.html', {
            'post': post, 'comments': comments,
            'new_comment': new_comment, 
            'comment_form': comment_form

            }
    )

def post_share(request, post_id):
    # Получение статьи по идентификатору.
    post = get_object_or_404(
        Post, id=post_id,status='published'
        ) 
    sent=False
    if request.method == 'POST':
        # Форма была отправлена на сохранение. 
        form = EmailPostForm(request.POST)
        print(form)
        if form.is_valid():
        # Все поля формы прошли валидацию. 
            cd = form.cleaned_data
            print(cd)
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
                )
            print(post_url)
            subject = '{} ({}) recommends you reading "{}"'.format(
                cd['name'], cd['email'], post.title)

            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(
                post.title, post_url, cd['name'], cd['comments']
                )
            send_mail(
                subject, message, 
                'alymbekovdastan1@gmail.com', [cd['to']]
                )
            sent = True
            # {'name':'asdsa', 'email': 'adsad'}
        # ... Отправка электронной почты.
    else:
        form = EmailPostForm()
            
    return render(request, 'blog/share.html',
            {'post': post, 'form': form, 'sent': sent})