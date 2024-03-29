from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q, Count, Case, When
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from repo.models import Lick, Instrument
from blog.models import Article
from operator import attrgetter
from django.views import generic
from .forms import LickForm
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from itertools import cycle
import re
import json
from django.core.serializers.json import DjangoJSONEncoder



def get_chord_seq_search(chord_seq):
    sharps = ['C#', 'D#', 'F#', 'G#', 'A#']
    flats = ['Db', 'Eb', 'Gb', 'Ab', 'Bb']
    for s, f in zip(sharps, flats):
        chord_seq = chord_seq.replace(s, f)
    return chord_seq


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


def chord_seq_T(chord_seq, chord_seq_query="test"):
    # calculates interval between the lick and query from search form
    # transpose lick t half steps up to match chords in query
    query = chord_seq_query
    chords = chord_seq
    for t in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
        tr = transpose_seq(chords, t)
        if bool(re.search(query, tr)):
            return(t)


def is_valid_queryparam(param):
    return param != '' and param is not None


def get_liked_licks(request, licks):
    if request.user.is_authenticated:
        # find if user liked any of those licks
        user_liked = []
        for lick in licks:
            if lick in request.user.profile.liked_licks.all():
                user_liked.append(lick)
    else:
        user_liked = []

    return(user_liked)


def get_faved_licks(request, licks):
    if request.user.is_authenticated:
        # find if user faved any of those licks
        user_faved = []
        for lick in licks:
            if lick in request.user.profile.faved_licks.all():
                user_faved.append(lick)
    else:
        user_faved = []

    return(user_faved)



def home(request):

    licks = Lick.objects.all().order_by('-id')[:10]

    today = timezone.now().date()
    articles = Article.objects.all().order_by('pk').filter(
        draft=False).filter(date_published__lte=today)

    latest_articles = articles.order_by('-date_published')

    featured_articles = latest_articles.filter(id__in=(8, 5, 1))


    lick_info = licks.values(
        'id',
        'chord_seq_search',
        'time_signature',
        'transpose_rule',
    )

    lick_info = list(lick_info)

    # add audio filenames to lick info dict
    audio_urls = [lick.file.url for lick in licks]

    for i in range(0, len(lick_info)):
        lick_info[i]['audio_url'] = audio_urls[i]


    # convert to json
    licks_json = json.dumps(lick_info, cls=DjangoJSONEncoder)

    context = {}
    context['title'] = 'Home'
    context['licks'] = licks
    context['user_liked'] = get_liked_licks(request, licks)
    context['user_faved'] = get_faved_licks(request, licks)
    context['latest_articles'] = latest_articles
    context['featured_articles'] = featured_articles
    context['licks_json'] = licks_json

    return render(request, 'repo/home.html', context)


def browse_licks_view(request):

    if request.user.is_authenticated:
        instr_transpose_shift = int(request.user.profile.instr_transpose_shift)
    else:
        instr_transpose_shift = 0
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

        chord_seq = get_chord_seq_search(
            request.GET.get('chord_seq', "")).split('x')[1:17]
        instrument_string = request.GET.get('instr_seq', "")
        keyword_string = request.GET.get('tags', "")
        must_contain_keyword = bool(request.GET.get('must_contain', ""))

        instrument_list = instrument_string.split(',')

        keyword_list = keyword_string.split(',')

        # make regex query seq
        def get_chord_seq_query(chord_seq, half_steps=0):

            half_steps = half_steps - instr_transpose_shift

            query = ""

            if chord_seq == ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']:
                return query

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
            Q(chord_seq_search__regex=chord_seq_query)
        )
    else:
        licks = licks.filter(
            Q(chord_seq_search__regex=chord_seq_queries_T[0]) |
            Q(chord_seq_search__regex=chord_seq_queries_T[1]) |
            Q(chord_seq_search__regex=chord_seq_queries_T[2]) |
            Q(chord_seq_search__regex=chord_seq_queries_T[3]) |
            Q(chord_seq_search__regex=chord_seq_queries_T[4]) |
            Q(chord_seq_search__regex=chord_seq_queries_T[5]) |
            Q(chord_seq_search__regex=chord_seq_queries_T[6]) |
            Q(chord_seq_search__regex=chord_seq_queries_T[7]) |
            Q(chord_seq_search__regex=chord_seq_queries_T[8]) |
            Q(chord_seq_search__regex=chord_seq_queries_T[9]) |
            Q(chord_seq_search__regex=chord_seq_queries_T[10]) |
            Q(chord_seq_search__regex=chord_seq_queries_T[11])
        )

    if lick_id_query > 0:
        licks = licks.filter(id=lick_id_query)

    licks = licks.distinct()

    for lick in licks:
        queryset.append(lick)




    licks = sorted(list(set(queryset)), key=attrgetter('date_posted'), reverse=True)

    # paginate
    paginator_number_pages = 10
    page = request.GET.get('page', 1)
    paginator = Paginator(licks, 10)
    licks = paginator.page(page)

    # find most common instruments
    instr_ordered = Lick.objects.values("instrument").annotate(
        count=Count('instrument')).order_by("-count")
    instr_ids = [sub['instrument'] for sub in instr_ordered]  # as list
    preserved = Case(*[When(pk=pk, then=pos)
                       for pos, pk in enumerate(instr_ids)])
    instr_qs = Instrument.objects.filter(pk__in=instr_ids).order_by(preserved)

    common_instr = []
    for instr in instr_qs:
        if str(instr) not in ['', ' ', 'other']:
            common_instr.append(str(instr))

    instr_selection = ','.join(common_instr)


    # lick data for js variables
    displayed_lick_ids = [lick.id for lick in licks]
    displayed_licks = Lick.objects.filter(pk__in=displayed_lick_ids).order_by('-id')

    lick_info = displayed_licks.values(
        'id',
        'chord_seq_search',
        'time_signature',
        'transpose_rule',
    )

    lick_info = list(lick_info)

    # add audio filenames to lick info dict
    audio_urls = [lick.file.url for lick in displayed_licks]
    transpose_bys = [chord_seq_T(lick.chord_seq_search,chord_seq_query) for lick in displayed_licks]

    print("TEST")
    print(lick_info)

    print("DISP_LICKS")
    print(displayed_licks)


    for i in range(0, len(lick_info)):
        lick_info[i]['audio_url'] = audio_urls[i]
        lick_info[i]['transpose_by'] = transpose_bys[i]


    # convert to json
    licks_json = json.dumps(lick_info, cls=DjangoJSONEncoder)


    # pass values to context
    context = {}
    context['form'] = LickForm()
    context['licks'] = licks
    context['instrument'] = Instrument.objects.all().order_by('name')
    context['chord_seq_query'] = chord_seq_query  # used for template tags
    context['user_liked'] = get_liked_licks(request, licks)
    context['user_faved'] = get_faved_licks(request, licks)
    context['instr_selection'] = instr_selection
    context['licks_json'] = licks_json


    return render(request, "repo/browse_licks.html", context)


