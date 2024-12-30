from django.shortcuts import render
import requests

def index(request):
    return  render(request, 'index.html')

def admin(reqquest):
    return render(reqquest, 'admin.html')

def user(request):
    return render(request, 'user.html')