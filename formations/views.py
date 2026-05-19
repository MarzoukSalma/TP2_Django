from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Formation
from .forms import FormationForm

# ---- vues normales ----

def is_admin(user):
    return user.is_staff

@login_required
def liste_formations(request):
    formations = Formation.objects.all()
    return render(request, 'formations/liste.html', {'formations': formations})

@login_required
@user_passes_test(is_admin)
def ajouter_formation(request):
    form = FormationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('liste_formations')
    return render(request, 'formations/form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def modifier_formation(request, pk):
    formation = get_object_or_404(Formation, pk=pk)
    form = FormationForm(request.POST or None, instance=formation)
    if form.is_valid():
        form.save()
        return redirect('liste_formations')
    return render(request, 'formations/form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def supprimer_formation(request, pk):
    formation = get_object_or_404(Formation, pk=pk)
    if request.method == 'POST':
        formation.delete()
        return redirect('liste_formations')
    return render(request, 'formations/confirmer_suppression.html', {'formation': formation})

# ---- vues API ----

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .serializers import FormationSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_liste_formations(request):
    formations = Formation.objects.all()
    serializer = FormationSerializer(formations, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def api_ajouter_formation(request):
    serializer = FormationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def api_formation_detail(request, pk):
    try:
        formation = Formation.objects.get(pk=pk)
    except Formation.DoesNotExist:
        return Response({'error': 'Formation introuvable'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FormationSerializer(formation)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = FormationSerializer(formation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        formation.delete()
        return Response({'message': 'Formation supprimée'}, status=status.HTTP_204_NO_CONTENT)