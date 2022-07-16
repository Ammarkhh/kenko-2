from django.contrib import admin

from trainer.models import Programme, Survey


# Survey
class SurveyAdmin(admin.ModelAdmin):
    pass


admin.site.register(Survey, SurveyAdmin)


# Programme
class ProgrammeMealsInLine(admin.TabularInline):
    model = Programme.meals.through


class ProgrammeWorkoutsInLine(admin.TabularInline):
    model = Programme.workouts.through


class ProgrammeAdmin(admin.ModelAdmin):
    inlines = [
        ProgrammeMealsInLine,
        ProgrammeWorkoutsInLine,
    ]


admin.site.register(Programme, ProgrammeAdmin)
