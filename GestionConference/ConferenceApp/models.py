from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils import timezone
import random
import string


def validate_keywords(value):
    # Supprimer les espaces inutiles et séparer les mots-clés par des virgules
    keywords_list = [kw.strip() for kw in value.split(',') if kw.strip()]
    
    # Vérifier le nombre de mots-clés
    if len(keywords_list) > 10:
        raise ValidationError("Le nombre de mots-clés ne doit pas dépasser 10.")
    
def generate_submission_id():
    random_part = ''.join(random.choices(string.ascii_uppercase, k=8))
    return f"SUB{random_part}"
    
# Create your models here.
class Conference(models.Model):
    Conference_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    description=models.CharField(validators=[MinLengthValidator(30,"la discription doit contenir au moins 30 caracteres")])
    location=models.CharField(max_length=255)
    THEME=[
        ("CS&IA","Computer science & IA"),
        ("CS","Social science"),
        ("SE","science And eng")
    ]
    theme=models.CharField(max_length=255,choices=THEME)
    start_date=models.DateField()
    end_date=models.DateField()
    #on utilise clean pour gerer 2 attribut
    def clean(self):
         if self.start_date>self.end_date:
             raise ValidationError("la date de debut doit etre avant la date de fin")
    def __str__(self):
        return self.name
    def clean(self):
    # Vérifier que la date de début est avant la date de fin
     if self.start_date and self.end_date and self.start_date > self.end_date:
        raise ValidationError("La date de début doit être avant la date de fin de la conférence.")
    

         
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
class Submission(models.Model):
    #submission_id=models.CharField(primary_key=True,max_length=255,unique=True)
    submission_id = models.CharField(
        primary_key=True,
        max_length=11,  # "SUB" + 8 lettres = 11 caractères
        unique=True,
        default=generate_submission_id,  # génère automatiquement un ID
        editable=False  # empêche la modification manuelle dans l’admin
    )
    user_id=models.ForeignKey("UserApp.User",on_delete=models.CASCADE,related_name="submissions")
    Conference=models.ForeignKey(Conference,on_delete=models.CASCADE,related_name="submissions")
    title=models.CharField(max_length=255)
    abstract=models.TextField()
    keywords=models.TextField(validators=[validate_keywords])
   # paper=models.FileField(upload_to='papers/')
    paper = models.FileField(upload_to='sub_paper/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    STATUS=[
        ("submitted","submitted"),
        ("under review","under review"),
        ("accepted","accepted"),
        ("rejected","rejected")
    ]
    status=models.CharField(max_length=255,choices=STATUS,default="submitted")
    payd=models.BooleanField(default=False)
    submission_date=models.DateField(auto_now_add=True)
    #keywords (Submission) : vérifier que la chaîne ne dépasse pas un nombre maximal de mots-clés (par ex. 10). (Utiliser une fonction personnalisée qui compte les mots séparés par virgules).
    def clean(self):
        today = timezone.now().date()

        # 1 Vérifier que la conférence est à venir
        if self.Conference.start_date <= today:
            raise ValidationError("La soumission ne peut être faite que pour des conférences à venir.")

        # 2 Limiter à 3 soumissions max par utilisateur et par jour
        if self.user_id:
            submissions_today = Submission.objects.filter(
                user_id=self.user_id,
                submission_date=today
            ).count()
            
            # Si on édite une soumission existante, il faut exclure la soumission actuelle
            if self.pk:
                submissions_today = Submission.objects.filter(
                    user_id=self.user_id,
                    submission_date=today
                ).exclude(pk=self.pk).count()

            if submissions_today >= 3:
                raise ValidationError("Vous avez déjà effectué 3 soumissions aujourd’hui. Limite quotidienne atteinte.")


    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    

