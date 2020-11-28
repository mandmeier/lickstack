
# TODO

This section lists things to do, ordered by category and priority

## Bugfixes

### Safari Mobile: licks don't load, just endless load wheel spinning

### When manually typing keywords on mobile, there is no way to press "enter"
Maybe confirm with space after typing keyword?

### check uploaded files for audio filetype instead of just file extension
So that files for upload don't need extension



## New Features

### ability to create lick albums in "My Licks"
bundle up to 20(?) licks in album. Album will show licks in sequence in the selected key.
Show album on separate page so that the url to the album can be shared

### individual page for licks
so that the url to the lick can be shared
this could be the same as an album page, but just show one lick?

### option to add comments to licks for discussion
as dropdown underneath licks, like the info dropdown?

### option to sort licks by number of likes



## Performance/security improvements

### redo lick panel using JS object

### convert tone.js object into web audio
Currently, each lick downloads each audio file twice, once for Tone.js and once for web audio. Not ideal.
Try converting tone.js object into web audio, or try building audio player exclusively with Tone.js.
load audio from amazon (only once) -> connect to tone.js (or find current time in tone.js)

### confirm email address upon signup

### check if an audio file is a duplicate, already uploaded
https://josephmosby.com/2015/05/13/preventing-file-dupes-in-django.html



# Ideas


This section lists and any ideas (however ridiculous and impossible) to make the LickStack more fun/useful/awesome


## New Features

### shoutbox on home page?
in an effort to create a feeling of a live community

### start developing app for phone

### develop easier way to enter chords
maybe multilevel dropdown? F > m7
Layout in circle of fifths would be slick

### create user profile page
Kinda like a social media user profile.
You can list what you do and link to any external pages.
"I'm a jazz piano teacher, find my videos here"
List your favorite licks / lick albums that show how awesome a musician you are
author name on lick panel is link to author profile

### if you marked a lick as a favorite, alert if new comment / likes since last login
email alert?

### display featured lick of the day on home page

### way to post alternative chords for your lick?

### support chords with custom base note e.g. G7/C, Eb7/G

### allow for custom beats per measure, e.g. 5/4, 2/4, 6/8

### sort licks by relevancy: calculate from date and likes

### find way to share functionong lick panel in email (with audio)

### find way to share functionong lick panel anywhere (with audio)
So that others can embed licks in their websites, like embedding a tweet or youtube video.
I think this is what an iframe is for.

### log in with facebook, google?

### on home page show panels and with jazz, blues, latin (most popular lick ctegories)
Also show number of licks in each category.
When you click on a panel you will be taken to list of licks with this tag

### report inappropriate content button: bad quality, chords don't match, not music, wrong instrument
