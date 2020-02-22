from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from repo.models import Lick, Genre, Instrument
from operator import attrgetter
from django.views import generic
from .forms import LickForm
from django.utils import timezone
from django.urls import reverse_lazy

from itertools import cycle
import re


def transpose_note(start, half_steps):
    if half_steps > 0:
        # transpose up
        chords = ["C", "Db", "D", "Eb", "E",
                  "F", "Gb", "G", "Ab", "A", "Bb", "B"]
    else:
        # transpose down
        chords = ["C", "B", "Bb", "A", "Ab",
                  "G", "Gb", "F", "E", "Eb", "D", "Db"]

    def custom_slice(lst, start):
        return(cycle(lst[start:] + lst[:start + 1]))
    position = custom_slice(chords, chords.index(start))
    for i in range(0, abs(half_steps) + 1):
        nxt = next(position)
    return(nxt)


def transpose_seq(chord_seq, half_steps):
    note_regex = r'_([a-gA-g]{1,2})_'
    # find all notes in chord seq
    old_notes = re.findall(note_regex, chord_seq)
    # transpose notes
    new_notes = list(
        map(lambda x: "_" + transpose_note(x, half_steps) + "_", old_notes))
    # replace chord seq with transposed notes

    def callback(match):
        return next(callback.v)
    callback.v = iter(new_notes)
    chord_seq_T = re.sub(note_regex, callback, chord_seq)
    return(chord_seq_T)


def is_valid_queryparam(param):
    return param != '' and param is not None


def home(request):
    return render(request, 'repo/home.html', {'title': 'Home'})


"""
def get_lick_queryset(genre_query=None, instrument_query=None):
    queryset = []

    licks = Lick.objects.filter(
        Q(genre__name__icontains=genre_query) &
        Q(instrument__name__icontains=instrument_query)
    ).distinct()
    for lick in licks:
        queryset.append(lick)

    return list(set(queryset))
"""


def browse_licks_view(request):

    # default no search parameters
    include_transposed = False
    genre_query = ""
    instrument_query = ""
    username_contains_query = ""
    chord_seq_query = ""
    # dummy for transpose before form submit
    chord_seq_queries_T = ["" for i in range(12)]
    time_signature = ""

    # if search submitted get parameters from URL
    if request.GET:
        include_transposed = bool(request.GET.get('include_transposed', ""))
        time_signature = request.GET.get('time_signature', "")
        genre_query = request.GET.get('genre', "")
        instrument_query = request.GET.get('instrument', "")
        username_contains_query = request.GET.get('username_contains', "")

        m1_b1 = request.GET.get('m1_b1', "")
        m1_b2 = request.GET.get('m1_b2', "")
        m1_b3 = request.GET.get('m1_b3', "")
        m1_b4 = request.GET.get('m1_b4', "")
        m2_b1 = request.GET.get('m2_b1', "")
        m2_b2 = request.GET.get('m2_b2', "")
        m2_b3 = request.GET.get('m2_b3', "")
        m2_b4 = request.GET.get('m2_b4', "")
        m3_b1 = request.GET.get('m3_b1', "")
        m3_b2 = request.GET.get('m3_b2', "")
        m3_b3 = request.GET.get('m3_b3', "")
        m3_b4 = request.GET.get('m3_b4', "")
        m4_b1 = request.GET.get('m4_b1', "")
        m4_b2 = request.GET.get('m4_b2', "")
        m4_b3 = request.GET.get('m4_b3', "")
        m4_b4 = request.GET.get('m4_b4', "")

        chord_seq = [
            m1_b1, m1_b2, m1_b3, m1_b4,
            m2_b1, m2_b2, m2_b3, m2_b4,
            m3_b1, m3_b2, m3_b3, m3_b4,
            m4_b1, m4_b2, m4_b3, m4_b4,
        ]

        # make regex query seq
        def get_chord_seq_query(chord_seq, half_steps=0):
            query = ""
            for chord in chord_seq:
                if chord != ".":
                    chord_T = transpose_seq(str(chord), half_steps)
                    query = query + "[x.]*" + chord_T
            query = query + "x"
            return query

        chord_seq_query = get_chord_seq_query(chord_seq, 0)

        if include_transposed == True:
            chord_seq_queries_T = []
            for half_step in range(0, 12):
                chord_seq_queries_T.append(
                    get_chord_seq_query(chord_seq, half_step))
            print(chord_seq_queries_T)

    # filter queryset with search parameters
    queryset = []

    licks = Lick.objects.filter(
        Q(time_signature__icontains=time_signature) &
        Q(genre__name__icontains=genre_query) &
        Q(instrument__name__icontains=instrument_query) &
        Q(author__username__icontains=username_contains_query)
    )

    if include_transposed == False:
        licks = licks.filter(
            Q(chord_seq__regex=chord_seq_query)
        )
    else:
        licks = licks.filter(
            Q(chord_seq__regex=chord_seq_queries_T[0]) |
            Q(chord_seq__regex=chord_seq_queries_T[1]) |
            Q(chord_seq__regex=chord_seq_queries_T[2]) |
            Q(chord_seq__regex=chord_seq_queries_T[3]) |
            Q(chord_seq__regex=chord_seq_queries_T[4]) |
            Q(chord_seq__regex=chord_seq_queries_T[5]) |
            Q(chord_seq__regex=chord_seq_queries_T[6]) |
            Q(chord_seq__regex=chord_seq_queries_T[7]) |
            Q(chord_seq__regex=chord_seq_queries_T[8]) |
            Q(chord_seq__regex=chord_seq_queries_T[9]) |
            Q(chord_seq__regex=chord_seq_queries_T[10]) |
            Q(chord_seq__regex=chord_seq_queries_T[11])
        )

    licks = licks.distinct()

    for lick in licks:
        queryset.append(lick)

    queryset = list(set(queryset))

    #licks = get_lick_queryset(query).order_by('-date_posted')
    licks = sorted(queryset, key=attrgetter('date_posted'), reverse=True)

    # paginate
    page = request.GET.get('page', 1)
    paginator = Paginator(licks, 3)
    licks = paginator.page(page)

    # pass values to context
    context = {}
    context["form"] = LickForm()
    context['licks'] = licks
    context["genres"] = Genre.objects.all()
    context["instrument"] = Instrument.objects.all().order_by('name')
    context["chord_seq_query"] = chord_seq_query  # used for template tags

    return render(request, "repo/browse_licks.html", context)


