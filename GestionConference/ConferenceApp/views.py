from django.shortcuts import render
from .models import Conference
from django.views.generic import ListView,DetailView,CreateView,UpdateView
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from .forms import ConferenceModel 
from django.contrib.auth.mixins import LoginRequiredMixin #to restrict access to authenticated users
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
class conferenceCreate(LoginRequiredMixin,CreateView):
    model=Conference
    template_name='conference/conference_form.html'
    #fields="__all__" on fait le negliger pour utiliser le forms.py
    form_class=ConferenceModel

    success_url=reverse_lazy("list_conferences")
class conferenceUpdate(LoginRequiredMixin,UpdateView):
    model=Conference
    template_name='conference/conference_form.html'
    #fields="__all__"
    form_class=ConferenceModel
    success_url=reverse_lazy("list_conferences")
class conferenceDelete(LoginRequiredMixin,DeleteView):
    model=Conference
    template_name='conference/conference_confirm_delete.html'
    success_url=reverse_lazy("list_conferences")







# Create your views here.
