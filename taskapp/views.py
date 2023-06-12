
    
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
        

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

@api_view(['POST'])
def create_user_profile(request):
    if request.user.is_authenticated:
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            profile = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['PATCH'])
def update_user_profile(request, profile_id):
    if request.user.is_authenticated:
        profile = get_object_or_404(UserProfile, id=profile_id)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            profile = serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
