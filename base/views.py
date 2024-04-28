from django.shortcuts import render, redirect
from .models import Receipe
import os
from django.conf import settings
# Create your views here.
def home(request):
    foods = Receipe.objects.all()
    if request.method == "POST":
        search = request.POST.get('search')
        foods = foods.filter(name__icontains = search)
    return render(request, 'index.html', context= {'foods':foods})

def create(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        print(name, description, image)
        Receipe.objects.create(name=name, description=description, image=image)
        return redirect('home')
    return render(request, 'create.html')

def edit(request, pk):
    foods = Receipe.objects.get(id=pk)
    img = foods.image
    if request.method == "POST":
        foods.name = request.POST.get('name')
        foods.description = request.POST.get('description')
        foods.image = request.FILES.get('image')
        if foods.image == None:
            foods.image = img
            foods.save()
        else:
            os.remove(f'media/{img}')   
            foods.save()
        return redirect('home')
    return render(request, 'edit.html', context={'foods':foods})

def delete(request, pk):
    foods = Receipe.objects.get(id=pk)
    img =foods.image
    os.remove(f'media/{img}')
    foods.delete()
    return redirect('home')

   