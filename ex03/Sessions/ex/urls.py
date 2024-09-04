from django.urls import path
from .views import homepage, user_login, user_logout, register, upvote_tip, downvote_tip, delete_tip

urlpatterns = [
    path('', homepage, name='homepage'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
    path('upvote/<int:tip_id>/', upvote_tip, name='upvote_tip'),
    path('downvote/<int:tip_id>/', downvote_tip, name='downvote_tip'),
    path('delete/<int:tip_id>/', delete_tip, name='delete_tip'),
]