@login_required
def my_licks_view(request):
    chord_seq_query = ""
    licks = Lick.objects.all()
    licks = licks.filter(author=request.user)  # get current user id
    display = "mylicks"

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
    paginator = Paginator(licks, 10)
    licks = paginator.page(page)

    # lick data for js variables
    displayed_lick_ids = [lick.id for lick in licks]
    displayed_licks = Lick.objects.filter(pk__in=displayed_lick_ids)

    lick_info = displayed_licks.values(
        'id',
        'chord_seq_search',
        'time_signature',
        'transpose_rule',
    )

    lick_info = list(lick_info)

    # add audio filenames to lick info dict
    audio_urls = [lick.file.url for lick in displayed_licks]

    for i in range(0, len(lick_info)):
        lick_info[i]['audio_url'] = audio_urls[i]


    # convert to json
    licks_json = json.dumps(lick_info, cls=DjangoJSONEncoder)

    context = {}
    context['licks'] = licks
    context['chord_seq_query'] = chord_seq_query  # used for template tags
    context['user_liked'] = get_liked_licks(request, licks)
    context['user_faved'] = get_faved_licks(request, licks)
    context['display'] = display
    context['licks_json'] = licks_json

    return render(request, "repo/my_licks.html", context)


@login_required
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

    print("TEST")
    print(request)
    print(request.is_ajax())

    if request.is_ajax():
        html = render_to_string(
            'repo/snippets/like_section.html', context, request=request)
        return JsonResponse({'form': html})


@login_required
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
    i = re.sub(r'[^A-Za-z0-9\s()]+', '', i)
    i = re.sub(r'^[\s]+', '', i)
    i = re.sub(r'[\s]+$', '', i)
    i = re.sub(r'[\s]+', '_', i).lower()
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

            # transpose 3 up for Eb instruments
            instr_transpose_shift = int(
                request.user.profile.instr_transpose_shift)
            chord_seq = transpose_seq(form_data.get(
                'chord_seq'), -instr_transpose_shift)
            obj.chord_seq = chord_seq

            obj.save()
            form.save_m2m()
            messages.success(
                request, f'Lick {obj.id} created successfully.')

            # if selected form value points to 'other' instrument
            if Instrument.objects.get(pk=form_data.get('instrument')).name == 'other':
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


@login_required
def update_lick(request):
    form = LickForm(request.POST or None)
    if request.method == "POST":
        form = LickForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            form_data = request.POST.copy()
            obj.author = request.user

            # transpose 3 up for Eb instruments
            instr_transpose_shift = int(
                request.user.profile.instr_transpose_shift)
            chord_seq = transpose_seq(form_data.get(
                'chord_seq'), -instr_transpose_shift)
            obj.chord_seq = chord_seq

            obj.save()
            form.save_m2m()
            messages.success(
                request, f'Lick {obj.id} updated successfully.')

            # if selected form value points to 'other' instrument
            if Instrument.objects.get(pk=form_data.get('instrument')).name == 'other':
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


class LickUpdateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Lick
    form_class = LickForm
    template_name = 'repo/lick_edit.html'
    context_object_name = 'lick'

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

    def get_context_data(self, **kwargs):
        lick = self.get_object()
        ctx = super(LickUpdateView, self).get_context_data(**kwargs)
        ctx['kw_string'] = ','.join(lick.tags.slugs())
        return ctx


@login_required
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


@staff_member_required
def lick_detail(request, pk):

    album = [1,4,7,32,41]

    licks = Lick.objects.filter(id__in=album).order_by('-id')

    # lick data for js variables
    lick_info = licks.values(
        'id',
        'chord_seq_search',
        'time_signature',
        'transpose_rule',
    )

    lick_info = list(lick_info)

    # add audio filenames to lick info dict
    audio_urls = [lick.file.url for lick in licks]
    for i in range(0, len(lick_info)):
        lick_info[i]['audio_url'] = audio_urls[i]

    # convert to json
    licks_json = json.dumps(lick_info, cls=DjangoJSONEncoder)

    context = {}
    context['licks'] = licks
    context['licks_json'] = licks_json
    context['pk'] = pk
    context['user_liked'] = ",".join([str(lick.id) for lick in get_liked_licks(request, licks)])
    context['user_faved'] = ",".join([str(lick.id) for lick in get_faved_licks(request, licks)])
    return render(request, 'repo/lick_detail.html', context)
