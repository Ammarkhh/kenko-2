from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from fitness.models import Program


def home_view(request):
    return render(request, "views/home.html")


def fitness_view(request):
    programs = Program.objects.all()
    return render(request, "views/fitness.html", context={
        "programs": programs
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user:
                # Check if admin
                if user.is_superuser or user.is_staff:
                    messages.error(request, "You are an admin, you can not login here.")
                    return redirect("login")

                login(request, user)
                messages.success(request, f"You are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="views/login.html", context={"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("home")

def hub_view(request):
    return render(request, "views/hub.html", context={"survey": "aouaou"})