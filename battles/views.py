from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import PartyBattle, DamageLog

@login_required
def battles_view(request):
    return render(request, 'battles/index.html')
