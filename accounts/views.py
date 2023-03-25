from django.shortcuts import render
from django.contrib.auth import authenticate
from .serializer import SignUpSerializer, FollowSerializer, Logoutserializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from .tokens import create_jwt_pair_for_user
from . models import User, Follow
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, Token

# Create your views here.


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = []

    def post(self, request: Request):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            response = {
                'message': 'User Succesully Created',
                'data': serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = []

    def post(self, request: Request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user is not None:

            tokens = create_jwt_pair_for_user(user)

            response = {
                'message': 'Loging Successfull',
                'tokens': tokens
            }

            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(data={'Messag': 'Invalid email or password'})

    def get(self, request: Request):
        content = {
            'user': str(request.user),
            'auth': str(request.auth)
        }

        return Response(data=content, status=status.HTTP_200_OK)


class FollowToggle(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, user_id):
        follower = request.user
        follow, created = Follow.objects.get_or_create(
            follower=follower)
        if not created:
            follow.delete()
            return Response({'status': 'unfollowed'}, status=status.HTTP_200_OK)
        serializer = FollowSerializer(follow)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Logoutserializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message': 'Logout successful'})
