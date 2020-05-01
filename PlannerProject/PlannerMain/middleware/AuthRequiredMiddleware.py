from django.http import HttpResponseRedirect
from django.urls import reverse

class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)
        
        if not request.path == reverse('login') and not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login')) # or http response


        return response