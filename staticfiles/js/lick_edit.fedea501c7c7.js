// remember previous page in hidden input field
prev = document.getElementById("previous_page");
prev.value = document.referrer;

delete_btn = document.getElementById("delete_btn");
url = delete_btn.href.split("/?")[0]
new_url = url + "/?prev_url=" + document.referrer;
delete_btn.href = new_url.replace(/&/g, "@")




function transposeChord(input, tr) {
    var sharp_regex = /(_[A-H]#_)/
    if (sharp_regex.test(input)) {
        if (tr >= 0) {
            var chdlst = ["_C_", "_C#_", "_D_", "_D#_", "_E_", "_F_", "_F#_", "_G_", "_G#_", "_A_", "_A#_", "_B_"]
        } else {
            var chdlst = ["_C_", "_B_", "_A#_", "_A_", "_G#_", "_G_", "_F#_", "_F_", "_E_", "_D#_", "_D_", "_C#_"]
        }
    } else {
        if (tr >= 0) {
            var chdlst = ["_C_", "_Db_", "_D_", "_Eb_", "_E_", "_F_", "_Gb_", "_G_", "_Ab_", "_A_", "_Bb_", "_B_"]
        } else {
            var chdlst = ["_C_", "_B_", "_Bb_", "_A_", "_Ab_", "_G_", "_Gb_", "_F_", "_E_", "_Eb_", "_D_", "_Db_"]
        }
    }
    element = input.match(/(_[a-hA-H#]{1,2}_)/)[0]
    var start = chdlst.indexOf(element)
    element_transposed =  chdlst[(start + Math.abs(tr)) % chdlst.length];
    return input.replace(/(_[a-hA-H#]{1,2}_)/, element_transposed);
}



function populateTsChords(chds){
    //transpose chords 2 up for Bb
    var ts_chds = []
    for (let i = 0; i < chds.length; i++) {
        if (chds[i] == "."){
            ts_chds[i] = "."
        } else {
            ts_chds[i] = transposeChord(chds[i], instr_transpose_shift)
        }
    }
    for (let i = 0; i < ts_chds.length; i++) {
        selectedList[i].dataset["value"] = ts_chds[i]

        if(ts_chds[i] == "."){
            selectedList[i].innerHTML = "&nbsp;&nbsp;&#45;"
        } else{
            search_str = "[for=" + ts_chds[i] + "]"
            search_str = search_str.replace(/#/g, '\\#')
            selectedList[i].innerHTML = optionsContainer.querySelectorAll(search_str)[0].innerHTML
        }

    }
}



// populate chords
const chds = document.getElementById("id_chord_seq").value.split('x').slice(1,17)
populateTsChords(chds);

// populate keywords with data from context
const kws = kw_string.split(',')
kws.forEach(item => add_kw(item));


function updateChordSeq(){
    let chord_seq = "x"
    for (let chord of selectedList) {
        if (chord.dataset["value"] == "."){
            update_chord = "."
        } else {
            update_chord = transposeChord(chord.dataset["value"], -instr_transpose_shift)
        }
        chord_seq = chord_seq + update_chord + "x"
    }
    document.getElementById("id_chord_seq").value = chord_seq
}
