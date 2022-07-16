from rest_framework.response import Response
from rest_framework.views import APIView

from nutrition.models import Meal
from nutrition.serializer import MealSerializer


class MealView(APIView):
    def get(self, request):
        meals = Meal.objects.all()
        serializer = MealSerializer(meals, context={"fields": ["id", "title", "image"]}, many=True)
        return Response({"meals": serializer.data})

    def post(self, request):
        meals = None

        if request.data.get("id", None):
            meals = Meal.objects.filter(pk=request.data.get("id"))

        if request.data.get("title", None):
            meals = Meal.objects.filter(title__icontains=request.data.get("title"))

        return Response(MealSerializer(meals, many=True).data)
