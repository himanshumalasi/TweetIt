from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Tweet
from users.models import Profile,Follow
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def tweet(request):
	if request.method == "POST":
		content = request.POST.get('content')
		t = Tweet(content=content,user=request.user)
		t.save()
		return redirect('/')

	# Getting All Tweet by current user
	tweets = Tweet.objects.filter(user=request.user).order_by('-date_posted')
	following_user_tweet = []
	followings = []
	for x in request.user.follow_by.all():
		user = User.objects.get(id=x.follow_who_id)
		followings.append(user)
	print(followings)
	for user in followings:
		following_user_tweet.append(Tweet.objects.filter(user=user).order_by('-date_posted'))
	# Getting user profile
	user_profile = User.objects.get(id=request.user.id)
	# Getting all the followers that we follow
	followers = Follow.objects.filter(follow_by=request.user)
	followers_id = []
	for i in followers:
		followers_id.append(i.follow_who.id)
	followers_id.append(request.user.id)
	# Getting users that are not already followed by us
	other_users = User.objects.exclude(Q(id__in = followers_id))
	

	context = {
		'tweets':tweets,
		'user_profile': user_profile,
		'follow_users': other_users,
		'following_user_tweet':following_user_tweet
	}
	return render(request,'tweets/tweets.html',context)

@login_required
def detail(request,id):
	tweet = Tweet.objects.filter(pk=id).first()
	is_liked = False
	if tweet.likes.filter(id=request.user.id).exists():
		is_liked = True
	else:
		is_liked = False
	context = {
	'tweet':tweet,
	'is_liked':is_liked,
	}
	return render(request,'tweets/detail.html',context)

@login_required
def like(request,id):
	tweet = Tweet.objects.filter(pk=id).first()
	if tweet.likes.filter(id=request.user.id).exists():
		tweet.likes.remove(request.user)
	else:
		tweet.likes.add(request.user)
	return redirect('tweet')

@login_required
def delete(request,id):
	try:
		Tweet.objects.get(user=request.user,pk=id).delete()
	except:
		pass
	return redirect('tweet')



def  retweet(request,id):
	tweet = Tweet.objects.get(pk=id)
	if request.user.is_authenticated:
		new_tweet = Tweet.objects.retweet(request.user,tweet)
		return redirect('/')
	return redirect('/')





	