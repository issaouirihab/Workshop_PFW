from django.urls import path
from .views import *
#from .import views
urlpatterns = [
    #path("liste/",view=views.all_conferences,name="list_conferences"),
    path("liste/",conferencelist.as_view(),name="list_conferences"),
    path("details/<int:pk>/",conferenceDetails.as_view(),name="details_conference"),
    

    
]
