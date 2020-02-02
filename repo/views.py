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


def home(request):
    return render(request, 'repo/home.html', {'title': 'Home'})


def is_valid_queryparam(param):
    return param != '' and param is not None


class LickListView(generic.ListView):
    model = Lick
    form_class = LickForm
    template_name = 'repo/all_licks.html'
    context_object_name = 'licks'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # some other stuff — where you create `context`
        context = super().get_context_data(**kwargs)
        context["form"] = LickForm()
        return context

    def get_queryset(self):

        # search
        qs = Lick.objects.all()
        genre_exact_query = self.request.GET.get('genre_exact')
        username_contains = self.request.GET.get('username_contains')

        m1_b1 = self.request.GET.get('m1_b1')
        m1_b2 = self.request.GET.get('m1_b2')
        m1_b3 = self.request.GET.get('m1_b3')
        m1_b4 = self.request.GET.get('m1_b4')
        m2_b1 = self.request.GET.get('m2_b1')
        m2_b2 = self.request.GET.get('m2_b2')
        m2_b3 = self.request.GET.get('m2_b3')
        m2_b4 = self.request.GET.get('m2_b4')
        m3_b1 = self.request.GET.get('m3_b1')
        m3_b2 = self.request.GET.get('m3_b2')
        m3_b3 = self.request.GET.get('m3_b3')
        m3_b4 = self.request.GET.get('m3_b4')
        m4_b1 = self.request.GET.get('m4_b1')
        m4_b2 = self.request.GET.get('m4_b2')
        m4_b3 = self.request.GET.get('m4_b3')
        m4_b4 = self.request.GET.get('m4_b4')

        chord_seq = [
            m1_b1, m1_b2, m1_b3, m1_b4,
            m2_b1, m2_b2, m2_b3, m2_b4,
            m3_b1, m3_b2, m3_b3, m3_b4,
            m4_b1, m4_b2, m4_b3, m4_b4,
        ]

        # make regex query seq
        query = ""
        for chord in chord_seq:
            if chord != ".":
                print(chord)
                query = query + "[x.]*" + str(chord)

        query = query + "x"

        print(query)

        if is_valid_queryparam(username_contains):
            qs = qs.filter(author__username__icontains=username_contains)

        if is_valid_queryparam(genre_exact_query):
            qs = qs.filter(genre__name=genre_exact_query)

        # filter by chord selection
        qs = qs.filter(chord_seq__regex=query)

        # order
        qs = qs.order_by('-date_posted')

        return qs


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
