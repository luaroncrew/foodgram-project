from django.shortcuts import render, redirect

from .forms import CreationForm


def registration(request):
    form = CreationForm()
    if request.method == 'POST':
        form = CreationForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}

    return render(request, 'users/reg.html', context)
