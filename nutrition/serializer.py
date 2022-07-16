from rest_framework import serializers

from nutrition.models import Meal, MealIngredient, Ingredient, Macro


class MacroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Macro
        fields = ("macro_type", "weight")


class IngredientSerializer(serializers.ModelSerializer):
    # macros = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = ("title", "image")

    # def get_macros(self, obj):
    #     return MacroSerializer(obj.macros, many=True).data


class MealIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = MealIngredient
        fields = ("ingredient", "weight")


class MealSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Meal
        fields = ("id", "title", "image", "video", "instructions", "ingredients", "calories", "macros")

    def get_ingredients(self, obj):
        serializer = MealIngredientSerializer(MealIngredient.objects.filter(meal=obj), many=True)
        return serializer.data

    def get_field_names(self, *args, **kwargs):
        field_names = self.context.get("fields", None)
        if field_names:
            return field_names

        return super(MealSerializer, self).get_field_names(*args, **kwargs)
