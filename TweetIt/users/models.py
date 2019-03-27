from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class  Follow(models.Model):
	follow_by = models.ForeignKey(User,related_name='follow_by',on_delete=models.CASCADE)
	follow_who = models.ForeignKey(User,related_name='follow_who',on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.follow_who} is followed by {self.follow_by}"

class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	image = models.ImageField(default="default.jpg",upload_to='profile_pics')
	description = models.CharField(max_length=250)

	def  __str__(self):
		return f"{self.user.username} Profile"