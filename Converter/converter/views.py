# converter/views.py
from django.shortcuts import render


def main(request):
    return render(request, "converter/main.html")
