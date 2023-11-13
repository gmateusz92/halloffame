from django.shortcuts import render

# Create your views here.
# def home(request):
#     recent_halls = Hall.objects.all().order_by('-id')[:3]
#     popular_halls = [Hall.objects.get(pk=1),Hall.objects.get(pk=2),Hall.objects.get(pk=3)]
#     return render(request, 'halls/home.html', {'recent_halls':recent_halls, 'popular_halls':popular_halls})

def home(request):
    return render(request, 'halls/home.html')