from django import template

register = template.Library()


@register.filter
def chord_seq_T(chord_seq, chord_seq_query="test"):
    return(f'query: {chord_seq_query}, chords: {chord_seq} made with templatetags!')

### goal: calculate value that the T dropdown field should be (to be used by JS for displaying chords and transposing)

### input chord seq and chord query

### find out where query chord seq matches chord seq, pick first chords of that sequence to calculate difference

### Find difference between query and seq.

### query G, seq F -> difference +2 or -10 (pick whichever is smaller in abs to find nearest)
### query G, seq C -> difference +7 or -5  (pick whichever is smaller in abs)
