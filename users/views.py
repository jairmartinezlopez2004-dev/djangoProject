from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from users.models import Product
from .forms import RegisterForm


def get_user(request):
    return HttpResponse("<h1>Hello World!</h1>")


def inicio(request):
    products = Product.objects.all()
    context = {
        "name": "Jair",
        "email": "jair@email.com",
        "age": 22,
        "resumen": ["Estudiante de Ingeniería en Sistemas"],
        "products": products,
    }
    return render(request, "base.html", context=context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
