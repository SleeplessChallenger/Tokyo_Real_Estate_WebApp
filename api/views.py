from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import (viewsets, permissions,
	generics, mixins, viewsets,
	status)
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import (UserSerializer, ProfileSerializer,
	PropertySerializer)
from users.models import Profile
from general.models import PropertyClass


class ProfileViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
	'''
	Use generics.ListAPIView to prevent user from
	making POST.
	Actually it caused error, that's why I changed
	a way of implementation
	'''
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer
	permission_classes = [permissions.IsAuthenticated]


# curl -X DELETE -u "Daniil":"Enoshima" "http://127.0.0.1:8000/api/properties/88"
# curl -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://127.0.0.1:8000/api/users/
# curl --header "Content-Type: application/json" --request POST --data '{"username":"Itachi", "password":"Naruto"}' http://127.0.0.1:8000/api/users/
# curl --header "Content-Type: application/json" --request PATCH --data '{"username":"Itachi", "password":"Sasuke"}' http://127.0.0.1:8000/api/users/10
class UserView(APIView):
	'''
class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = [permissions.IsAuthenticated]

We can use ViewSet, but for the sake of example
I'll stick with APIView

	'''
	serializer_class = UserSerializer
	permission_classes = [
		permissions.AllowAny
	]

	def get(self, request, pk = None, format=None):
		if not pk:
			users = User.objects.all()
			serializer = self.serializer_class(users, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)

		else:
			user = User.objects.filter(pk=pk).first()
			if not user:
				return Response({'message': 'No user'}, status=status.HTTP_204_NO_CONTENT)

			serializer = self.serializer_class(user)
			return Response(serializer.data, status=status.HTTP_200_OK)

	def post(self, request, format=None):
		serializer = self.serializer_class(data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		else:
			# if username already exists
			return Response(serializer.errors, status=status.HTTP_409_CONFLICT)


	def patch(self, request, format=None):
		pk = request.data.get('pk') or request.data.get('id')
		if not pk:
			return Response({'message': "Cannot make patch without id"},
				status=status.HTTP_406_NOT_ACCEPTABLE)

		user = User.objects.filter(pk=pk).first()
		if not user:
			return Response({'message': "Doesn't have user with such id"},
				status=status.HTTP_204_NO_CONTENT)

		serializer = self.serializer_class(user, data=request.data,
			partial=True)

		if serializer.is_valid():
			serializer.save()
			return Response({'message': f"{user.username} was updated"},
				status=status.HTTP_200_OK)

		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk=None, format=None):
		if not pk:
			return Response({'message': "Can't delete without pk"},
				status=status.HTTP_400_BAD_REQUEST)

		user = User.objects.filter(pk=pk).first()
		if not user:
			return Response({'message': f"{pk} isn't in db"},
				status=status.HTTP_400_BAD_REQUEST)

		else:
			user.delete()
			return Response({'message': f"{user.username} was erased"},
				status=status.HTTP_200_OK)


class PropertyView(APIView):
	'''
class PropertyViewSet(viewsets.ModelViewSet):
	queryset = PropertyClass.objects.all().order_by('-date_created')
	serializer_class = PropertySerializer
	permission_classes = [permissions.IsAuthenticated]

	'''
	serializer_class = PropertySerializer

	def get(self, request, pk=None):
		if pk is None:
			properties = PropertyClass.objects.all().order_by('-building_year')
			serializer = self.serializer_class(properties, many=True)
			return Response(serializer.data,
				status=status.HTTP_200_OK)
		else:
			property_one = PropertyClass.objects.filter(pk=pk).first()
			if not property_one:
				return Response({'message': 'No property with such id'},
					status=status.HTTP_400_BAD_REQUEST)

			serializer = self.serializer_class(property_one)
			return Response(serializer.data,
				status=status.HTTP_200_OK)

	def post(self, request, format=None):
		'''
		1. if user isn't authorized: error
		2. if author != current user AND 
			user isn't super or user isn't super:
			error
		'''
		if not request.user.is_authenticated:
			return Response({'message': 'Only author/admin can add posts'},
				status=status.HTTP_400_BAD_REQUEST)

		user = self._get_author_name(request)

		first_check = user.username != request.user.username and\
			not request.user.is_superuser
		second_check = not request.user.is_superuser

		if first_check or second_check:
			return Response(
				{'message': "You can't specify others as authors unless you're admin"},
				status=status.HTTP_409_CONFLICT)

		serializer = self.serializer_class(data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data,
				status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	def patch(self, request, format=None):
		'''
		in this function we're to use
		another helper as here we must
		specify pk/id in PATCH form of
		post, not author

		1. Invalid post id: error
		2. if user isn't authenticated or
			user isn't author of post AND
			user isn't superuser: error

		3. if everything is OK: save partial
			input and return message
		'''
		user = self._get_author_name_2(request)
		# if id/pk isn't provided: error will be triggered
		if not user:
			return Response({'message': "Wrong id"},
				status=status.HTTP_400_BAD_REQUEST)

		first_check = not request.user.is_authenticated
		second_check = user.username != request.user.username and\
			not request.user.is_superuser

		if first_check or second_check:
			return Response(
				{'message': "You are unable to tweak others' post unless you're admin"},
				status=status.HTTP_400_BAD_REQUEST)

		post_pk = request.data.get('id') or request.data.get('pk')
		post = PropertyClass.objects.filter(pk=post_pk).first()

		serializer = self.serializer_class(post, data=request.data, partial=True)

		if serializer.is_valid():
			serializer.save()
			return Response({"message": f"{post.title} was updated!"},
				status=status.HTTP_202_ACCEPTED)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	# if you want to delete via curl: use -u
	def delete(self, request, format=None, pk=None):
		'''
		1. if invalid id: error
		2. if user isn't authenticated or
			user isn't author of post AND
			user isn't superuser: error

		'''
		post = PropertyClass.objects.filter(id=pk).first()

		if not post:
			return Response({'message': "No post with such id"},
				status=status.HTTP_400_BAD_REQUEST)

		first_check = not request.user.is_authenticated
		second_check = post.author != request.user.username and\
			not request.user.is_superuser

		if first_check or second_check:
			return Response(
				{'message': "You are unable to tweak others' post unless you're admin"},
				status=status.HTTP_400_BAD_REQUEST)

		else:
			post.delete()
			return Response({'message': f"{post.title} was deleted"},
				status=status.HTTP_200_OK)

	def _get_author_name(self, request):
		author_id = request.data.get('author')
		user = User.objects.filter(pk=author_id).first()
		return user

	def _get_author_name_2(self, request):
		post_id = request.data.get('id') or\
			request.data.get('pk')
		post = PropertyClass.objects.filter(pk=post_id).first()
		if not post:
			return False
		return post.author
