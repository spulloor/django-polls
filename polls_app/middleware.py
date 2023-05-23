from django.http import JsonResponse

class JSONResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 404 and not request.path.endswith('/'):
            return JsonResponse(
                {"message": "Invalid API route. Please try again.", "status": 404},
                status=404
            )

        return response
