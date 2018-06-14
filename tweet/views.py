from django.shortcuts import render, get_object_or_404
from .models import Profile

def index(request):
    object_name = Profile.objects.all()
    return render(request, 'tweet/index.html', {'object_name': object_name})

def detail(request, profile_id):
    profiles = get_object_or_404(Profile, pk=profile_id)
    object_name = Profile.objects.all()
    return render(request, 'tweet/detail.html', {'profiles': profiles, 'object_name': object_name})