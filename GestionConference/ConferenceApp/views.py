from django.shortcuts import render
from .models import Conference
from django.views.generic import ListView,DetailView

def all_conferences(request):
    conferences=Conference.objects.all()
    return render(request,'conference/list.html',{"liste":conferences })    
class conferencelist(ListView):
    model=Conference
    context_object_name='liste'
    template_name='conference/list.html'
    ordering =["start_date"]
class conferenceDetails(DetailView):
    model=Conference
    context_object_name='conference'
    template_name='conference/details.html'

    








# Create your views here.
