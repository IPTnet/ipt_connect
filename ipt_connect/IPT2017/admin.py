# coding: utf8
from django.contrib import admin
from django.contrib.auth.models import User
from models import *
from django import forms
from django.forms import widgets


class JuryGradeInline(admin.TabularInline):
	model = JuryGrade
	extra = 0


class TacticalRejectionInline(admin.TabularInline):
	model = TacticalRejection
	extra = 0


class EternalRejectionInline(admin.TabularInline):
	model = EternalRejection
	extra = 0


class Roundadmin(admin.ModelAdmin):

	list_display = ('pf_number', 'round_number', 'room')
	list_filter = ('pf_number', 'round_number', 'room')
	fieldsets = [
	('General Information', {'fields': [
	 ('pf_number', "round_number", "room"), ("reporter_team", "opponent_team", "reviewer_team")]}),
	(None, {'fields': [("reporter"), ('opponent'),
	 ('reviewer'), 'problem_presented']})
	]
	inlines = [TacticalRejectionInline, EternalRejectionInline, JuryGradeInline]

	# Saving the round triggers the computation of the scores, so we need to save the
	# JuryGrade's first in order to use up-to-date grades. The soution used here is to
	# use the save_related function, which will first save the inline models, and then
	# call round.save() in there
	def save_model(self, request, obj, form, change):
		pass  # don't actually save the parent instance

	def save_related(self, request, form, formsets, change):
		# first save the inlines
		for formset in formsets:
			self.save_formset(request, form, formset, change=change)
		# the save the round once, triggerring the update_scores methods
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
		js = ('admin/js/jquery.js','admin/js/participant_fill.js',)
	# TODO: Display the full name+surname of the reporter, opponent and reviewer in the admin view


class TeamAdmin(admin.ModelAdmin):

	list_display = ('name','IOC','surname')
	search_fields = ('name','IOC')


class ParticipantAdmin(admin.ModelAdmin):

	list_display = ('surname','name','team','affiliation','email','phone_number','role','gender','birthdate','veteran','diet','shirt_size','mixed_gender_accommodation','remark')
	search_fields = ('surname','name')
	list_filter = ('team','gender','role','veteran','diet','shirt_size','mixed_gender_accommodation')

	def save_model(self, request, obj, form, change):
		if not(request.user.is_superuser):
			u = User.objects.get(username = request.user.username)
			obj.team = u.Team_IPT2017
			obj.save()
		obj.save()

	def get_queryset(self,request):
		qs = super(ParticipantAdmin,self).get_queryset(request)
		u = User.objects.get(username = request.user.username)
		if request.user.is_superuser:
			return qs
		return qs.filter(team = u.Team_IPT2017)

class JuryAdmin(admin.ModelAdmin):

	list_display = ('name','surname','team','affiliation','pf1','pf2','pf3','pf4','final','remark',)
	list_filter = ('team','pf1','pf2','pf3','pf4','final',)
	search_fields = ('name','surname','affiliation',)

# Register your models here.
admin.site.register(Team,TeamAdmin)
admin.site.register(Participant,ParticipantAdmin)
admin.site.register(Round, Roundadmin)
admin.site.register(Problem)
admin.site.register(Room)
admin.site.register(Jury,JuryAdmin)
