from django.contrib.auth import login

from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_jwt.settings import api_settings

from user.models import Profile
from .serializers import UserProfileSerializer
from .forms import CustomUserCreationForm


class UserProfileView(APIView):
    """
    A class based view for retrieve and create user profile
    """
    permission_classes = (AllowAny, )

    def get(self, _request):
        user_profile = Profile.objects.all()
        serializer = UserProfileSerializer(user_profile, many=True)
        return Response({
            'list': serializer.data
        })

    def post(self, request):
        form = CustomUserCreationForm(request.data)

        if not form.is_valid():
            return Response({
                'success': False,
                'reason': form.errors,
            }, status=HTTP_400_BAD_REQUEST)

        user = form.save()
        # Log in user manually
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        # Creating a new token manually --> https://getblimp.github.io/django-rest-framework-jwt/
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        return  Response({
            'success': True,
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'active': user.is_active,
                'staff': user.is_staff
            }
        })
