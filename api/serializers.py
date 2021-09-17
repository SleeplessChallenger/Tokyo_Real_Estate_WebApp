from django.contrib.auth.models import User
from rest_framework import serializers
from users.models import Profile
from general.models import PropertyClass


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Profile
		fields = ['pk', 'first_name', 'last_name',
			'country', 'can_add_posts']


class PropertySerializer(serializers.ModelSerializer):
	class Meta:
		model = PropertyClass
		fields = ['id', 'title', 'author', 'price', 'age', 'municipality_code',
			'city_planning', 'use', 'structure', 'nearest_station',
			'district', 'municipality', 'property_type', 'floor_ratio',
			'coverage_ratio', 'building_year', 'time_to_station']


class UserSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)

	def create(self, validated_data):
		user = User.objects.create_user(
			username=validated_data['username'],
			password=validated_data['password']
		)

		return user

	class Meta:
		model = User
		fields = ['pk', 'username', 'email', 'password']
