from rest_framework import serializers, status
from user.models import Profile, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff')


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for UserProfile
    """

    user = UserSerializer(required=True)

    class Meta:
        model = Profile
        fields = ('user', 'avatar', 'nick_name', 'bio', 'location', 'age')

    # def create(self, validated_data):
    #     """
    #     Override the default create method of Model Serializer
    #     :param validated_data: Data containing all detail of Profile
    #     :return: Returns a successfully created profile record
    #     """
    #     user_data = validated_data.pop('user')
    #     user = UserSerializer.create(UserSerializer(), validated_data=user_data)
    #     profile, created = UserProfileSerializer.objects.update_or_create(
    #         user=user,
    #         avatar=validated_data.pop('avatar'),
    #         nick_name=validated_data.pop('nick_name'),
    #         bio=validated_data.pop('bio'),
    #         location=validated_data.pop('location'),
    #         age=validated_data.pop('age'),
    #     )
    #     return profile
