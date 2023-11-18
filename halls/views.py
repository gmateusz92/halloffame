from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Hall, Video
from .forms import VideoForm, SearchForm
from django.http import Http404


# Create your views here.
# def home(request):
#     recent_halls = Hall.objects.all().order_by('-id')[:3]
#     popular_halls = [Hall.objects.get(pk=1),Hall.objects.get(pk=2),Hall.objects.get(pk=3)]
#     return render(request, 'halls/home.html', {'recent_halls':recent_halls, 'popular_halls':popular_halls})

youtube_api_key = 'AIzaSyDA3SNzwY4FiTQ9chdwmcEL5Kk0QBPlSWg'

def home(request):
    return render(request, 'halls/home.html')

def dashboard(request):
    halls = Hall.objects.filter(user=request.user)
    return render(request, 'halls/dashboard.html', {'halls':halls})

def add_video(request, pk): #pip install django-widget-tweaks
    form = VideoForm()
    search_form = SearchForm()
    hall = Hall.objects.get(pk=pk)
    if not hall.user == request.user:
        raise Http404

    if request.method == 'POST':
        # Create
        filled_form = VideoForm(request.POST)
        if filled_form.is_valid():
            video = Video()
            video.url = filled_form.cleaned_data['url']
            video.title = filled_form.cleaned_data['title']
            video.youtube_id = filled_form.cleaned_data['youtube_id']
            video.hall = hall
            video.save()

    return render(request, 'halls/add_video.html', {'form': form, 'search_form': search_form, 'hall': hall})


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self, form): # dzieki temu automatyczne logowanie
        view = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return view



class CreateHall(generic.CreateView): #generic views to gdy uzytkownik nie musi byc zalogowany
    model = Hall
    fields = ['title']
    template_name = 'halls/create_hall.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreateHall, self).form_valid(form)
        return redirect('home')
    
class DetailHall(generic.DetailView):
    model = Hall
    template_name = 'halls/detail_hall.html'    

class UpdateHall(generic.UpdateView):
    model = Hall
    fields = ['title']  # Dodaj pola, które chcesz zaktualizować
    template_name = 'halls/update_hall.html'  # Dodaj odpowiedni szablon
    success_url = reverse_lazy('dashboard')     

class DeleteHall(generic.DeleteView):
    model = Hall
    template_name = 'halls/delete_hall.html'  # Dodaj odpowiedni szablon
    success_url = reverse_lazy('dashboard')      