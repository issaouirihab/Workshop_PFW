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

    #Submission URLs
     path("details/<int:conference_id>/submissions/",SubmissionListView.as_view(),name="submission_list"),
     path("details/<int:conference_id>/submissions/add/",SubmissionCreateView.as_view(),name="submission_add"),
     path("submissions/<str:pk>/",SubmissionDetailView.as_view(),name="submission_detail"),
     path("submissions/<str:pk>/edit/",SubmissionUpdateView.as_view(),name="submission_edit"),
]