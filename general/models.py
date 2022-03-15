from django.db import models
from django.utils import timezone
from PIL import Image
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime


class PropertyClass(models.Model):
	'''
	fields have the same name as
	dataframe so as to add then
	easily
	'''
	# numerical at first
	time_to_station = models.IntegerField()
	building_year = models.IntegerField()
	coverage_ratio = models.IntegerField()
	floor_ratio = models.IntegerField()

	# categorical
	property_type = models.CharField(max_length=150)
	municipality = models.CharField(max_length=300)
	district = models.CharField(max_length=300)
	nearest_station = models.CharField(max_length=350)
	structure = models.CharField(max_length=100)
	use = models.CharField(max_length=100)
	city_planning = models.CharField(max_length=250)
	municipality_code = models.IntegerField()
	# omit age in form, but use in prediction
	age = models.IntegerField()

	# further info
	price = models.BigIntegerField()
	image = models.ImageField(upload_to='propery_photo', default='default_property.jpg')
	title = models.CharField(max_length=1000)
	date_created = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.title} in {self.district}"

	def get_absolute_url(self):
		'''
		it will return full url which
		we want to be redirected to. And
		the view func in turn will handle
		it. Also, if we need additional info:
		{'pk': self.pk}
		'''
		return reverse('all_info')

	# to escape huge memory usage - resize images
	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		image = Image.open(self.image.path)
		if image.height > 800 or image.width > 800:
			desired_size = (800, 800)
			image.thumbnail(desired_size)
			image.save(self.image.path)
