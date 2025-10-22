from django.contrib import admin
from .models import Session

#admin.site.register(Session)
@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'conference','description' , 'start_time', 'end_time')
    list_filter = ('conference', 'session_day')

    date_hierarchy = "session_day"
    search_fields = ("title", "description", "topic")
    fieldsets = (
        ("Infos générales", {
            "fields": ("title", "description", "topic", "conference")
        }),
        ("Planification", {
            "fields": ("session_day", "start_time", "end_time"),
            "description": "La date doit être comprise dans la période de la conférence ; lheure de fin doit être après lheure de début."
        }),
        ("Métadonnées", {
            
            "fields": ("created_at", "updated_at"),
        }),
    )
# Register your models here.


# Register your models here.
