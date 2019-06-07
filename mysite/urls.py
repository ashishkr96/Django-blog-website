from django.urls import path
from mysite import views
from django.contrib.auth.views import LoginView as Login
from django.contrib.auth.views import LogoutView as Logout

from .views import PostUpdateView, PostDeleteView

urlpatterns = [
    path('', views.post_listview, name='blog-home'),
    path('post-draft/', views.post_draft, name='post-draft'),

    path('post/user/<int:author>/', views.user_post, name='user-post'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('comment/<int:id>/delete/', views.delete_comment, name='comment-delete'),
    path('post/new/', views.create_post, name='post-create'),
    path('about/', views.about, name='blog-about'),
    path('profile/', views.profile, name='blog-profile'),
    path('login/', Login.as_view(template_name='mysite/login.html', redirect_authenticated_user=True), name='Login'),
    path('logout/', Logout.as_view(template_name='mysite/logout.html'), name='Logout'),
    path('like/', views.likes, name='likes'),
    path('password-set-new/', views.newpasswordset, name='password_new_set'),
    path('change-password/', views.passchange, name='password_change'),

]
