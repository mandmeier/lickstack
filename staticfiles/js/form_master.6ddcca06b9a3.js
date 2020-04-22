const chord_select = document.getElementsByClassName("chord-select");

var counter = 1
for (let chord of chord_select) {
    chord.id = "chord_"+counter.toString()
    counter += 1

}

// hide chord seq field
const chord_seq_field = document.getElementById("chord_seq_field");
chord_seq_field.style.display = "none";

// update chord seq upon change of chords
function updateChordSeq(){
    let chord_seq = "x"
    for (let chord of chord_select) {
        chord_seq = chord_seq + chord.value + "x"
    }
    document.getElementById("id_chord_seq").value = chord_seq
}

document.querySelectorAll('.chord-select').forEach(item => {
    item.addEventListener("change", function(){
        updateChordSeq();
    });
})

//// reset chords button
const reset_chords_btn = document.getElementById("reset_chords")

reset_chords_btn.addEventListener("click", function(){
    for (let chord of chord_select) {
        chord.value = "."
    };
    updateChordSeq();
})

// Time Signature Controls
function changeLayout() {
    if (document.getElementById("id_time_signature_1").checked){
        $("#chord_4").show();
        $("#chord_8").show();
        $("#chord_12").show();
        $("#chord_16").show();
        $(".form-chords-row .chord-select").css("width","11.5%");
    } else if (document.getElementById("id_time_signature_2").checked){
        $("#chord_4").hide();
        $("#chord_8").hide();
        $("#chord_12").hide();
        $("#chord_16").hide();
        $(".form-chords-row .chord-select").css("width","15.33%");
        $("#chord_4, #chord_8, #chord_12, #chord_16").css("width","0px");
        document.getElementById("chord_4").value = ".";
        document.getElementById("chord_8").value = ".";
        document.getElementById("chord_12").value = ".";
        document.getElementById("chord_16").value = ".";
    }
    updateChordSeq();
};

time_sign_input = document.getElementById('time-signature')
time_sign_input.addEventListener("change", function(){
 changeLayout();
});

