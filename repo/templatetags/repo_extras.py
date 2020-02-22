from django import template

register = template.Library()


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


@register.filter
def chord_seq_T(chord_seq, chord_seq_query="test"):
    query = chord_seq_query
    chords = chord_seq
    # if query transposed find interval to adjust written chords and sound
    # for t in [0, 1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 6]:
    for t in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
        tr = transpose_seq(chords, t)
        if bool(re.search(query, tr)):
            return(t)


@register.simple_tag
def url_replace(request, field, value):

    dict_ = request.GET.copy()

    dict_[field] = value

    return dict_.urlencode()
