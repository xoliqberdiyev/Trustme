from rest_framework.response import Response

def success_message(msg, status_code):
    return Response(
        {'success': True, 'message': msg},
        status=status_code,
    )

def error_message(msg, status_code):
    return Response(
        {'success': False, 'message': msg},
        status=status_code,
    )
