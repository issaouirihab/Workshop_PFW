from django import forms
from .models import Conference, Submission

class ConferenceModel(forms.ModelForm):
    class Meta:
        model=Conference
        fields=['name','theme','description','location','start_date','end_date']
        labels={
            'name':'Nom de la conference',
            'theme':'Theme de la conference',
            'description':'Description de la conference',
            'location':'Lieu de la conference',
            'start_date':'Date de debut',
            'end_date':'Date de fin',
            }
        widgets ={
            'name':forms.TextInput(attrs={'placeholder':'nom de la conference'}),
            'start_date':forms.DateInput(attrs={'type':'date','placeholder':'date de debut'}),
            'end_date':forms.DateInput(attrs={'type':'date','placeholder':'date de fin'}),
            }
class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ["title", "abstract", "keywords", "paper"]
        labels = {
            "title": "Titre",
            "abstract": "Résumé",
            "keywords": "Mots-clés",
            "paper": "Fichier PDF",
        }
        widgets = {
            "abstract": forms.Textarea(attrs={"rows": 4}),
        }