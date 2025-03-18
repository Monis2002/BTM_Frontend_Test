from .models import Category
from .models import Profile

def categories_context(request):
    categories = Category.objects.all()
    return {'categories': categories}

def location_context(request):
    # Fetch unique locations from Profile
    all_location = Profile.objects.values_list('city', flat=True).distinct()
    return {'all_location': all_location}