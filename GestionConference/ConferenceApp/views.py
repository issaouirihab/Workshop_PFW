from django.shortcuts import render, get_object_or_404
from .models import Conference, Submission
from django.views.generic import ListView,DetailView,CreateView,UpdateView
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from .forms import ConferenceModel ,SubmissionForm
from django.contrib.auth.mixins import LoginRequiredMixin #to restrict access to authenticated users
from django.urls import reverse
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


#Submission Views
class SubmissionListView(LoginRequiredMixin, ListView):
    model = Submission
    template_name = "conference/submission_list.html"
    context_object_name = "submissions"

    def get_queryset(self):
        # on récupère l'id de la conf dans l'URL
        conference_id = self.kwargs.get("conference_id")
        conf = get_object_or_404(Conference, pk=conference_id)
        # soumissions de CET utilisateur pour CETTE conf
        return Submission.objects.filter(
            Conference=conf,
            user_id=self.request.user
        ).order_by('-submission_date')
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["conference"] = get_object_or_404(Conference, pk=self.kwargs.get("conference_id"))
        return ctx


class SubmissionDetailView(LoginRequiredMixin, DetailView):
    model = Submission
    template_name = "conference/submission_detail.html"
    context_object_name = "submission"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user_id != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("Vous ne pouvez pas voir cette soumission.")
        return obj

class SubmissionCreateView(LoginRequiredMixin, CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name = "conference/submission_form.html"

    def form_valid(self, form):
        conference = get_object_or_404(Conference, pk=self.kwargs.get("conference_id"))
        form.instance.user_id = self.request.user
        form.instance.Conference = conference
        # status par défaut = submitted (déjà dans le modèle)
        response = super().form_valid(form)
        return response
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["conference"] = get_object_or_404(Conference, pk=self.kwargs.get("conference_id"))
        return ctx
    def get_success_url(self):
        return reverse("submission_list", args=[self.kwargs.get("conference_id")])
    
class SubmissionUpdateView(LoginRequiredMixin, UpdateView):
    model = Submission
    form_class = SubmissionForm   # même form mais on va réactiver certains champs
    template_name = "conference/submission_form.html"

    # on veut que certains champs ne soient pas modifiables → on peut le faire dans get_form
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # ces champs NE doivent PAS être modifiés
        if "Conference" in form.fields:
            form.fields["Conference"].disabled = True
        return form

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # sécurité propriétaire
        if obj.user_id != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("Vous ne pouvez pas modifier cette soumission.")
        # blocage selon statut
        if obj.status in ("accepted", "rejected"):
            raise PermissionDenied("Une soumission acceptée ou rejetée ne peut pas être modifiée.")
        return obj

    def get_success_url(self):
        # revenir à la liste de la conférence liée
        return reverse("submission_list", args=[self.object.Conference.pk])





# Create your views here.
