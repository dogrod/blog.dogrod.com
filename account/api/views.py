from django.shortcuts import render

# Create your views here.
def jwt_response_payload_handler(token, user, request, *args, **kwargs):
  data = {
    'token': token,
    'user': {
      'id': user.id,
      'username': user.username,
      'email': user.email,
      'active': user.is_active,
      'staff': user.is_staff
    }
  }
  return data