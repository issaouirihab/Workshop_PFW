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
    template_name = "conference/submission_list.html"   # tu peux mettre "submission/submission_list.html" si tu veux
    context_object_name = "submissions"

    def get_queryset(self):
        # /conferences/3/submissions/
        conference = get_object_or_404(Conference, pk=self.kwargs["conference_id"])
        return (
            Submission.objects
            .filter(Conference=conference)
            .select_related("user_id", "Conference")
            .order_by('-submission_date')
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["conference"] = get_object_or_404(Conference, pk=self.kwargs["conference_id"])
        return ctx


# 9. Détail d’une soumission
class SubmissionDetailView(LoginRequiredMixin, DetailView):
    model = Submission
    template_name = "conference/submission_detail.html"
    context_object_name = "submission"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # l’auteur peut voir, le staff peut voir
        if obj.user_id != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("Vous ne pouvez pas voir cette soumission.")
        return obj


# 10. Ajout d’une soumission pour UNE conférence
class SubmissionCreateView(LoginRequiredMixin, CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name = "conference/submission_form.html"

    def form_valid(self, form):
        # on force la conférence depuis l’URL
        conference = get_object_or_404(Conference, pk=self.kwargs.get("conference_id"))
        form.instance.user_id = self.request.user
        form.instance.Conference = conference
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["conference"] = get_object_or_404(Conference, pk=self.kwargs.get("conference_id"))
        return ctx

    def get_success_url(self):
        # retour vers la liste des soumissions de cette conférence
        return reverse("submission_list", args=[self.kwargs.get("conference_id")])


# 11. Modification d’une soumission
class SubmissionUpdateView(LoginRequiredMixin, UpdateView):
    model = Submission
    form_class = SubmissionForm
    template_name = "conference/submission_form.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # l’auteur ou staff
        if obj.user_id != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("Vous ne pouvez pas modifier cette soumission.")
        # statut non modifiable
        if obj.status in ("accepted", "rejected"):
            raise PermissionDenied("Une soumission acceptée ou rejetée ne peut pas être modifiée.")
        return obj

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # on empêche de changer la conférence
        if "Conference" in form.fields:
            form.fields["Conference"].disabled = True
        # si tu veux empêcher de modifier le status dans le form :
        if "status" in form.fields:
            form.fields["status"].disabled = True
        return form
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # ici self.object existe déjà dans l’update
        ctx["conference"] = self.object.Conference
        return ctx


    def get_success_url(self):
        # retour vers la liste de la conférence liée
        return reverse("submission_list", args=[self.object.Conference.pk])