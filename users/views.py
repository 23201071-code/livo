from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserSignUpForm, ProfileUpdateForm
from .models import LifestylePreference, PreferenceTag
from househelp.models import Househelp

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            # 1. Create the User object
            user = form.save()

            # 2. Extract and handle role-specific data
            role = user.role

            if role == 'ROOMMATE':
                # Create Lifestyle Profile and link tags
                profile = LifestylePreference.objects.create(user=user)
                selected_preferences = form.cleaned_data.get('preferences')
                if selected_preferences:
                    profile.preferences.set(selected_preferences)

            elif role == 'HOUSE_HELP':
                # Create Househelp Profile and link skills
                profile = Househelp.objects.create(user=user)
                selected_skills = form.cleaned_data.get('skills')
                if selected_skills:
                    profile.skills.set(selected_skills)

            # 3. Log the user in and redirect
            login(request, user)
            return redirect('landing')
    else:
        form = UserSignUpForm()

    # Group preferences for categorized display in the template
    grouped_preferences = {}
    for cat_code, cat_name in PreferenceTag.CATEGORY_CHOICES:
        tags = PreferenceTag.objects.filter(category=cat_code)
        if tags.exists():
            grouped_preferences[cat_name] = tags

    return render(request, 'signup.html', {
        'form': form,
        'grouped_preferences': grouped_preferences
    })

def logout_view(request):
    logout(request)
    return redirect('landing')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

