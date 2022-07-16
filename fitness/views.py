from rest_framework.response import Response
from rest_framework.views import APIView

from fitness.models import Workout, Program, Day
from fitness.serializers import WorkoutSerializer, ProgramSerializer, DaySerializer


class WorkoutView(APIView):
    def post(self, request):
        workout = None

        if request.data.get("id", None):
            workout = Workout.objects.get(pk=request.data.get("id"))

        serializer = WorkoutSerializer(workout)
        return Response(serializer.data)


class ProgramView(APIView):
    def get(self, request):
        programs = Program.objects.all()
        programmSerializer = ProgramSerializer(programs, context={"fields": ["id", "title", "image"]}, many=True)
        return Response(programmSerializer.data)

    def post(self, request):
        program = None
        days = None
        if request.data.get("id", None):
            program = Program.objects.get(pk=request.data.get("id"))
            days = Day.objects.filter(program=request.data.get("id")).order_by("rank")

        programmSerializer = ProgramSerializer(program, context={"fields": ["title", "image"]})
        daysSerializer = DaySerializer(days, many=True)

        return Response(
            {
                "program": programmSerializer.data,
                "Days": daysSerializer.data,
            }
        )
