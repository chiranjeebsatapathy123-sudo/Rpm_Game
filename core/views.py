from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import User
from character.models import Character

def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')

def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'accounts/login.html')

def register_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        e = request.POST.get('email')
        p = request.POST.get('password')
        if User.objects.filter(username=u).exists():
            messages.error(request, "Username already exists.")
        else:
            user = User.objects.create_user(username=u, email=e, password=p)
            Character.objects.create(user=user)
            login(request, user)
            return redirect('onboarding')
    return render(request, 'accounts/register.html')

def logout_view(request):
    logout(request)
    return redirect('landing')

@login_required
def onboarding_view(request):
    if request.method == 'POST':
        rpg_class = request.POST.get('rpg_class')
        char = request.user.character
        char.rpg_class = rpg_class
        
        # Apply bonuses
        if rpg_class == 'WARRIOR':
            char.strength += 5; char.vitality += 2
        elif rpg_class == 'MAGE':
            char.intellect += 5; char.wisdom += 2
        elif rpg_class == 'ROGUE':
            char.agility += 5; char.discipline += 2
        elif rpg_class == 'ENGINEER':
            char.intellect += 5; char.discipline += 2
        elif rpg_class == 'PALADIN':
            char.vitality += 5; char.strength += 2
        elif rpg_class == 'ARCHER':
            char.agility += 5; char.strength += 2
            
        char.save()
        return redirect('dashboard')
    return render(request, 'accounts/onboarding.html')

@login_required
def dashboard_view(request):
    return render(request, 'dashboard/index.html')

@login_required
def quests_view(request):
    return render(request, 'quests/index.html')

@login_required
def character_view(request):
    return render(request, 'character/index.html')

@login_required
def achievements_view(request):
    return render(request, 'achievements/index.html')

@login_required
def shop_view(request):
    return render(request, 'shop/index.html')

@login_required
def inventory_view(request):
    return render(request, 'inventory/index.html')

@login_required
def analytics_view(request):
    return render(request, 'analytics/index.html')

@login_required
def social_view(request):
    return render(request, 'social/index.html')

@login_required
def settings_view(request):
    if request.method == 'POST':
        user = request.user
        user.timezone = request.POST.get('timezone', user.timezone)
        user.theme = request.POST.get('theme', user.theme)
        user.profile_visibility = request.POST.get('profile_visibility', user.profile_visibility)
        user.email_notifications = request.POST.get('email_notifications') == 'on'
        user.reduced_motion = request.POST.get('reduced_motion') == 'on'
        
        # If the user is trying to change their password, handle it
        if 'new_password' in request.POST and request.POST['new_password']:
            user.set_password(request.POST['new_password'])
            
        # Handle avatar upload
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']
            
        user.save()
        messages.success(request, "Settings updated successfully.")
        
        # If password changed, re-login the user to prevent session invalidation
        if 'new_password' in request.POST and request.POST['new_password']:
            login(request, user)
            
        return redirect('settings')
        
    return render(request, 'settings/index.html')
