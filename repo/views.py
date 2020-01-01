from django.shortcuts import render, redirect
from repo.models import Lick
from django.views import generic
#from .forms import LickForm
#from django.utils import timezone


def about(request):
    return render(request, 'repo/about.html', {'title': 'About'})


class LickListView(generic.ListView):
    model = Lick
    template_name = 'repo/home.html'
    context_object_name = 'licks'
    ordering = ['-date_posted']  # minus reverses order
    #paginate_by = 5


"""

class LickDetailView(generic.DetailView):
    model = Lick
    template_name = 'repo/lick_detail.html'


def lick_new(request):
    if request.method == "POST":
        form = LickForm(request.POST, request.FILES)
        if form.is_valid():
            lick = form.save(commit=False)
            #lick.author = request.user
            lick.date_posted = timezone.now()
            lick.last_updated = timezone.now()
            lick.save()
            return redirect('lick-detail', pk=lick.pk)
    else:
        form = LickForm()
    return render(request, 'repo/lick_edit.html', {'form': form})

"""
