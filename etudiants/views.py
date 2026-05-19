from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from formations.models import Formation
from .models import Etudiant

def is_etudiant(user):
    return not user.is_staff

@login_required
def inscrire(request, pk):
    if request.user.is_staff:
        return redirect('liste_formations')  # admin ne peut pas s'inscrire
    
    formation = get_object_or_404(Formation, pk=pk)
    etudiant, created = Etudiant.objects.get_or_create(
        user=request.user,
        defaults={
            'nom': request.user.last_name,
            'prenom': request.user.first_name,
            'email': request.user.email,
        }
    )
    etudiant.formation = formation
    etudiant.save()
    return redirect('liste_formations')