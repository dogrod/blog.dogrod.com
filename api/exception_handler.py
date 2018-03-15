from rest_framework.views import exception_handler

# from rest_framework import status


def custom_exception_handler(exc, context):
    '''
    Custom exception handler for DRF.
    Follow from http://www.django-rest-framework.org/api-guide/exceptions/#custom-exception-handling
    '''
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        print(response.data)
        response.data['code'] = response.status_code

    return response
