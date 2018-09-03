# Create your views here.
def jwt_response_payload_handler(token, user, request, *args, **kwargs):
    profile = user.get_profile()
    data = {
        'token': token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'active': user.is_active,
            'staff': user.is_staff,
            'nickname': profile.nick_name,
        }
    }
    return data
