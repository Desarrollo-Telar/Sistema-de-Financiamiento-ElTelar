# URL
from django.shortcuts import render, redirect

#HTTP ERROR
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import UserPassesTestMixin

def error400(request, exception=None):
    return render(request, 'http/400/400.html',{
        'title':'ERROR 400',
        'status':400
    })

def error403(request, exception=None):
    return render(request, 'http/400/403.html',{
        'title':'ERROR 403',
        'status': 403,
    })