"""
m1_b1 = '_A_7'
m1_b2 = '_Dm_7'
m1_b3 = '_G_7'
m1_b4 = '_C_maj7'


chord_seq = [m1_b1, m1_b2, m1_b3, m1_b4]


chord_urls = list(map(lambda x: f'static/img/chords/{x}.png', chord_seq))

    context["chord_urls"] = ['static/img/chords/_A_7.png',
    'static/img/chords/_Dm_7.png',
    'static/img/chords/_G_7.png',
    'static/img/chords/_C_maj7.png']
"""


class LickListView(generic.ListView):
    model = Lick
    template_name = 'repo/all_licks.html'
    context_object_name = 'licks'
    paginate_by = 10
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):
        # some other stuff — where you create `context`
        context = super().get_context_data(**kwargs)
        context["form"] = LickForm()
        #gen = ["Any"]
        # for g in Genre.objects.all():
        # gen.append(g)
        context["genres"] = Genre.objects.all()
        context["instrument"] = Instrument.objects.all().order_by('name')
        return context

    def get_queryset(self):
        # search
        qs = Lick.objects.all()
        include_transposed = False
        genre_query = self.request.GET.get('genre')
        instrument_query = self.request.GET.get('instrument')
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
        def get_query(chord_seq, half_steps=0):
            query = ""
            for chord in chord_seq:
                if chord != ".":
                    chord_T = transpose_seq(str(chord), half_steps)
                    query = query + "[x.]*" + chord_T
            query = query + "x"
            return query

        if is_valid_queryparam(genre_query) and genre_query != 'Any':
            qs = qs.filter(genre__name=genre_query)

        if is_valid_queryparam(instrument_query) and instrument_query != 'Any':
            qs = qs.filter(instrument__name=instrument_query)

        if is_valid_queryparam(username_contains):
            print(username_contains)
            qs = qs.filter(author__username__icontains=username_contains)

        # filter by chord selection
        if include_transposed == False:
            query = get_query(chord_seq, 0)
            print(query)
            qs = qs.filter(chord_seq__regex=query)
        else:
            query_set_T = []
            for half_step in range(0, 12):
                query_set_T.append(get_query(chord_seq, half_step))
            print(query_set_T)
            Q(first_name__startswith='R') | Q(
                last_name__startswith='D').distinct()
            qs = qs.filter(
                Q(chord_seq__regex=query_set_T[0]) |
                Q(chord_seq__regex=query_set_T[1]) |
                Q(chord_seq__regex=query_set_T[2]) |
                Q(chord_seq__regex=query_set_T[3]) |
                Q(chord_seq__regex=query_set_T[4]) |
                Q(chord_seq__regex=query_set_T[5]) |
                Q(chord_seq__regex=query_set_T[6]) |
                Q(chord_seq__regex=query_set_T[7]) |
                Q(chord_seq__regex=query_set_T[8]) |
                Q(chord_seq__regex=query_set_T[9]) |
                Q(chord_seq__regex=query_set_T[10]) |
                Q(chord_seq__regex=query_set_T[11])
            )

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
