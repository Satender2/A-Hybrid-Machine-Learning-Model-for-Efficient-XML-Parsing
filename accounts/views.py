from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm, UserProfileUpdateForm

def landing_page(request):
    """Landing page with project information"""
    if request.user.is_authenticated:
        if request.user.user_type == 'admin':
            return redirect('admin_panel:dashboard')
        return redirect('dashboard:home')
    
    return render(request, 'accounts/landing.html')


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        form = UserRegistrationForm()
        return render(request, 'accounts/register.html', {'form': form})
    
    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'user'
            user.save()
            messages.success(request, 'Registration successful! Please login.')
            return redirect('accounts:login')
        return render(request, 'accounts/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.user_type == 'admin':
                return redirect('admin_panel:dashboard')
            return redirect('dashboard:home')
        form = UserLoginForm()
        return render(request, 'accounts/login.html', {'form': form})
    
    def post(self, request):
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                
                if user.user_type == 'admin':
                    return redirect('admin_panel:dashboard')
                return redirect('dashboard:home')
        
        messages.error(request, 'Invalid username or password.')
        return render(request, 'accounts/login.html', {'form': form})


class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.success(request, 'Logged out successfully.')
        return redirect('accounts:landing')


@login_required
def profile_view(request):
    """User profile view and update"""
    user = request.user
    
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileUpdateForm(instance=user)
    
    # Get user statistics
    from xml_profiler.models import XMLFile
    total_uploads = XMLFile.objects.filter(user=user).count()
    
    context = {
        'form': form,
        'user': user,
        'total_uploads': total_uploads
    }
    
    return render(request, 'accounts/profile.html', context)
