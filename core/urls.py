from . import views
from django.urls import path
from django.conf import settings
from .views import PostLikeView
# CommentListCreateView, CommentRetrieveUpdateDestroyView


urlpatterns = [
    path('homepage/', views.homepage, name='posts_home'),
    path("", views.PostListCreateView.as_view(), name="list_post"),
    path("<int:pk>/", views.PostRetrieveUpdateDeleteView.as_view(),
         name="post_by_id"),
    path('current_user/', views.get_post_for_current_user, name='current_user'),
    path('posts_for/', views.ListPOstForAuthor.as_view(),
         name='posts_for_Authon',),
    path('<int:pk>/like/', PostLikeView.as_view(), name='post-like'),
    # path('', CommentListCreateView.as_view(), name='comment_list_create'),
    # path('<int:pk>/', CommentRetrieveUpdateDestroyView.as_view(),
    #     name='comment_retrieve_update_destroy'),
]
