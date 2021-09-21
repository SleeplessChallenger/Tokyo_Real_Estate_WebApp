from django.test import TestCase
from users.models import Profile
from django.contrib.auth.models import User
from django.dispatch import Signal
from mock_django.signals import mock_signal_receiver


class SignalTestCase(TestCase):
	def setUp(self):
		pass

	def test_signal(self):
		signal = Signal()
		with mock_signal_receiver(signal) as receiver:
			signal.send(sender=None)
			self.assertEqual(receiver.call_count, 1)

		user = User.objects.create(username='ハシラマ')
		user.set_password('FirstHoakge536')
		user.save()

		with mock_signal_receiver(signal) as receiver:
			signal.send(sender=user)
			profile = user.profile
			self.assertTrue(isinstance(profile, Profile))
