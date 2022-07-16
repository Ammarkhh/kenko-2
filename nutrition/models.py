from django.db import models


class Meal(models.Model):
    title = models.CharField(max_length=64)

    image = models.ImageField(null=True, blank=True)
    video = models.CharField(max_length=300, null=True, blank=True)

    instructions = models.TextField(null=True, blank=True)

    ingredients = models.ManyToManyField("nutrition.Ingredient", through="nutrition.MealIngredient")

    def __str__(self):
        return str(self.title)

    def get_ingredients_info(self):
        return MealIngredient.objects.filter(meal=self)

    @property
    def calories(self):
        total_calories = 0
        mealingredients_records = MealIngredient.objects.filter(meal=self)
        for ingredient in mealingredients_records:
            total_calories += ingredient.calories
        return total_calories

    @property
    def macros(self):
        macros = {}
        mealingredients_records = MealIngredient.objects.filter(meal=self)

        for ingredient in mealingredients_records:
            for macro_type, amount in ingredient.macros.items():
                if macros.get(macro_type):
                    macros[macro_type] += amount
                else:
                    macros[macro_type] = amount
        return macros


class MealIngredient(models.Model):
    meal = models.ForeignKey("nutrition.Meal", on_delete=models.CASCADE)

    ingredient = models.ForeignKey("nutrition.Ingredient", on_delete=models.CASCADE)
    weight = models.IntegerField()

    @property
    def calories(self):
        return self.weight * self.ingredient.calories

    @property
    def macros(self):
        macros_of_ingredient_per_gram = Macro.objects.filter(ingredient=self.ingredient)
        if not macros_of_ingredient_per_gram:
            return None

        macros = {}

        for macro in macros_of_ingredient_per_gram:
            macros[macro.macro_type] = macro.weight * self.weight

        return macros


class Ingredient(models.Model):
    title = models.CharField(max_length=64)
    image = models.ImageField(null=True, blank=True)

    calories = models.DecimalField(
        decimal_places=3, max_digits=7, blank=True, help_text="Calories for this ingredient per 1g", default=0
    )

    def __str__(self):
        return self.title

    @property
    def macros(self):
        return Macro.objects.filter(ingredient=self)


class Macro(models.Model):
    class MacroTypes(models.TextChoices):
        FAT = "FAT", "Fats"
        PRO = "PRO", "Proteins"
        CAR = "CAR", "Carbohydrates"

    macro_type = models.CharField(
        max_length=3,
        choices=MacroTypes.choices,
        default=MacroTypes.FAT,
    )
    weight = models.DecimalField(
        decimal_places=3,
        max_digits=7,
        blank=True,
        help_text="How much of this macro is in the ingredient per gram",
        default=0,
    )
    ingredient = models.ForeignKey("nutrition.Ingredient", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("macro_type", "ingredient")
