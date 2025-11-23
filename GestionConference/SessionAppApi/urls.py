from rest_framework import routers
from .views import SessionViewSet
from django.urls import path, include 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('sessions',SessionViewSet)
urlpatterns = [   
    
    path('', include(router.urls)),

]