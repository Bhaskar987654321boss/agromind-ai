from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, user_passes_test
from crops.models import RecommendationLog, YieldLog, DiseaseLog
from django.db.models import Count

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

def register(request):
    if request.method == 'POST':
        # Simple registration for demo (using default UserCreationForm would need custom user model support)
        # Creating a custom form is better, but for speed, let's manually handle or use a simple form
        # Let's use a minimal custom form approach or just manual creation for the stub
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role', 'FARMER')
        
        if User.objects.filter(username=username).exists():
            return render(request, 'users/register.html', {'error': 'Username already exists'})
            
        user = User.objects.create_user(username=username, email=email, password=password, role=role)
        login(request, user)
        return redirect('home')
        
    return render(request, 'users/register.html')

@login_required
def user_dashboard(request):
    recommendations = RecommendationLog.objects.filter(user=request.user).order_by('-created_at')[:5]
    yields = YieldLog.objects.filter(user=request.user).order_by('-created_at')[:5]
    diseases = DiseaseLog.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    context = {
        'recommendations': recommendations,
        'yields': yields,
        'diseases': diseases
    }
    return render(request, 'users/dashboard.html', context)

@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    # Stats
    total_users = User.objects.count()
    total_recommendations = RecommendationLog.objects.count()
    total_yields = YieldLog.objects.count()
    total_diseases = DiseaseLog.objects.count()
    
    # Recent Activity
    recent_recommendations = RecommendationLog.objects.all().order_by('-created_at')[:10]
    
    # Popular Crops (from recommendations)
    popular_crops = RecommendationLog.objects.values('recommended_crop').annotate(count=Count('recommended_crop')).order_by('-count')[:5]
    
    context = {
        'total_users': total_users,
        'total_recommendations': total_recommendations,
        'total_yields': total_yields,
        'total_diseases': total_diseases,
        'recent_recommendations': recent_recommendations,
        'popular_crops': popular_crops
    }
    return render(request, 'users/admin_dashboard.html', context)
