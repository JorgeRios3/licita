from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class HealthCheckMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.META['PATH_INFO'] == '/ping/':
            return HttpResponse('pong!')


class DisableBrowserCacheMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Pragma'] = 'no-cache'
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Expires'] = '0'
        return response