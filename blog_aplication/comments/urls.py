from django.urls import path
from .views import CommentCreateView, CommentDeleteView

#app_name = 'comments'

urlpatterns = [
    path('post/<int:post_id>/comment/', CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
]