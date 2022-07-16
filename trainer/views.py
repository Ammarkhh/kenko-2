from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from auths.serializers import UserSerializer
from auths.validators import validate_token
from trainer.models import Survey, Programme
from trainer.serializers import SurveySerializer


class SurveyView(APIView):
    def get(self, request):
        today = timezone.now()
        user = validate_token(request)

        survey = (
            Survey.objects.filter(user=user).filter(date__gte=today - timezone.timedelta(days=30)).order_by("id").last()
        )

        if not survey:
            raise ValueError("No Survey was available within the last 30 days.")

        user_programmes = Programme.objects.filter(based_on_survey__user=user)
        latest_programmes_based_on_survey = user_programmes.filter(based_on_survey=survey)

        # check if there is a programme based on this survey
        if not latest_programmes_based_on_survey:
            new_programme = Programme.objects.create_programme(date=today, latest_survey=survey)

        # within 24 hrs
        if latest_programmes_based_on_survey.filter(date__gte=today - timezone.timedelta(days=1)).first():
            return Response({"user": UserSerializer(survey.user).data, "survey": SurveySerializer(survey).data})
        # the latest programme based on survey at anytime
        latest_programme = latest_programmes_based_on_survey.order_by("-id").first()

        # create a new one with rank +1
        Programme.objects.create_programme(date=today, latest_survey=survey, last_day=latest_programme.based_on_day)
        return Response({"user": UserSerializer(survey.user).data, "survey": SurveySerializer(survey).data})

    def post(self, request):
        # create a new checkup record
        user = validate_token(request)
        survey_data = {
            "activity": request.data.get("activity"),
            "goal": request.data.get("goal"),
            "weight": request.data.get("weight"),
            "height": request.data.get("height"),
            "program_type": request.data.get("program_type"),
            "user": user.id,
        }
        serializer = SurveySerializer(data=survey_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
