
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError

from accounts.models import User
from character.models import Character


def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    return render(request, 'landing.html')


def login_view(request):
    if request.method == 'POST':
        # Your custom User model uses email as USERNAME_FIELD.
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')

        if not email or not password:
            messages.error(request, "Please enter your email and password.")
            return render(request, 'accounts/login.html')

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        messages.error(request, "Invalid email or password.")

    return render(request, 'accounts/login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')

        if not username or not email or not password:
            messages.error(request, "All fields are required.")
            return render(request, 'accounts/register.html')

        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'accounts/register.html')

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, 'accounts/register.html')

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # Create the RPG character for the new user.
            Character.objects.get_or_create(user=user)

            login(request, user)

            return redirect('onboarding')

        except (ValidationError, ValueError) as error:
            messages.error(request, str(error))

    return render(request, 'accounts/register.html')


def logout_view(request):
    """
    Log the current user out of the Django session.
    """
    if request.method == 'POST':
        logout(request)
        return redirect('landing')

    # Do not allow logout through a normal GET request.
    return redirect('dashboard')


@login_required
def onboarding_view(request):
    if request.method == 'POST':
        rpg_class = request.POST.get('rpg_class', '').strip().upper()

        char, created = Character.objects.get_or_create(
            user=request.user
        )

        # Prevent changing the class after it has already been selected.
        if getattr(char, 'rpg_class', None):
            messages.info(
                request,
                "Your RPG class has already been selected."
            )
            return redirect('dashboard')

        # Get the valid choices directly from the model field.
        field = Character._meta.get_field('rpg_class')
        valid_classes = {
            str(value).upper()
            for value, label in field.choices
        }

        if rpg_class not in valid_classes:
            messages.error(
                request,
                "Please select a valid RPG class."
            )
            return render(
                request,
                'accounts/onboarding.html'
            )

        char.rpg_class = rpg_class

        # Apply starting attribute bonuses.
        # These are only applied if the corresponding fields exist.
        bonuses = {
            'WARRIOR': {
                'strength': 5,
                'vitality': 2,
            },
            'MAGE': {
                'intellect': 5,
                'wisdom': 2,
            },
            'ROGUE': {
                'agility': 5,
                'discipline': 2,
            },
            'RANGER': {
                'agility': 5,
                'wisdom': 2,
            },
            'MONK': {
                'discipline': 5,
                'vitality': 2,
            },
            'ENGINEER': {
                'intellect': 5,
                'discipline': 2,
            },
            'PALADIN': {
                'vitality': 5,
                'strength': 2,
            },
            'ARCHER': {
                'agility': 5,
                'strength': 2,
            },
        }

        selected_bonuses = bonuses.get(rpg_class, {})

        for attribute, amount in selected_bonuses.items():
            if hasattr(char, attribute):
                current_value = getattr(char, attribute, 0)
                setattr(char, attribute, current_value + amount)

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
    user = request.user

    if request.method == 'POST':

        # Update timezone if the field exists.
        if hasattr(user, 'timezone'):
            user.timezone = request.POST.get(
                'timezone',
                user.timezone
            )

        # Update theme if the field exists.
        if hasattr(user, 'theme'):
            user.theme = request.POST.get(
                'theme',
                user.theme
            )

        # Update profile visibility if the field exists.
        if hasattr(user, 'profile_visibility'):
            user.profile_visibility = request.POST.get(
                'profile_visibility',
                user.profile_visibility
            )

        # Update email notifications if the field exists.
        if hasattr(user, 'email_notifications'):
            user.email_notifications = (
                request.POST.get('email_notifications') == 'on'
            )

        # Update reduced motion if the field exists.
        if hasattr(user, 'reduced_motion'):
            user.reduced_motion = (
                request.POST.get('reduced_motion') == 'on'
            )

        # Update avatar if uploaded.
        if 'avatar' in request.FILES and hasattr(user, 'avatar'):
            user.avatar = request.FILES['avatar']

        # Change password if requested.
        new_password = request.POST.get(
            'new_password',
            ''
        ).strip()

        password_changed = False

        if new_password:
            try:
                from django.contrib.auth.password_validation import (
                    validate_password
                )

                validate_password(
                    new_password,
                    user
                )

                user.set_password(new_password)
                password_changed = True

            except ValidationError as error:
                for error_message in error.messages:
                    messages.error(
                        request,
                        error_message
                    )

                return render(
                    request,
                    'settings/index.html'
                )

        user.save()

        # Keep the user logged in after changing password.
        if password_changed:
            update_session_auth_hash(
                request,
                user
            )

        messages.success(
            request,
            "Settings updated successfully."
        )

        return redirect('settings')

    return render(
        request,
        'settings/index.html'
    )

