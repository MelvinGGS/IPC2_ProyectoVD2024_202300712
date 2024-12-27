from django.shortcuts import render

def login_view(request):
    return render(request, "login/templates/login.html")  # Asegúrate de que la ruta coincida con tu estructura
