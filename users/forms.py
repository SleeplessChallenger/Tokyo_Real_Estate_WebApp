from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegistration(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


class GiveRights(forms.ModelForm):
	can_add_posts = forms.ChoiceField(
		widget=forms.RadioSelect,
		choices=[(True, 'Give right'), (False, 'Remove right')],
		required=True
	)

	class Meta:
		model = Profile
		fields = ['can_add_posts']


class UserChange(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email']


class ProfileChange(forms.ModelForm):

	class Meta:
		model = Profile
		fields = ['first_name', 'last_name', 'country', 'image']


class UserDelete(forms.ModelForm):
	class Meta:
		model = User
		fields = []
