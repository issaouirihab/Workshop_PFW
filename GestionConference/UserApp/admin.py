from django.contrib import admin
from .models import User,OrganizingComitee

#admin.site.register(User)
#admin.site.register(OrganizingComitee)
@admin.action(description="Définir le rôle : Participant")
def make_participant(modeladmin, request, queryset):
    queryset.update(role="Participant")

@admin.action(description="Définir le rôle : Comité d'organisation")
def make_comitee(modeladmin, request, queryset):
    queryset.update(role="comitee")

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # colonnes visibles
    list_display = (
        "user_id", "username", "first_name", "last_name",
        "email", "role", "affiliation", "nationality",
        "is_staff", "is_active", "date_joined",
    )
    list_display_links = ("user_id", "username")
    ordering = ("-date_joined",)
    date_hierarchy = "date_joined"

    # filtres & recherche
    list_filter = ("role", "is_staff", "is_active", "nationality")
    search_fields = ("user_id", "username", "first_name", "last_name", "email", "affiliation", "nationality")

    # édition rapide
    list_editable = ("role",)

    # formulaire (lecture seule pour les champs système)
    readonly_fields = ("user_id", "created_at", "updated_at", "last_login", "date_joined")
    fieldsets = [
        ("Identité", {"fields": ("user_id", "username", "password")}),
        ("Infos personnelles", {"fields": ("first_name", "last_name", "email", "affiliation", "nationality", "role")}),
        ("Statuts", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Dates", {"fields": ("last_login", "date_joined", "created_at", "updated_at")}),
    ]

    actions = [make_participant, make_comitee]


# ===========================
# OrganizingComitee
# ===========================
@admin.register(OrganizingComitee)
class OrganizingComiteeAdmin(admin.ModelAdmin):
    # colonnes visibles
    list_display = ("user", "conference", "comitee_role", "date_joined", "created_at")
    ordering = ("-date_joined",)
    date_hierarchy = "date_joined"

    # filtres & recherche
    list_filter = ("comitee_role", "conference")
    search_fields = ("user__username", "user__first_name", "user__last_name", "user__email", "conference__title")

    # formulaire
    readonly_fields = ("created_at", "updated_at", "date_joined")
    fieldsets = [
        ("Lien", {"fields": ("user", "conference")}),
        ("Rôle", {"fields": ("comitee_role",)}),
        ("Dates", {"fields": ("date_joined", "created_at", "updated_at")}),
    ]
# Register your models here.
