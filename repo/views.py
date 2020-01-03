from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
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
    paginate_by = 10


class UserLickListView(generic.ListView):
    model = Lick
    template_name = 'repo/user_licks.html'
    context_object_name = 'licks'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Lick.objects.filter(author=user).order_by('-date_posted')


class LickDetailView(generic.DetailView):
    model = Lick
    template_name = 'repo/lick_detail.html'


class LickCreateView(SuccessMessageMixin, LoginRequiredMixin, generic.CreateView):
    model = Lick
    form_class = LickForm
    success_url = reverse_lazy('lick-create')
    success_message = f'Lick has been created successfully, you may upload another one!'
    template_name = 'repo/lick_form.html'

    def form_valid(self, form):
        if Lick.objects.filter(author=self.request.user).count() == 0:
            form.instance.counter = 1
        else:
            form.instance.counter = Lick.objects.filter(author=self.request.user).order_by(
                '-date_posted').first().counter + 1  # Lick number for each author

        form.instance.author = self.request.user
        return super().form_valid(form)


class LickUpdateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Lick
    form_class = LickForm
    success_url = reverse_lazy('home')
    success_message = f'Lick has been successfully updated!'
    template_name = 'repo/lick_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class LickDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Lick
    template_name = 'repo/lick_confirm_delete.html'
    success_url = reverse_lazy('home')
    success_message = f'Lick has been deleted!'

    def delete(self, request, *args, **kwargs):  # this replaces SuccessMessageMixin
        messages.success(self.request, self.success_message)
        return super(LickDeleteView, self).delete(request, *args, **kwargs)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# redirecting back to home
# redirect to home and make success message appear


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
