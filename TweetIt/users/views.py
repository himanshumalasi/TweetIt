from django.shortcuts import render,redirect
from .forms import UserRegisterForm,ProfileForm
from .models import Follow
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from tweets.models import Tweet
# Create your views here.

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request,'users/register.html',{'form':form})

@login_required
def  follow(request,id):
	user = User.objects.get(id=id)
	if user.id == request.user.id:
		return redirect('/')
	follow = Follow(follow_by=request.user,follow_who=user)
	follow.save()
	return redirect('/')

@login_required
def  unfollow(request,id):
	print(id)
	user = User.objects.get(id=id)
	follow = Follow.objects.get(follow_by=request.user,follow_who=user)
	follow.delete()
	return redirect('user-following')

@login_required
def  profile(request,id):
	form = ProfileForm(instance=request.user.profile)
	if request.method == "POST":
		form = ProfileForm(request.POST,request.FILES,instance=request.user.profile)
		if form.is_valid():
			image = form.cleaned_data['image']
			description = form.cleaned_data['description']
			profile = form.save(commit=False)
			profile.user = request.user
			profile.save()
			return redirect('/')
	context = {
		'form':form
	}
	return render(request,'users/profile.html',context)


@login_required
def follower(request):
	followers = []
	for x in request.user.follow_who.all():
		user = User.objects.get(id=x.follow_by_id).profile
		followers.append(user)
	context = {
		'followers' : followers
	}
	return render(request,'users/follower.html',context)

	
@login_required
def following(request):
	followings = []
	for x in request.user.follow_by.all():
		user = User.objects.get(id=x.follow_who_id).profile
		followings.append(user)
	context = {
		'followings':followings
	}
	return render(request,'users/following.html',context)



def  info(request,id):
	print(id)

	tweets = User.objects.get(id=id).tweet_set.all().order_by('-date_posted')
	print(tweets)
	context = {
		'profile' : User.objects.get(id=id).profile,
		'tweets':tweets,
	}
	return render(request,'users/userdetail.html',context)