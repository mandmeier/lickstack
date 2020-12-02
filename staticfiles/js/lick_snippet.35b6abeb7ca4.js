
function transposeChord(input,transpose_by) {
    element = input.match(/(_[a-gA-g]{1,2}_)/)[0]
    let tr = transpose_by + instr_transpose_shift
    if (tr >= 0) {
        var chds = ["_C_", "_Db_", "_D_", "_Eb_", "_E_", "_F_", "_Gb_", "_G_", "_Ab_", "_A_", "_Bb_", "_B_"]
    } else {
        var chds = ["_C_", "_B_", "_Bb_", "_A_", "_Ab_", "_G_", "_Gb_", "_F_", "_E_", "_Eb_", "_D_", "_Db_"]
    }
    var start = chds.indexOf(element)
    element_transposed =  chds[(start + Math.abs(tr)) % chds.length];
    return input.replace(/(_[a-gA-g]{1,2}_)/, element_transposed);
}


function transposePlayer(l){
    console.log(l)
    transpose_bys[l] = Number(licks[l].getElementsByClassName('transpose-btn')[0].value)
    playback_rates[l] = licks[l].getElementsByClassName('slowdown-btn')[0].value
    audios[l].playbackRate = playback_rates[l];
    players[l].playbackRate = playback_rates[l];
    players[l].toDestination();

    //reset all pitch shift nodes to clear memory
    for (let j = 0; j < pitch_shifts.length; j++) {
        if (pitch_shifts[j] != null) {
            pitch_shifts[j].disconnect();
        }
        delete pitch_shifts[j]
    }

    if (playback_rates[l] == 1){
        pitch_shifts[l] = new Tone.PitchShift({
        pitch: transpose_bys[l].toString()
        }).toDestination();
    } else { //if playbackrate == 0.5 add +12 to pitch to correct
        trans = transpose_bys[l] + 12
        trans = trans.toString()
        pitch_shifts[l] = new Tone.PitchShift({
        pitch: trans
      }).toDestination();
    }
    // disconnect old player (get overlay of two players otherwise)
    players[l].disconnect();
    players[l].connect(pitch_shifts[l]);
}


// var chdStr = '_Cb_m7';

// newStr = chdStr.replace(/b_/g, "&#9837;");

// function strReplace(regex, pattern){
//     var myStr = 'quick_brown_fox';
//     var newStr = myStr.replace(/_/g, "-");

//     // Insert modified string in paragraph
//     document.getElementById("myText").innerHTML = newStr;
// }


function toMuseJazz(chd, transpose_rule){
    var chd = chd.replace(/^_/g, "");
    chd = chd.replace(/maj7/g, "Maj");
     chd = chd.replace(/7/g, "&#57751;");
     chd = chd.replace(/6/g, "&#57750;");
    if (transpose_rule == "h") {
        chd = chd.replace(/Db_/g, "C&#9839;_");
        chd = chd.replace(/Eb_/g, "D&#9839;_");
        chd = chd.replace(/Gb_/g, "F&#9839;_");
        chd = chd.replace(/Ab_/g, "G&#9839;_");
        chd = chd.replace(/Bb_/g, "A&#9839;_");
    } else {
        chd = chd.replace(/b_/g, "&#9837;");
    }
    chd = chd.replace(/_/g, "");
    chd = chd.replace(/Maj/g, "&#57738;");
    chd = chd.replace(/dim/g, "&#57744;");
    chd = chd.replace(/sus4/g, "&#57741;");
    chd = chd.replace(/b5/g, "&#57736;&#57749;");
    return chd
}




function updateChords(l) {
    let lick = licks[l]
    let chords = lick.getElementsByClassName('chord_seq')[0].getAttribute("value").split('x').slice(1,17);
    let transpose_rules = lick.getElementsByClassName('transpose_rule')[0].getAttribute('value').split(',')
    let transpose = Number(lick.getElementsByClassName('transpose-btn')[0].value)
    let chord_imgs = lick.getElementsByClassName('chord-img')



    for (let i = 0; i < 16; i++) {

        if (chords[i] == '.') {
            chord_imgs[i].innerHTML = "&nbsp;&nbsp;&#45;"
        } else {
            let chord_transposed = transposeChord(chords[i], transpose)
            chord_imgs[i].name = chord_transposed
            chord_imgs[i].innerHTML = toMuseJazz(chord_transposed, transpose_rules[i])
        }
    }

    if (players[l] != undefined){
        transposePlayer(l);
    }

}


function make_ts34(lck){
    let chord_fields = lck.getElementsByClassName('chord-img')
    chord_fields[3].style.display = "none"
    chord_fields[7].style.display = "none"
    chord_fields[11].style.display = "none"
    chord_fields[15].style.display = "none"

    sep34 = Array.prototype.slice.call(lck.getElementsByClassName('separator-34'));
    sep34.forEach( function(element){ element.style.width = '2.9%'; });

    seplr = Array.prototype.slice.call(lck.getElementsByClassName('separator-lr'));
    seplr.forEach( function(element){ element.style.width = '5%'; });

    sepmid = Array.prototype.slice.call(lck.getElementsByClassName('separator-mid'));
    sepmid.forEach( function(element){ element.style.width = '8.8%'; });
}


