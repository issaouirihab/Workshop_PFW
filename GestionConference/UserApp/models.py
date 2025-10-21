from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.core.exceptions import ValidationError
#validateur predefini pour les noms
from django.core.validators import RegexValidator
def generate_userid():
    return "USER"+uuid.uuid4().hex[:4].upper()
def verify_email(email):
    domaine=["esprit.tn","sesame.com","tekup.tn","central.tn"]
    if email.split("@")[1] not in domaine:
        raise ValidationError("Email non valide et doit appartenir a un domaine universitaire privee")
name_validator= RegexValidator (
    regex= r'[a-zA-Z\s-]+',
    #regex=r'^[a-zA-Z\s-]+$',
    message="Le nom ne doit contenir que des lettres, des espaces et des tirets"
)
#\s:espace
# Create your models here.
class User(AbstractUser):
    user_id=models.CharField(max_length=8,primary_key=True,unique=True,editable=False)
    first_name=models.CharField(max_length=100,validators=[name_validator])
    last_name=models.CharField(max_length=100,validators=[name_validator])
    email=models.EmailField(unique=True,validators=[verify_email])
    affiliation=models.CharField(max_length=255)
    nationality=models.CharField(max_length=255)
    ROLE=[("Participant","Participant"),("comitee","Organizing comitee member")]
    role=models.CharField(max_length=255,choices=ROLE,default="Participant")
    #sans related name onn peut utiliser ça
    #submissions=models.ManyToManyField("ConferenceApp.Conference",through="submission")
    #organizingComiteeList=models.ManyToManyField("ConferenceApp.Conference",through="OrganizingComitee")
    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
#fonction pour enregistrer l'utilisateur avec un user_id unique
    def save(self,*args,**kwargs):
        if not self.user_id:
            new_id=generate_userid()
            while User.objects.filter(user_id=new_id).exists():
                new_id=generate_userid()
            self.user_id=new_id
        super().save(*args,**kwargs)    

class OrganizingComitee(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="comitees")
    conference=models.ForeignKey("ConferenceApp.Conference",on_delete=models.CASCADE,related_name="comitees")
    ROLES=[("Chair","Chair"),("Co-Chair","Co-Chair"),("Member","Member")]
    comitee_role=models.CharField(max_length=255,choices=ROLES)
    date_joined=models.DateField(auto_now_add=True)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

 