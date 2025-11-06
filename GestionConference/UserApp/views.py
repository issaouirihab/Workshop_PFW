from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth import logout

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        # si le form n'est pas valide, on va retomber en bas et le réafficher
    else:
        # ici c'est le GET : on affiche un formulaire vide
        form = UserRegisterForm()

    # commun aux deux cas
    return render(request, "register.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")
       
# Create your views here.
