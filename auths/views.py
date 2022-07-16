import jwt
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from auths.models import User
from auths.serializers import UserSerializer
from auths.validators import validate_token


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")

        payload = {
            "id": user.id,
            "exp": timezone.now() + timezone.timedelta(minutes=1440),
            "iat": timezone.now(),
        }

        token = jwt.encode(payload, "secret", algorithm="HS256")

        return Response({"jwt": token})


class UserView(APIView):
    def get(self, request):
        user = validate_token(request)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        return Response({"message": "Logout success"})
