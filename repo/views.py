from django.shortcuts import render, redirect
from repo.models import Lick
from django.views import generic
from .forms import LickForm
from django.utils import timezone
from django.urls import reverse_lazy


def about(request):
    return render(request, 'repo/about.html', {'title': 'About'})


class LickListView(generic.ListView):
    model = Lick
    template_name = 'repo/home.html'
    context_object_name = 'licks'
    ordering = ['-date_posted']  # minus reverses order
    #paginate_by = 5


class LickDetailView(generic.DetailView):
    model = Lick
    template_name = 'repo/lick_detail.html'


class LickCreateView(generic.CreateView):
    model = Lick
    form_class = LickForm
    success_url = reverse_lazy('lick-create')
    template_name = 'repo/lick_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# check corey 26:30
# https://www.youtube.com/watch?v=-s7e_Fy6NRU&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=10
# https://www.youtube.com/watch?v=HSn-e2snNc8
# trying to replace function based form with class based form to upload list


# function based view that goes with lick_new.html template
"""
def lick_new(request):
    if request.method == "POST":
        form = LickForm(request.POST, request.FILES)
        if form.is_valid():
            lick = form.save()
            lick.author = request.user
            lick.date_posted = timezone.now()
            lick.last_updated = timezone.now()
            lick.save()
            return redirect('home')
    else:
        form = LickForm()
    return render(request, 'repo/lick_new.html', {'form': form})
"""
