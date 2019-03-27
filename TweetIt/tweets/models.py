from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class  TweetManager(models.Manager):
	def retweet(self,user,parent_obj):
		if parent_obj.parent:
			og_parent = parent_obj.parent
		else:
			og_parent = parent_obj

		# This stops from retweeting ....
		qs = self.get_queryset().filter(
			user=user,parent=og_parent
			).filter(
				date_posted__year=timezone.now().year,
				date_posted__month = timezone.now().month,
				date_posted__day = timezone.now().day
			)
		if qs.exists():
			return None
		# Creating New Tweet with parent equal to tweet
		obj = self.model(
				parent = og_parent,
				user = user,
				content = parent_obj.content,
			)
		obj.save()
		return obj


	def like_toggle(self,user,tweet_obj):
		if user in tweet_obj.likes.all():
			is_liked = False
			tweet_obj.likes.remove(user)
		else:
			is_liked = True
			tweet_obj.likes.add(user)
		return is_liked

class Tweet(models.Model):
	parent = models.ForeignKey("self",blank=True,null=True,on_delete=models.CASCADE)
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	likes = models.ManyToManyField(User,related_name='likes',blank=True)
	content = models.CharField(max_length=140)
	date_posted = models.DateTimeField(auto_now=True)
	objects = TweetManager()
	
	def  __str__(self):
		return str(self.content)

	def no_of_likes(self):
		return self.likes.count()

