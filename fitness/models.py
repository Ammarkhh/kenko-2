from django.db import models


class Exercise(models.Model):
    title = models.CharField(max_length=64)

    image = models.ImageField(null=True, blank=True)
    video = models.CharField(blank=True, null=True, max_length=300)

    instructions = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class Workout(models.Model):
    exercise = models.ForeignKey("fitness.Exercise", on_delete=models.CASCADE)

    sets = models.IntegerField()
    reps = models.IntegerField()

    day = models.ForeignKey("fitness.Day", on_delete=models.CASCADE)

    def __str__(self):
        return "%s Day %s %s %sx%s" % (self.day.program.title, self.day.rank, self.exercise.title, self.sets, self.reps)


class Day(models.Model):
    rank = models.IntegerField(null=True, blank=True)

    image = models.ImageField(null=True, blank=True)

    program = models.ForeignKey("fitness.Program", on_delete=models.CASCADE)

    def __str__(self):
        return self.program.title + " Day " + self.rank.__str__()


class Program(models.Model):
    class ProgramType(models.TextChoices):
        HOME = "HOME", "Home"
        PPL = "PPL", "Push-Pull-Leg"
        BSPLT = "BSPLT", "Bro-Split"

    title = models.CharField(max_length=64)
    image = models.ImageField(null=True, blank=True)

    type = models.CharField(
        max_length=5,
        choices=ProgramType.choices,
        default=ProgramType.HOME,
    )

    def __str__(self):
        return self.title