// initialize variables and controls for all licks
const licks = document.getElementsByClassName('lick')
const lick_order = []

const play_btns = document.getElementsByClassName('play')
const slowdown_btns = document.getElementsByClassName('slowdown-btn')
const transpose_btns = document.getElementsByClassName('transpose-btn')

for (let i = 0; i < play_btns.length; i++) {

    // assign new lick_id (thus I can show the same lick several times in different keys)
    lick_id = i.toString()
    licks[i].id = lick_id
    lick_order.push(lick_id)
}

for (let i = 0; i < play_btns.length; i++) {

    lick_id = i.toString()

    let sld = 'slowdown(' + lick_id + ')'
    slowdown_btns[i].setAttribute('onclick', sld)

    let uch = 'updateChords("' + lick_id + '")'
    transpose_btns[i].setAttribute('onchange', uch)
}


const seekBars = document.getElementsByClassName('seek-bar')
const fillBars = document.getElementsByClassName('fill')
mouseDown = false;
players = []
audios = []
playButtonIcons = []
playback_rates = []
pitch_shifts = []


// set initial transpose values for blog posts (and albums?)
if (typeof(initial_transpose) != "undefined"){
    var transpose_bys = initial_transpose

    // make transpose_bys from tstr
    for (let i = 0; i < licks.length; i++) {
        transpose_btns[i].value = initial_transpose[i]
        updateChords(i)
    }
} else {
// for browse licks, my licks
    var transpose_bys = []
}



for (let i = 0; i < play_btns.length; i++) {

    // time signatures
    let time_signature = licks[i].getElementsByClassName('time_signature')[0].getAttribute('value');
    if (time_signature == 34){
        make_ts34(licks[i]);
    };

    playButtonIcons.push(play_btns[i].querySelector('span'));
    playback_rates.push(Number(licks[i].getElementsByClassName('slowdown-btn')[0].value))

    if (typeof(initial_transpose) != "undefined"){
        transpose_bys.push(licks[i].getElementsByClassName('transpose-btn')[0].value)
    }


    pitch_shifts.push(null)

    updateChords(lick_order[i]);
}

function play(i){
    if (pitch_shifts[i] == undefined) {
        transposePlayer(i);
    }
    if (audios[i].paused) {
        audios[i].play();
        ofs = audios[i].currentTime;
        players[i].start();
        players[i].seek(offset = ofs);
    } else {
        audios[i].pause();
        players[i].stop(0);
    }
}



for (let i = 0; i < play_btns.length; i++) {


    play_btns[i].addEventListener('click', function () {


        if (players[i] == undefined) {
            playButtonIcons[i].className = 'icon icon-spinner8';
            let audio_url = play_btns[i].id.split('[X]')[1]
            players[i] = new Tone.Player(audio_url);
            audios[i] = new Audio(audio_url);
            audios[i].volume = 0;
            transposePlayer(i);


            audios[i].addEventListener('play', function () {
              playButtonIcons[i].className = 'icon icon-pause';
              resetAudio(i);
            });

            audios[i].addEventListener('pause', function () {
              playButtonIcons[i].className = 'icon icon-play';
            });

            audios[i].addEventListener('timeupdate', function () {
              if (mouseDown) return;
                let p = audios[i].currentTime / audios[i].duration;
                let x =
                fillBars[i].style.width = p * 100 + "%";
            });

            seekBars[i].addEventListener('mousedown', function (e) {
              mouseDown = true;
              window.rect = e.target.getBoundingClientRect();
              let x = e.clientX - rect.left;
              let p = x / seekBars[i].clientWidth;
              fillBars[i].style.width = p * 100 + "%";
            });

            licks[i].addEventListener('mousemove', function (e) {
              if (!mouseDown) return;
                let x = e.clientX - rect.left;
                let p = x / seekBars[i].clientWidth;
                fillBars[i].style.width = p * 100 + "%";
            });

            licks[i].addEventListener('mouseup', function (e) {
              if (!mouseDown) return;
                mouseDown = false;
                let x = e.clientX - rect.left;
                let p = x / seekBars[i].clientWidth;
                fillBars[i].style.width = p * 100 + "%";
                audios[i].currentTime = p * audios[i].duration;
                ofs = audios[i].currentTime;

              if (!audios[i].paused) {
                players[i].start();
                players[i].seek(offset = ofs);
              }
            });


        }

        function playWhenLoaded(){
            if(players[i].buffer.loaded){
                play(i);
            }
            else{
                setTimeout(playWhenLoaded, 200);
            }
        }
        playWhenLoaded()

    });


}





// reset other licks
function resetAudio(num){
    for (let i = 0; i < play_btns.length; i++) {
        if (players[i] != undefined && num != i){
            audios[i].pause();
            audios[i].currentTime = 0;
            players[i].stop(0);
        }
    }
}

// slow down audio button
function slowdown(i) {
    //selected_tortoise = document.getElementById('slowdown_'+lick_id)
    selected_tortoise = slowdown_btns[i]

    if (selected_tortoise.value == "1") {
        selected_tortoise.src=tortoise_on_url; // change icon to toggled version
        selected_tortoise.value="0.5";
    } else {
        selected_tortoise.value="1";
        selected_tortoise.src=tortoise_off_url; // change icon to default version
        selected_tortoise.value="1";
    }
    transposePlayer(i);
}
