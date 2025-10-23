from django.urls import path
from .views import *
#from .import views
urlpatterns = [
    #path("liste/",view=views.all_conferences,name="list_conferences"),
    path("liste/",conferencelist.as_view(),name="list_conferences"),
    path("details/<int:pk>/",conferenceDetails.as_view(),name="details_conference"),
    path("form/",conferenceCreate.as_view(),name="conference_add"),
    path("<int:pk>/edit/",conferenceUpdate.as_view(),name="conference_edit"),
    path("<int:pk>/delete/",conferenceDelete.as_view(),name="conference_delete"),
    

    
]
