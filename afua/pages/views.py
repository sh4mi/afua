from django.shortcuts import render


def home(requset):
    return render(requset, 'pages/landing.html')
