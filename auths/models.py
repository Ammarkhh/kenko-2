from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from trainer.models import Survey


class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"

    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        default=Gender.MALE,
    )

    @property
    def age(self):
        today = timezone.now().date()
        birthdate = self.birth_date
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age

    @property
    def bmi(self):
        latest_survey = Survey.objects.filter(user=self.id).order_by("-id").first()
        if not latest_survey:
            return None

        height = latest_survey.height
        weight = latest_survey.weight
        bmi = weight / (height * height) * 10000
        return format(bmi, ".1f")

    @property
    def height(self):
        latest_survey = Survey.objects.filter(user=self.id).order_by("-id").first()
        if not latest_survey:
            return None
        return latest_survey.height

    @property
    def weight(self):
        latest_survey = Survey.objects.filter(user=self.id).order_by("-id").first()
        if not latest_survey:
            return None
        return latest_survey.weight

    @property
    def goal(self):
        latest_survey = Survey.objects.filter(user=self.id).order_by("-id").first()
        if not latest_survey:
            return None
        return latest_survey.goal