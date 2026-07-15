from django.urls import path
from . import views

urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog'),
    path('<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('comment/<int:post_id>/', views.AddCommentView.as_view(), name='add_comment'),
]