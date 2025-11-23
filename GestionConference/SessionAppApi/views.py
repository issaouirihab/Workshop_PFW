from django.shortcuts import render
from rest_framework import viewsets
from SessionApp.models import Session
from .serializers import SessionSerialize
class SessionViewSet(viewsets.ModelViewSet):
    queryset=Session.objects.all()
    serializer_class=SessionSerialize
# Create your views here.
