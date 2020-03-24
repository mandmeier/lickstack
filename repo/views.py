from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from repo.models import Lick, Instrument
from operator import attrgetter
from django.views import generic
from .forms import LickForm
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

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


def browse_licks_view(request):

    # default no search parameters
    exact_search = False
    include_transposed = False
    ignore_extensions = False
    must_contain_keyword = False
    instrument_query = ""
    username_contains_query = ""
    chord_seq_query = ""
    lick_id_query = 0
    # dummy for transpose before form submit
    chord_seq_queries_T = ["" for i in range(12)]
    time_signature = ""
    instrument_list = [""]
    keyword_list = [""]

    # if search submitted get parameters from URL
    if request.GET:
        exact_search = bool(request.GET.get('exact_search', ""))
        include_transposed = bool(request.GET.get('include_transposed', ""))
        ignore_extensions = bool(request.GET.get('ignore_extensions', ""))
        time_signature = request.GET.get('time_signature', "")
        instrument_query = request.GET.get('instrument', "")
        username_contains_query = request.GET.get('username_contains', "")
        lick_id_query = request.GET.get('lick_id', "")
        if not lick_id_query.isdigit():
            lick_id_query = 0
        else:
            lick_id_query = int(lick_id_query.strip())

        chord_seq = request.GET.get('chord_seq', "").split('x')[1:15]
        instrument_string = request.GET.get('instr_seq', "")
        keyword_string = request.GET.get('tags', "")
        must_contain_keyword = bool(request.GET.get('must_contain', ""))

        print('TEST')
        print(instrument_string)
        print(keyword_string)

        instrument_list = instrument_string.split(',')
        print(instrument_list)

        keyword_list = keyword_string.split(',')
        print(keyword_list)

        # make regex query seq
        def get_chord_seq_query(chord_seq, half_steps=0):
            query = ""
            if exact_search == False:
                for chord in chord_seq:
                    if chord != ".":
                        chord_T = transpose_seq(str(chord), half_steps)
                        query = query + "[x.]*" + chord_T
                query = query + "x"

            else:
                while chord_seq[len(chord_seq) - 1] == ".":
                    chord_seq.pop()
                chord_seq.reverse()
                while chord_seq[len(chord_seq) - 1] == ".":
                    chord_seq.pop()
                chord_seq.reverse()
                for chord in chord_seq:
                    if chord != ".":
                        chord = transpose_seq(str(chord), half_steps)
                    query = query + chord + "x"

            if ignore_extensions == True:
                m = "(_m7b5|_m7|_m(?!a))"
                notm = "(_|_7|_maj7|_6|_dim|_sus4)"
                query = re.sub(r'((_m7b5)|(_m7)|(_m(?!a)))', m, query)
                query = re.sub(
                    r'((_maj7)|(_7)|(_6)|(_dim)|(_sus4)|(_(?=[\[x])))', notm, query)

            return query

        chord_seq_query = get_chord_seq_query(chord_seq, 0)

        if include_transposed == True:
            chord_seq_queries_T = []
            for half_step in range(0, 12):
                chord_seq_queries_T.append(
                    get_chord_seq_query(chord_seq, half_step))

    # filter queryset with search parameters
    queryset = []

    licks = Lick.objects.filter(
        Q(time_signature__icontains=time_signature) &
        Q(author__username__icontains=username_contains_query)
    )

    instrument_search = Q()
    for item in instrument_list:
        instrument_search |= Q(instrument__name__icontains=item)

    licks = licks.filter(instrument_search)

    if keyword_list != [""]:
        if must_contain_keyword == True:
            for item in keyword_list:
                licks = licks.filter(tags__slug__in=[item])
        else:
            licks = licks.filter(tags__slug__in=keyword_list)

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

    if lick_id_query > 0:
        licks = licks.filter(id=lick_id_query)

    licks = licks.distinct()

    for lick in licks:
        queryset.append(lick)

    queryset = list(set(queryset))

    # licks = get_lick_queryset(query).order_by('-date_posted')
    licks = sorted(queryset, key=attrgetter('date_posted'), reverse=True)

    if request.user.is_authenticated:
        # find if user liked any of those licks
        user_liked = []
        for lick in licks:
            if lick in request.user.profile.liked_licks.all():
                user_liked.append(lick)

        # find if user faved any of those licks
        user_faved = []
        for lick in licks:
            if lick in request.user.profile.faved_licks.all():
                user_faved.append(lick)
    else:
        user_liked = []
        user_faved = []

    # paginate
    page = request.GET.get('page', 1)
    paginator = Paginator(licks, 6)
    licks = paginator.page(page)

    # pass values to context
    context = {}
    context["form"] = LickForm()
    context['licks'] = licks
    context["instrument"] = Instrument.objects.all().order_by('name')
    context["chord_seq_query"] = chord_seq_query  # used for template tags
    context["user_liked"] = user_liked
    context["user_faved"] = user_faved
    # remember form input
    # context["username_contains_query"] = username_contains_query

    return render(request, "repo/browse_licks.html", context)


