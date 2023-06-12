# PROJECCT-TASK
1.Create a Django API endpoint that listens to POST and PATCH requests for creating and updating user profiles.

solution:-

First, make sure you have Django installed. You can install it using pip:
pip install Django
Next, create a new Django project:
django-admin startproject task
Now, create a new Django app:
python manage.py startapp taskapp
Open the user_profiles/settings.py file and add 'profiles' to the INSTALLED_APPS list.
INSTALLED_APPS = [
    # ...
    '[Appname]',
    # ...
]

Next, open profiles/models.py and define the UserProfile model. For simplicity, let's assume the user profile has only two fields: name and bio.
from django.db import models

# Create your models here.



from django.db import models

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    bio=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    image=models.ImageField(null=False,blank=False)


def _str_(self):
    return self.name
    
 Now, create a migration for the new model:
 python manage.py makemigrations
python manage.py migrate

Next, open profiles/views.py and define the view for the API endpoint.
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from taskapp.models import UserProfile
from taskapp.serializers import UserProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication



@api_view(['GET', 'POST', 'PATCH'])

def user_profile(request, profile_id=None):
    if request.method == 'GET':
        if profile_id:
            profile = get_object_or_404(UserProfile, id=profile_id)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        else:
            profiles = UserProfile.objects.all()
            serializer = UserProfileSerializer(profiles, many=True)
            return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            profile = serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
    elif request.method == 'PATCH':
        profile = get_object_or_404(UserProfile, id=profile_id)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            profile = serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
        




Finally, open user_profiles/urls.py and add the URL pattern for the API endpoint:
from django.urls import path
from profiles import views

urlpatterns = [
    path('profiles/', views.user_profile),
    path('profiles/<int:profile_id>/', views.user_profile),
]
That's it! You've created the Django API endpoint for creating and updating user profiles. You can run the development server using the following command:
python manage.py runserver

2.The endpoint should validate the incoming data, ensuring that required fields are provided and that the email is in a valid format.

Solution:-

To add data validation to the Django API endpoint for creating and updating user profiles, you can use Django's built-in form validation and serializers. Here's an updated version of the code that includes data validation:

 if a user is trying to sign up for a new account on a website, the endpoint should check that they have filled out all the required fields and that their email address is in a valid format. If the information is not valid or complete, the endpoint should send an error message back to the user.
 
 3. If the data is valid, create a new profile or update the existing profile in the database.
 
  Solution:-
  
  This code uses the UserProfileSerializer to validate and serialize the data before saving it in the database. If the data is valid, it creates a new profile for POST requests or updates the existing profile for PATCH requests.

Now, when you send a POST request to http://localhost:8000/profiles/, a new user profile will be created in the database if the data is valid. Similarly, when you send a PATCH request to http://localhost:8000/profiles/<profile_id>/, the existing profile with the given profile ID will be updated in the database if the data is valid.

4.Return appropriate HTTP responses and messages to indicate the success or failure of the operation.

Solution:-

 To provide appropriate HTTP response codes and messages to indicate the success or failure of the operation. For example, if the operation is successful, the endpoint can return a 200 OK response code and a message indicating that the operation was successful. If the operation fails, the endpoint can return a 400 Bad Request response code and a message indicating what went wrong.

5. Implement proper URL routing for the API endpoint.

Solution:-

By defining URL routes in this way, you can ensure that incoming requests are properly routed to the appropriate endpoint handlers. This makes it easier to build a scalable and maintainable API that can handle a wide range of client requests.

6.Implement proper authentication and authorization mechanisms, ensuring that only authenticated users can create or update profiles.

Solution:-

To implement proper authentication and authorization mechanisms in Django to ensure that only authenticated users can create or update profiles, you can utilize Django's authentication and permission classes. Here's how you can update the Django API endpoint to include authentication and authorization:

In user_profiles/settings.py, make sure you have the necessary authentication and permission classes configured. For example, you can add the following lines to the REST_FRAMEWORK settings:
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
Next, in profiles/views.py, import the necessary authentication and permission classes:
Now, update the view functions with the authentication and permission classes:

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_user_profile(request):
    serializer = UserProfileSerializer(data=request.data)
    if serializer.is_valid():
        profile = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user_profile(request, profile_id):
    profile = get_object_or_404(UserProfile, id=profile_id)
    serializer = UserProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        profile = serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

By adding the @authentication_classes([SessionAuthentication, TokenAuthentication]) decorator and the @permission_classes([IsAuthenticated]) decorator to the view functions, you ensure that only authenticated users can access the endpoints for creating and updating user profiles.
Now, when a request is made to create or update a profile, the user needs to include valid authentication credentials, such as a session cookie or a token, in the request headers. Otherwise, the API will respond with a 403 Forbidden status code.
#now run the server
python manage.py runserver

7.Write unit tests to verify the functionality of the API endpoint.

Solution:-

you can write unit tests to verify the functionality of the API endpoint:

In profiles/tests.py, add the following code:
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from profiles.models import UserProfile

class UserProfileAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = UserProfile.objects.create(user=self.user, name='John Doe', email='johndoe@example.com')

    def test_create_user_profile(self):
        url = reverse('profile-list')
        data = {
            'name': 'Jane Smith',
            'email': 'janesmith@example.com',
            'bio': 'I am a test user.'
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserProfile.objects.count(), 2)
        self.assertEqual(UserProfile.objects.last().name, 'Jane Smith')

    def test_update_user_profile(self):
        url = reverse('profile-detail', args=[self.profile.id])
        data = {
            'name': 'John Johnson',
            'email': 'johnjohnson@example.com',
            'bio': 'Updated bio.'
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserProfile.objects.get(id=self.profile.id).name, 'John Johnson')

    def test_create_user_profile_unauthenticated(self):
        url = reverse('profile-list')
        data = {
            'name': 'Jane Smith',
            'email': 'janesmith@example.com',
            'bio': 'I am a test user.'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(UserProfile.objects.count(), 1)

    def test_update_user_profile_unauthenticated(self):
        url = reverse('profile-detail', args=[self.profile.id])
        data = {
            'name': 'John Johnson',
            'email': 'johnjohnson@example.com',
            'bio': 'Updated bio.'
        }

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(UserProfile.objects.get(id=self.profile.id).name, 'John Doe')




