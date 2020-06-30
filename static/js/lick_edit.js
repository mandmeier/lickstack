// remember previous page in hidden input field
prev = document.getElementById("previous_page");
prev.value = document.referrer;

delete_btn = document.getElementById("delete_btn");
url = delete_btn.href.split("/?")[0]
new_url = url + "/?prev_url=" + document.referrer;
delete_btn.href = new_url.replace(/&/g, "@")


// populate chords
const chds = document.getElementById("id_chord_seq").value.split('x').slice(1,17)
populateChords(chds);

// populate keywords with data from context
const kws = kw_string.split(',')
kws.forEach(item => add_kw(item));
