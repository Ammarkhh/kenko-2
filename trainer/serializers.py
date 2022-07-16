from rest_framework import serializers

from fitness.serializers import WorkoutSerializer
from nutrition.serializer import MealSerializer
from trainer.models import Survey, Programme, ProgrammeMeals, ProgrammeWorkouts


class ProgrammeMealsSerializer(serializers.ModelSerializer):
    meal = serializers.SerializerMethodField()

    class Meta:
        model = ProgrammeMeals
        fields = ("meal", "is_done")

    def get_meal(self, obj):
        return MealSerializer(obj.meal, context={"fields": ["id", "title", "image", "calories", "macros"]}).data


class ProgrammeWorkoutSerializer(serializers.ModelSerializer):
    workout = WorkoutSerializer()

    class Meta:
        model = ProgrammeWorkouts
        fields = ("workout", "is_done")


class ProgrammeSerializer(serializers.ModelSerializer):
    meals = serializers.SerializerMethodField()
    workouts = serializers.SerializerMethodField()

    class Meta:
        model = Programme
        fields = ("id", "meals", "rank", "based_on_day", "workouts")

    def get_meals(self, obj):
        serializer = ProgrammeMealsSerializer(ProgrammeMeals.objects.filter(programme=obj), many=True)
        return serializer.data

    def get_workouts(self, obj):
        serializer = ProgrammeWorkoutSerializer(ProgrammeWorkouts.objects.filter(programme=obj), many=True)
        return serializer.data


class SurveySerializer(serializers.ModelSerializer):
    programme = serializers.SerializerMethodField()

    class Meta:
        model = Survey
        fields = ("daily_calories", "macros", "program_type", "programme", "weight", "height", "user", "goal", "activity")

    def get_programme(self, obj):
        qset = Programme.objects.filter(based_on_survey_id=obj).order_by("-id").first()
        return ProgrammeSerializer(qset).data
