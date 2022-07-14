# coding: utf8
from django.contrib import admin
from solo.admin import SingletonModelAdmin

from model_SupplementaryMaterial import *
from models import *

# from config.models import SiteConfiguration

admin.site.register(SiteConfiguration, SingletonModelAdmin)

# There is only one item in the table, you can get it this way:
from .models import SiteConfiguration

# config = SiteConfiguration.objects.get()

try:
    # get_solo will create the item if it does not already exist
    config = SiteConfiguration.get_solo()
except:
    pass


class SupplementaryMaterialInline(admin.TabularInline):
    model = SupplementaryMaterial
    extra = 0


class JuryGradeInline(admin.TabularInline):
    model = JuryGrade
    extra = 0


class TacticalRejectionInline(admin.TabularInline):
    model = TacticalRejection
    extra = 0


class EternalRejectionInline(admin.TabularInline):
    model = EternalRejection
    extra = 0


class AprioriRejectionInline(admin.TabularInline):
    model = AprioriRejection
    extra = 0


class Roundadmin(admin.ModelAdmin):
    list_display = ('pf_number', 'round_number', 'room')
    list_filter = ('pf_number', 'round_number', 'room')
    fieldsets = [
        (
            'General Information',
            {
                'fields': [
                    ('pf_number', "round_number", "room"),
                    ("reporter_team", "opponent_team", "reviewer_team"),
                ]
            },
        ),
        (
            None,
            {
                'fields': [
                    ("reporter"),
                    ("reporter_2"),
                    ('opponent'),
                    ('reviewer'),
                    # ('problem_presented'),
                    # TODO: do the same in python-ish way
                    ('problem_presented', "bonus_points_reporter")
                    if params.manual_bonus_points
                    else ('problem_presented'),
                ]
            },
        ),
    ]

    # Jury grades. We always have them!
    inlines = [JuryGradeInline]

    # Round-based rejections (if supported)
    if params.enable_eternal_rejections:
        inlines = [EternalRejectionInline] + inlines

    if params.enable_tactical_rejections:
        inlines = [TacticalRejectionInline] + inlines

    # Saving the round triggers the computation of the scores, so we need to save the
    # JuryGrade's first in order to use up-to-date grades. The solution used here is to
    # use the save_related function, which will first save the inline models, and then
    # call round.save() in there
    def save_model(self, request, obj, form, change):
        pass  # don't actually save the parent instance

    def save_related(self, request, form, formsets, change):
        # First save iteration to prevent errors
        form.instance.save()
        # first save the inlines
        for formset in formsets:
            self.save_formset(request, form, formset, change=change)
        # then save the round once, triggerring the update_scores methods
        form.instance.save()

    # def save_formset(self, request, form, formset, change):
    # 	# print self
    # 	# print request
    # 	# print form
    # 	# print formset
    # 	# print change
    # 	formset.save() # this will save the children (the JuryGrade)
    # 	form.instance.save() # form.instance is the parent (ie the Round)

    class Media:
        js = (
            params.instance_name + '/js/admin/js/jquery.js',
            params.instance_name + '/js/admin/js/participant_fill.js',
        )

    # TODO: Display the full name+surname of the reporter, opponent and reviewer in the admin view


class TeamAdmin(admin.ModelAdmin):
    if params.manual_bonus_points:
        list_display = ("name", "surname", "IOC", "bonus_points")
    else:
        list_display = ("name", "surname", "IOC")
    search_fields = ("name", "IOC")

    inlines = []
    if params.enable_apriori_rejections:
        inlines = [AprioriRejectionInline]

    inlines += [SupplementaryMaterialInline]


class ParticipantAdmin(admin.ModelAdmin):
    list_display = (
        "surname",
        "name",
        "team",
        "affiliation",
        "email",
        "phone_number",
        "role",
        "gender",
        "birthdate",
        "veteran",
        "diet",
        "shirt_size",
        "mixed_gender_accommodation",
        "remark",
    )
    search_fields = ("surname", "name")
    list_filter = (
        "team",
        "gender",
        "role",
        "veteran",
        "diet",
        "shirt_size",
        "mixed_gender_accommodation",
    )

    def save_model(self, request, obj, form, change):
        if not (request.user.is_superuser) and not (
            request.user.username == "magnusson"
        ):
            u = User.objects.get(username=request.user.username)
            obj.team = getattr(u, "Team_" + params.instance_name)
            obj.save()
        obj.save()

    def get_queryset(self, request):
        qs = super(ParticipantAdmin, self).get_queryset(request)
        u = User.objects.get(username=request.user.username)
        if request.user.is_superuser or request.user.username == "magnusson":
            return qs
        return qs.filter(team=getattr(u, "Team_" + params.instance_name))


class JuryAdmin(admin.ModelAdmin):
    # TODO: unhardcode PF quantity!!...
    list_display = (
        "surname",
        "name",
        "team",
        "affiliation",
        "pf1",
        "pf2",
        "pf3",
        "pf4",
        "final",
        "email",
        "remark",
    )
    list_filter = (
        "team",
        "pf1",
        "pf2",
        "pf3",
        "pf4",
        "final",
    )
    search_fields = (
        "surname",
        "name",
        "affiliation",
    )


# Register your models here.
admin.site.register(Team, TeamAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Round, Roundadmin)
admin.site.register(Problem)
admin.site.register(Room)
admin.site.register(Jury, JuryAdmin)
