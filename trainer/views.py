from django.shortcuts import render, redirect
from authentication.models import User
from about.models import Trainer, Skills, Trainings
# Create your views here.

def trainer_dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        if Trainer.objects.filter(created_by=user).exists():
            # skills = Skills.objects.filter(trainer=trainer.id)
            # # trainings = Trainings.objects.filter(trainer=trainer.id)
            trainer = Trainer.objects.filter(created_by=user)
            context = {
            'trainer': trainer,
            'page_title': 'Trainer Profile',
            # 'skills': skills,
            # 'trainings': trainings,
            }
            return render(request, 'trainer/dashboard.html', context)
        else:
            return render(request, 'trainer/newform.html')
    else:
        return redirect("account_login")

def sidebar(request):
    if request.user.is_authenticated:
        user = request.user
        trainer = Trainer.objects.filter(created_by=user)
        # skills = Skills.objects.filter(trainer=trainer.id)
        # trainings = Trainings.objects.filter(trainer=trainer.id)
        context = {
            'trainer': trainer,
            'page_title': 'Trainer Profile',
            # 'skills': skills,
            # 'trainings': trainings,
            }
        return render(request, 'trainer/base.html', context)
    else:
        return redirect("account_login")

def profile_update(request):
    if request.user.is_authenticated and request.user.role == 4:
        return render(request, 'trainer/profileUpdate.html')
    else:
        return redirect("account_login")