@login_required
def my_licks_view(request):
    chord_seq_query = ""
    licks = Lick.objects.all()
    licks = licks.filter(author=request.user)  # get current user id
    display = ""

    if request.GET:
        display = request.GET.get('display', "")
        if display == "mylicks":
            licks = licks.filter(author=request.user)

        if display == "favorites":
            licks = request.user.profile.faved_licks.all()

    # licks = get_lick_queryset(query).order_by('-date_posted')
    licks = sorted(licks, key=attrgetter('date_posted'), reverse=True)

    # paginate
    page = request.GET.get('page', 1)
    paginator = Paginator(licks, 6)
    licks = paginator.page(page)

    # find if user liked any of those licks
    user_liked = []
    for lick in licks:
        if lick in request.user.profile.liked_licks.all():
            user_liked.append(lick)

    # find if user faved any of those licks
    user_faved = []
    for lick in licks:
        if lick in request.user.profile.faved_licks.all():
            user_faved.append(lick)

    context = {}
    context['licks'] = licks
    context["chord_seq_query"] = chord_seq_query  # used for template tags
    context["user_liked"] = user_liked
    context["user_faved"] = user_faved
    context["display"] = display

    return render(request, "repo/my_licks.html", context)


def lick_detail(request, pk):
    lick = get_object_or_404(Lick, id=pk)
    is_liked = False
    if lick.likes.filter(id=request.user.id).exists():
        is_liked = True

    context = {}
    context['lick'] = lick
    context['is_liked'] = is_liked
    context['total_likes'] = lick.total_likes()

    return render(request, 'repo/lick_detail.html', context)


def like_lick(request):
    lick = get_object_or_404(Lick, id=request.POST.get('id'))
    is_liked = False
    if lick.likes.filter(id=request.user.id).exists():
        lick.likes.remove(request.user)
        request.user.profile.liked_licks.remove(lick)
        is_liked = False
    else:
        lick.likes.add(request.user)
        request.user.profile.liked_licks.add(
            lick)  # add to liked licks in profile
        is_liked = True

    user_liked = request.user.profile.liked_licks.all()

    context = {}
    context['lick'] = lick
    context['is_liked'] = is_liked
    context['total_likes'] = lick.total_likes()
    context["user_liked"] = user_liked

    if request.is_ajax():
        html = render_to_string(
            'repo/snippets/like_section.html', context, request=request)
        return JsonResponse({'form': html})


def favorite_lick(request):
    lick = get_object_or_404(Lick, id=request.POST.get('id'))
    is_faved = False
    if lick.favorite.filter(id=request.user.id).exists():
        lick.favorite.remove(request.user)
        request.user.profile.faved_licks.remove(lick)
        is_faved = False
    else:
        lick.favorite.add(request.user)
        request.user.profile.faved_licks.add(
            lick)  # add to faved licks in profile
        is_faved = True

    user_faved = request.user.profile.faved_licks.all()

    context = {}
    context['lick'] = lick
    context['is_faved'] = is_faved
    context['total_faves'] = lick.total_faves()
    context["user_faved"] = user_faved

    if request.is_ajax():
        html = render_to_string(
            'repo/snippets/favorite_section.html', context, request=request)
        return JsonResponse({'form': html})


def sanitize_instrument(i):
    i = re.sub(r'[^A-Za-z0-9\s()]+', '', i).strip().lower()
    return(i)


@login_required
def create_lick(request):
    form = LickForm(request.POST or None)
    if request.method == "POST":
        form = LickForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            form_data = request.POST.copy()
            obj.author = request.user
            obj.save()
            form.save_m2m()
            messages.success(
                request, f'Lick {obj.id} created successfully.')

            # 5 or whatever index of 'other' instrument
            if form_data.get('instrument') == '5':
                # get other instrument from 'other' form field, sanitize input
                other_inst = sanitize_instrument(form_data.get('other'))
                # sanitize input

                # create new instrument if it does not exist yet
                all_instr = Instrument.objects.all().values_list('name', flat=True)
                if not other_inst in all_instr:
                    Instrument.objects.create(name=other_inst)

                # get new instument instance and assign to lick, then save
                obj.instrument = Instrument.objects.get(name=other_inst)
                obj.save(update_fields=['instrument'])

    context = {
        "form": form,
    }
    return render(request, 'repo/lick_form.html', context)


class LickCreateView(SuccessMessageMixin, LoginRequiredMixin, generic.CreateView):
    model = Lick
    form_class = LickForm
    success_url = reverse_lazy('lick-create')
    success_message = 'Lick has been created successfully, you may upload another one!'
    template_name = 'repo/lick_form.html'

    def form_valid(self, form):
        """
        if Lick.objects.filter(author=self.request.user).count() == 0:
            form.instance.counter = 1
        else:
            form.instance.counter = Lick.objects.filter(author=self.request.user).order_by(
                '-date_posted').first().counter + 1  # Lick number for each author
        """
        form.instance.author = self.request.user

        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class LickUpdateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Lick
    form_class = LickForm
    template_name = 'repo/lick_edit.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.success_url = self.request.POST.get('previous_page')
        return super().form_valid(form)

    def test_func(self):
        lick = self.get_object()
        self.success_message = f'Lick {lick.id} has been successfully updated!'
        if self.request.user == lick.author:
            return True
        return False


def delete_lick(request, pk):
    lick = get_object_or_404(Lick, pk=pk)
    messages.success(request, f'Lick {lick.id} deleted!')
    lick.delete()
    # redirect to previous url
    prev_url = request.GET.get('prev_url', "")
    if prev_url:
        prev_url = prev_url.replace("@", "&")
    else:
        prev_url = 'my-licks'
    return redirect(prev_url)
