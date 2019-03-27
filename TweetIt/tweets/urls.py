from django.urls import path
from .views import tweet,detail,like,delete,retweet
urlpatterns = [
    path('',tweet,name="tweet"),
    path('detail/<int:id>',detail,name='detail-view'),
    path('like/<int:id>',like,name='tweet-like'),
    path('delete/<int:id>',delete,name='tweet-delete'),
    path('retweet/<int:id>',retweet,name='tweet-retweet'),
    
]