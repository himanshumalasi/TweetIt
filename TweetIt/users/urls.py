from django.urls import path
from .views import follow,profile,follower,following,unfollow,info


urlpatterns = [
	path('follow/<int:id>',follow,name='follow-user'),
	path('profile/<int:id>',profile,name='user-profile'),
	path('followers/',follower,name='user-followers'),
	path('following/',following,name='user-following'),
	path('unfollow/<int:id>',unfollow,name='unfollow-user'),
	path('following/<int:id>',info,name='following-user-info')
]