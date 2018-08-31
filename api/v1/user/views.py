from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from user.models import Profile
from .serializers import UserProfileSerializer


class UserProfileView(APIView):
    """
    A class based view for retrieve and create user profile
    """
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, _request):
        user_profile = Profile.objects.all()
        serializer = UserProfileSerializer(user_profile, many=True)
        return Response({
            'list': serializer.data
        })
