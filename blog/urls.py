from django.urls import path
from .feeds import LatestPostsFeed   
from blog.views import post_list, post_detail, post_share
app_name = 'blog'

urlpatterns = [
    path('', post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
    post_detail, name='post_detail'),
    path('tag/<int:pk>/',post_list, name='post_list_by_tag'),
    path('<int:post_id>/share/', post_share, name='post_share'),
    path('feed/', LatestPostsFeed(), name='post_feed'), 
]

# http://test/1997/08/07/firstproject/