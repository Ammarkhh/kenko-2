from django.contrib import admin

from nutrition.models import Meal, Ingredient, Macro


# class MacroAdmin(admin.ModelAdmin):
#     pass
#
#
# admin.site.register(Macro, MacroAdmin)


class IngredientMacrosInLine(admin.TabularInline):
    model = Macro


class IngredientAdmin(admin.ModelAdmin):
    inlines = [IngredientMacrosInLine]


admin.site.register(Ingredient, IngredientAdmin)


class MealIngredientsInLine(admin.TabularInline):
    model = Meal.ingredients.through


class MealAdmin(admin.ModelAdmin):
    inlines = [MealIngredientsInLine]


admin.site.register(Meal, MealAdmin)
