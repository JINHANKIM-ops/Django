from django.urls import path
from blog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post'),
    path('post/create', views.PostCreate.as_view(), name='post_create'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('update/<int:pk>', views.PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>', views.PostDeleteView.as_view(), name='post_delete'),
    path('conn_write/<int:post_pk>', views.conn_write, name='post_comment_write'),
    path('conn_update/<int:pk>', views.conn_update, name='post_comment_update'),
    path('conn_delete/<int:pk>', views.conn_delete, name='post_comment_delete'),
    path('down/<int:pk>', views.file_download_view, name='file_down'),
]
