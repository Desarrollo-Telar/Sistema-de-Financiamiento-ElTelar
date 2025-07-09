# URLS
from django.urls import path, include

# http
from project.http.request_400 import error400, error404


urlpatterns_http = [
    path('error/404/',error404, name='http_404')
]