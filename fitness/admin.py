from django.contrib import admin

from fitness.models import Program, Day, Workout, Exercise


class ExerciseAdmin(admin.ModelAdmin):
    pass


admin.site.register(Exercise, ExerciseAdmin)


class WorkoutAdmin(admin.ModelAdmin):
    pass


admin.site.register(Workout, WorkoutAdmin)


class DayWorkoutInLine(admin.TabularInline):
    model = Workout


class DayAdmin(admin.ModelAdmin):
    inlines = [DayWorkoutInLine]


admin.site.register(Day, DayAdmin)


class ProgramAdmin(admin.ModelAdmin):
    pass


admin.site.register(Program, ProgramAdmin)
