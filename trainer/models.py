from django.db import models

from fitness.models import Program, Day, Workout
from nutrition.models import Meal


class ProgrammeManager(models.Manager):
    @staticmethod
    def select_meal(min_cals, max_cals, record_to_delete):
        recommended_meals = [
            meal
            for meal in Meal.objects.all().order_by("?")
            if (meal.calories >= min_cals) and (meal.calories <= max_cals)
        ]

        if not recommended_meals:
            recommended_meals = [Meal.objects.all().order_by("?").first()]

        random_meal = recommended_meals[0]
        return random_meal

    def create_programme(self, date, latest_survey, last_day=None):
        # Date and Survey
        programme = Programme(date=date, based_on_survey=latest_survey)

        # Latest Day
        if not last_day:
            newest_program_based_on_type = (
                Program.objects.filter(type=latest_survey.program_type).order_by("-id").first()
            )
            new_day = Day.objects.filter(program=newest_program_based_on_type).order_by("rank").first()
        else:
            new_day = (
                Day.objects.filter(program=last_day.program).filter(rank__gt=last_day.rank).order_by("rank").first()
            )

        # Day
        programme.based_on_day = new_day
        programme.save()

        # Workouts
        day_workouts = Workout.objects.filter(day=new_day)
        for workout in day_workouts:
            ProgrammeWorkouts(programme=programme, workout=workout).save()

        # Meals
        """ 
        30-35% of daily calories for breakfast
        35-40% of daily calories for lunch
        25-35% of daily calories for dinner
        """

        # Breakfast
        meal = self.select_meal(
            int((programme.based_on_survey.daily_calories / 100) * 25),
            int((programme.based_on_survey.daily_calories / 100) * 35),
            programme,
        )
        ProgrammeMeals(programme=programme, meal=meal).save()

        # Lunch
        meal = self.select_meal(
            int((programme.based_on_survey.daily_calories / 100) * 35),
            int((programme.based_on_survey.daily_calories / 100) * 40),
            programme,
        )
        ProgrammeMeals(programme=programme, meal=meal).save()

        # Dinner
        meal = self.select_meal(
            int((programme.based_on_survey.daily_calories / 100) * 25),
            int((programme.based_on_survey.daily_calories / 100) * 35),
            programme,
        )
        ProgrammeMeals(programme=programme, meal=meal).save()

        programme.save()
        return programme


class Programme(models.Model):
    date = models.DateTimeField(auto_now_add=True)  # DONE

    based_on_survey = models.ForeignKey("trainer.Survey", on_delete=models.CASCADE)  # DONE
    based_on_day = models.ForeignKey("fitness.Day", on_delete=models.CASCADE)  # DONE

    meals = models.ManyToManyField("nutrition.Meal", through="trainer.ProgrammeMeals")
    workouts = models.ManyToManyField("fitness.Workout", through="trainer.ProgrammeWorkouts")  # DONE
    @property
    def rank(self):
        rank=self.based_on_day.rank
        return rank


    objects = ProgrammeManager()


class ProgrammeMeals(models.Model):
    programme = models.ForeignKey("trainer.Programme", on_delete=models.CASCADE)

    meal = models.ForeignKey("nutrition.Meal", on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)


class ProgrammeWorkouts(models.Model):
    programme = models.ForeignKey("trainer.Programme", on_delete=models.CASCADE)

    workout = models.ForeignKey("fitness.Workout", on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)


class Survey(models.Model):
    class ActivityLevel(models.TextChoices):
        SED = "SED", "Sedentary: little or no exercise"
        LIT = "LIT", "Light: exercise 1-3 times/week"
        MOD = "MOD", "Moderate: exercise 4-5 times/week"
        ACT = "ACT", "Active: daily exercise or intense exercise 3-4 times/week"
        VCT = "VCT", "Very Active: intense exercise 6-7 times/week"
        # ECT = "ECT", "Extra Active: very intense exercise daily, or physical job"

    class Goals(models.TextChoices):
        MWL = "MWL", "Mild Weight Loss"
        WL = "WL", "Weight Loss"
        EWL = "EWL", "Extreme Weight Loss"
        MWG = "MWG", "Mild Weight Gain"
        WG = "WG", "Weight Gain"
        EWG = "EWG", "Extreme Weight Gain"

    user = models.ForeignKey("auths.User", on_delete=models.CASCADE)

    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    activity = models.CharField(
        max_length=3,
        choices=ActivityLevel.choices,
        default=ActivityLevel.MOD,
    )

    goal = models.CharField(
        max_length=3,
        choices=Goals.choices,
        default=Goals.WG,
    )

    program_type = models.CharField(
        max_length=5,
        choices=Program.ProgramType.choices,
        default=Program.ProgramType.HOME,
    )

    date = models.DateTimeField(auto_now_add=True)

    @property
    def macros(self):
        daily_calories = self.daily_calories
        carbs_in_grams = (daily_calories / 2) / 4
        proteins_in_grams = ((daily_calories / 100) * 35) / 4
        fats_in_grams = ((daily_calories / 100) * 15) / 4
        macros = {
            "Proteins_in_grams": int(proteins_in_grams),
            "Carbs_in_grams": int(carbs_in_grams),
            "Fats_in_grams": int(fats_in_grams),
        }
        return macros

    @property
    def daily_calories(self):
        age = self.user.age
        gender = self.user.gender
        weight = self.weight
        height = self.height
        daily_calories = 0
        if gender == "M":
            daily_calories = 66.47 + (13.75 * float(weight)) + (5.003 * float(height)) - (6.755 * float(age))
        if gender == "F":
            daily_calories = 655.1 + (9.563 * float(weight)) + (1.850 * float(height)) - (4.676 * float(age))
        activity_level = self.activity
        activity = 0
        goal = self.goal
        goalcal = 0

        if activity_level == "SED":
            activity = 1.2
        elif activity_level == "LIT":
            activity = 1.375
        elif activity_level == "MOD":
            activity = 1.55
        elif activity_level == "ACT":
            activity = 1.725
        elif activity_level == "VCT":
            activity = 1.9

        if goal == "MWL":
            goalcal = -200
        elif goal == "WL":
            goalcal = -300
        elif goal == "EWL":
            goalcal = -400
        elif goal == "MWG":
            goalcal = +200
        elif goal == "WG":
            goalcal = +300
        elif goal == "EWG":
            goalcal = +400

        return int(daily_calories * activity + goalcal)
