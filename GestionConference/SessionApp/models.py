from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
# Create your models here.

room_validator = RegexValidator(r'^[A-Za-z0-9\s]+$', 'Room may contain only letters, numbers and spaces')
class Session(models.Model):
    session_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    topic=models.CharField(max_length=255)
    session_day=models.DateField()
    start_time=models.DateTimeField()
    end_time=models.DateTimeField()
    
   # room=models.CharField(max_length=100,validators=[room_validator])
    def clean(self):
        # Vérifier que la date de la session appartient à la période de la conférence
        if self.conference and (self.session_day < self.conference.start_date or self.session_day > self.conference.end_date):
            raise ValidationError("La date de la session doit être comprise entre les dates de la conférence.")
        
        # Vérifier que l’heure de fin est après l’heure de début
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError("L’heure de fin doit être supérieure à l’heure de début.")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    conference=models.ForeignKey('ConferenceApp.Conference',on_delete=models.CASCADE,
                                 related_name='sessions')
    