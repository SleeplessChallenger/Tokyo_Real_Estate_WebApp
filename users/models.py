from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	id = models.IntegerField(primary_key=True)
	country = models.CharField(max_length=40)
	image = models.ImageField(default='avatar.jpg', upload_to='user_photo')
	first_name = models.CharField(max_length=30, default='アノニマス')
	last_name = models.CharField(max_length=30, default='アノニマス')
	can_add_posts = models.BooleanField(default=False)


	def __str__(self):
		return self.user.username

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		image = Image.open(self.image.path)
		if image.height > 400 or image.width > 400:
			desired_size = (400, 400)
			image.thumbnail(desired_size)
			image.save(self.image.path)
