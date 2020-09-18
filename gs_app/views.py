from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.core.exceptions import SuspiciousOperation
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
import uuid
import json
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
import threading


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = json.loads(request.body)['email']
        password = json.loads(request.body)['password']
        user = User.objects.get(email=email)
        if user is None:
            raise SuspiciousOperation

        user = authenticate(username=user.username, password=password)
        if not user:
            raise SuspiciousOperation
        login(request, user)
        token, dummy = Token.objects.get_or_create(user=user)
        return Response({'username': user.username, 'email': user.email, 'token': token.key, 'pk': user.pk, 'is_active': user.is_active})


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = json.loads(request.body)['email']
        user = User()
        user.email = email
        user.username = uuid.uuid4()
        user.first_name = json.loads(request.body)['firstName']
        user.last_name = json.loads(request.body)['lastName']
        user.save()
        return Response({'registered': True})
