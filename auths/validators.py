import jwt
from rest_framework.exceptions import AuthenticationFailed

from auths.models import User


def validate_token(request):
    auth_header = request.META.get("HTTP_AUTHORIZATION", None)

    if not auth_header:
        raise AuthenticationFailed("No AUTHORIZATION Header")

    try:
        auth_token = auth_header.split(" ")[1]
    except Exception:
        raise AuthenticationFailed("Invalid HTTP_AUTHORIZATION header")

    if not auth_token:
        raise AuthenticationFailed("Can not authenticate without a token.")

    try:
        payload = jwt.decode(auth_token, "secret", algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Can not authenticate with an expired token.")

    try:
        user = User.objects.get(pk=payload.get("id"))
    except User.DoesNotExist:
        raise AuthenticationFailed("Can not authenticate with a token that has an invalid user id.")

    return user
