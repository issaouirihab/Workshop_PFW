from django.contrib import admin
from .models import Conference,Submission

#modification de l'interface admin
admin.site.site_header="Gestion des conferences Management admin 25/26"
admin.site.site_title="Conference Dashboard"
admin.site.index_title="Conferences Management"
#admin.site.register(Conference)
#admin.site.register(Submission)

#tabulaireInline
#class submissionInline(admin.TabularInline):
class submissionInline(admin.StackedInline):    
    model=Submission
    extra=1
    readonly_fields=('submission_id',)

@admin.register(Conference)
# Register your models here.
class AdminPerso(admin.ModelAdmin):
    list_display=('name','theme','location','start_date','end_date','duration')
    #"filtre "
    ordering = ("start_date",)

 
     #Ajouter des filtres sur theme, location et start_date

    list_filter = ("theme","location","start_date")   

    #champ de recherche :par name, description et location
    search_fields = ("name","description", "location")

    fieldsets=[
        ("Info General",{'fields':('name','description','theme')}),
        (("logistic"),{'fields':('location','start_date','end_date')}),
    ]
   # readonly_fields=("conference_id",)
    def duration(self,obj):
       if obj.start_date and obj.end_date:
          return (obj.end_date-obj.start_date).days
       return "RAS"
    #filtre par date
    date_hierarchy='start_date'
    #personalisationde mot cle duration
    duration.short_description="Duree (en jours)"
    inlines=[submissionInline]
#Personalisation du modèle Submission 
# --------------------------------------------------------------------

@admin.action(description='marquer comme Payee')
def mark_as_payed(modeladmin, request, queryset):
    queryset.update(payd=True)
@admin.action(description='marquer commme acceptee')
def mark_as_accepted(modeladmin, request, queryset):
    queryset.update(status='accepted')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    # a. Colonnes affichées dans la liste d’administration
    list_display = ('title', 'abstract', 'status', 'user_id', 'Conference', 'submission_date', 'payd')
#Ajouter une méthode personnalisée short_abstract qui tronque l’abstract à 50 caractères pour l’affichage rapide.
    def short_abstract(self, obj):
        return (obj.abstract[:50] + '...') if len(obj.abstract) > 50 else obj.abstract
    short_abstract.short_description = 'Abstract'
    #
    list_filter = ('status', 'payd', 'Conference', 'submission_date')
    actions = [mark_as_payed,mark_as_accepted]
    # b. Champs de recherche
    search_fields = ('title', 'keywords', 'user__username')
    list_editable = ('status', 'payd')
    fieldsets = (
        ('Infos générales', {'fields': ('submission_id', 'title', 'abstract', 'keywords')}),
        ('Fichier et conférence', {'fields': ('paper', 'Conference')}),
        ('Suivi', {'fields': ('status', 'payd', 'submission_date', 'user_id')}),
    )

    readonly_fields = ('submission_id', 'submission_date')






# Register your models here.
