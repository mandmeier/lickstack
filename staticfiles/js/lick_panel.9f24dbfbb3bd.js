

const licks = document.getElementsByClassName('lick')
var mouseDown = false;
var liked_licks = [1,4]


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



/// define lick object

function Lick(lick_dat, i){

    this.id = lick_dat.id
    this.time_signature = lick_dat.time_signature

    this.panel = licks[i]
    this.chords = lick_dat.chord_seq_search.split('x').slice(1,17);
    this.chord_imgs = this.panel.getElementsByClassName('chord-img')

    // audio player controls
    this.play_btn = this.panel.getElementsByClassName('play')[0]
    this.play_btn_icon = this.play_btn.querySelector('span')
    this.seekBar = this.panel.getElementsByClassName('seek-bar')[0]
    this.fillBar = this.panel.getElementsByClassName('fill')[0]
    this.audio_url = lick_dat.audio_url
    this.playback_rate = 1;



    // transpose controls
    this.slowdown_btn = this.panel.getElementsByClassName('slowdown-btn')[0]
    this.transpose_btn = this.panel.getElementsByClassName('transpose-btn')[0]

    if (lick_dat.transpose_by == undefined){
        this.transpose_by = 0;
    } else {
        this.transpose_by = lick_dat.transpose_by; // get from search form or album
    }

    this.transpose_rules = lick_dat.transpose_rule.split(',')


    this.like_btn = this.panel.getElementsByClassName('like-btn')[0]
    this.fav_btn = this.panel.getElementsByClassName('fav-btn')[0]


    this.reset_other_players = function(){
        for (let i = 0; i < lick_objects.length; i++) {
                let lick = lick_objects[i]
                if (lick != this && lick.audio != undefined){
                    lick.audio.pause();
                    lick.audio.currentTime = 0;
                    lick.player.stop(0);
                }
            }
    }





    this.set_audio_controls = function() {
        this.play_btn_icon.className = 'icon icon-spinner8';
        this.player = new Tone.Player(this.audio_url);
        this.audio = new Audio(this.audio_url);
        this.player.toDestination();
        this.audio.volume = 0;
        //transposePlayer(i);


        this.audio.addEventListener('play', function () {
          lck.play_btn_icon.className = 'icon icon-pause';
        });

        this.audio.addEventListener('pause', function () {
          lck.play_btn_icon.className = 'icon icon-play';
        });

        this.audio.addEventListener('timeupdate', function () {
          if (mouseDown) return;
            let p = lck.audio.currentTime / lck.audio.duration;
            let x =
            lck.fillBar.style.width = p * 100 + "%";
        });

        this.seekBar.addEventListener('mousedown', function (e) {
          mouseDown = true;
          window.rect = e.target.getBoundingClientRect();
          let x = e.clientX - rect.left;
          let p = x / lck.seekBar.clientWidth;
          lck.fillBar.style.width = p * 100 + "%";
        });

        this.panel.addEventListener('mousemove', function (e) {
          if (!mouseDown) return;
            let x = e.clientX - rect.left;
            let p = x / lck.seekBar.clientWidth;
            lck.fillBar.style.width = p * 100 + "%";
        });

        this.panel.addEventListener('mouseup', function (e) {
          if (!mouseDown) return;
            mouseDown = false;
            let x = e.clientX - rect.left;
            let p = x / lck.seekBar.clientWidth;
            lck.fillBar.style.width = p * 100 + "%";
            lck.audio.currentTime = p * lck.audio.duration;
            ofs = lck.audio.currentTime;

          if (!lck.audio.paused) {
            lck.player.start();
            lck.player.seek(offset = ofs);
          }
        });

        this.playWhenLoaded()

    }


    this.playWhenLoaded = function(){
        if(lck.player.buffer.loaded){
            lck.start_player();
        } else {
            setTimeout(lck.playWhenLoaded, 200);
        }
    }


    this.start_player = function(){
        if (this.pitch_shift == undefined) {
            this.transpose();
        }
        if (this.audio.paused) {
            this.reset_other_players();
            this.audio.play();
            ofs = this.audio.currentTime;
            this.player.start();
            this.player.seek(offset = ofs);
        } else {
            this.audio.pause();
            this.player.stop(0);
        }
    }

    this.play = function(){
        if (this.player == undefined) {
            this.set_audio_controls();
        }
        else {
            this.start_player();
        }

    }


    var lck = this;

    this.play_btn.addEventListener('click', function(){
        lck.play();
    });


    this.make_34 = function(){
        if(this.time_signature == "34"){
            this.chord_imgs[3].style.display = "none"
            this.chord_imgs[7].style.display = "none"
            this.chord_imgs[11].style.display = "none"
            this.chord_imgs[15].style.display = "none"
            let sep34 = Array.prototype.slice.call(this.panel.getElementsByClassName('separator-34'));
            sep34.forEach( function(element){ element.style.width = '2.9%'; });
            let seplr = Array.prototype.slice.call(this.panel.getElementsByClassName('separator-lr'));
            seplr.forEach( function(element){ element.style.width = '5%'; });
            let sepmid = Array.prototype.slice.call(this.panel.getElementsByClassName('separator-mid'));
            sepmid.forEach( function(element){ element.style.width = '8.8%'; });
        }
    }


    this.draw_chords = function(){

        for (let i = 0; i < 16; i++) {

            if (this.chords[i] == '.') {
                this.chord_imgs[i].innerHTML = "&nbsp;&nbsp;&#45;"
            } else {
                let chord_transposed = transposeChord(this.chords[i], this.transpose_by + instr_transpose_shift)
                this.chord_imgs[i].name = chord_transposed
                this.chord_imgs[i].innerHTML = toMuseJazz(chord_transposed, this.transpose_rules)
            }
        }
        this.transpose_btn.value = this.transpose_by;
    }


    this.transpose_btn.addEventListener('change', function () {
        lck.transpose();
    });


    this.slowdown_btn.addEventListener('click', function () {
        lck.slowdown();
    });


    // slow down audio button
    this.slowdown = function() {
        if (this.playback_rate == 1) {
            this.slowdown_btn.src = tortoise_on_url; // change icon to toggled version
            this.playback_rate =0.5;
        } else {
            this.slowdown_btn.src=tortoise_off_url; // change icon to default version
            this.playback_rate = 1;
        }
        this.transpose();
    }



    this.transpose = function() {

        // transpose chord symbols
        this.transpose_by = Number(this.transpose_btn.value)
        this.draw_chords()


        // transpose audio
        if (this.player != undefined){
            this.player.playbackRate = this.playback_rate;
            this.audio.playbackRate = this.playback_rate;
            this.player.toDestination();

            // delete old pitch shift to prevent memory leak
            if (this.pitch_shift != null) {
                this.pitch_shift.disconnect();
            }
            delete this.pitch_shift


            if (this.playback_rate == 1){
                this.pitch_shift = new Tone.PitchShift({
                pitch: this.transpose_by.toString()
                }).toDestination();
            } else { //if playbackrate == 0.5 add +12 to pitch to correct
                trans = this.transpose_by + 12
                trans = trans.toString()
                this.pitch_shift = new Tone.PitchShift({
                pitch: trans
              }).toDestination();
            }
            // disconnect old player (get overlay of two players otherwise)
            this.player.disconnect();
            this.player.connect(this.pitch_shift);
        }
    }


    // mark liked and fav
    if (user_liked.includes(String(this.id))){
        this.like_btn.getElementsByClassName('icon')[0].className = "icon icon-thumbs-up"
    }
    if (user_faved.includes(String(this.id))){
        this.fav_btn.getElementsByClassName('icon')[0].className = "icon icon-star"
    }


}

// get JSON data
var lick_data = JSON.parse(lck_json.replace(/&quot;/g,'"'));

// create lick objects
var lick_objects = []
for (let i = 0; i < lick_data.length; i++) {
 lick_objects.push(new Lick(lick_data[i], i));
 lick_objects[i].make_34();
 lick_objects[i].draw_chords();
}




