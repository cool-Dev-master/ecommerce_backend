# # middleware.py

# from django.http import JsonResponse

# class AuthenticationMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Check if the current user is authenticated
#         print(request.user, "user", request.user.is_authenticated, request.path)
#         if not request.user.is_authenticated and request.path != '/customers/login/':
#             return JsonResponse({'error': 'Authentication required Please login and try again'}, status=401)

#         response = self.get_response(request)
#         return response