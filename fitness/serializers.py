from rest_framework import serializers

from fitness.models import Exercise, Workout, Day, Program


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ("title", "image", "video", "instructions")


class WorkoutSerializer(serializers.ModelSerializer):
    exercise = serializers.SerializerMethodField()

    class Meta:
        model = Workout
        fields = ("id", "exercise", "sets", "reps")

    def get_exercise(self, obj):
        return ExerciseSerializer(Exercise.objects.get(pk=obj.exercise.id)).data


class DaySerializer(serializers.ModelSerializer):
    workouts = serializers.SerializerMethodField()

    class Meta:
        model = Day
        fields = ("id", "rank", "workouts")

    def get_workouts(self, obj):
        qset = Workout.objects.filter(day=obj)
        return [WorkoutSerializer(m).data for m in qset]


class ProgramSerializer(serializers.ModelSerializer):
    days = serializers.SerializerMethodField()

    class Meta:
        model = Program
        fields = ("id", "title", "image", "days")

    def get_days(self, obj):
        qset = Day.objects.filter(program=obj)
        return [DaySerializer(m).data for m in qset]

    def get_field_names(self, *args, **kwargs):
        field_names = self.context.get("fields", None)
        if field_names:
            return field_names

        return super(ProgramSerializer, self).get_field_names(*args, **kwargs)
