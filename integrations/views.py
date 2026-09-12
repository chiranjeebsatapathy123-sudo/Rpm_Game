from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def integrations_view(request):
    return render(request, 'integrations/index.html')
