from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Profile


class ProfileTestCase(TestCase):
	def setUp(self):
		self.user = User.objects.create(username='シカマル')
		self.user.set_password('Pass1539')
		self.user.save()

	def test_str(self):
		self.assertEquals(str(self.user), self.user.username)

	def test_columns(self):
		self.user.country = 'Japan'
		self.assertEquals(self.user.country, 'Japan')
