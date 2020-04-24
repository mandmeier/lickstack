//// Audio preview

//initial values
playButton = document.getElementById("play");
playButtonIcon = playButton.querySelector('span');
seekBar = document.getElementById("seekbar");
fillBar = seekBar.querySelector('.fill');
mouseDown = false;
preview = document.getElementById("preview");

//play button
playButton.addEventListener('click', function () {
    if (audio.paused) {
        audio.play();
    } else {
        audio.pause();
    }
});


function update_audio_controls() {

    preview.style.display = "none";

    audio.addEventListener('play', function () {
      playButtonIcon.className = 'icon icon-pause';
    });

    audio.addEventListener('pause', function () {
      playButtonIcon.className = 'icon icon-play';
    });

    audio.addEventListener('timeupdate', function () {
      if (mouseDown) return;
        let p = audio.currentTime / audio.duration;
        fillBar.style.width = p * 100 + "%";
    });

    seekBar.addEventListener('mousedown', function (e) {
      mouseDown = true;
      window.rect = e.target.getBoundingClientRect();
      let x = e.clientX - rect.left;
      let p = x / seekBar.clientWidth;
      fillBar.style.width = p * 100 + "%";
    });

    window.addEventListener('mousemove', function (e) {
      if (!mouseDown) return;
        let x = e.clientX - rect.left;
        let p = x / seekBar.clientWidth;
        fillBar.style.width = p * 100 + "%";
    });

    window.addEventListener('mouseup', function (e) {
      if (!mouseDown) return;
        mouseDown = false;
        let x = e.clientX - rect.left;
        let p = x / seekBar.clientWidth;
        fillBar.style.width = p * 100 + "%";
        audio.currentTime = p * audio.duration;
      if (!audio.paused) {
        audio.play();
      }
    });

};

function audio_reset(){
    if (typeof audio != 'undefined') {
        audio.pause();
        audio.currentTime = 0;
        playButtonIcon.className = 'ion-play';
    }
}

// get audio file src from input field
inpFile = document.getElementById("inpFile");
inpFileLabel = document.getElementById("inpFileLabel")
file_upload_error = document.getElementById("file_upload_error")


inpFile.addEventListener("change", function() {
    audio_reset();
    file = this.files[0];
    inpFileLabel.textContent=file.name;
    //file_upload_error.innerHTML = "Choose audio file of type .mp3 .m4a or .ogg. Max size 1 MB.";
    preview.style.display = "hidden";

    if (file == null) {
        inpFileLabel.textContent="Choose File";
        preview.style.display = "block";
    } else if (!(file.type.split("/")[0] == "audio")) {
        file_upload_error.innerHTML = "Wrong file type. Please use audio, preferably '.mp3', '.m4a' or '.ogg'.";
        preview.style.display = "block";
    } else if (file.size > 1048576) {
        file_upload_error.innerHTML = "File too large (limit 1 MB). Consider shortening audio.";
        preview.style.display = "block";
    } else {
        file_upload_error.innerHTML = "";
        reader = new FileReader();
        reader.addEventListener("load", function() {
            audio = new Audio(this.result);
            update_audio_controls();
        });
        reader.readAsDataURL(file);
    }
});


//// Instrument selection


// make selection "other"
const instr_select = document.getElementById("id_instrument")

//move "other" option to end
const instr_options = instr_select.getElementsByTagName("option")
// find element with "other" option
for (let i = 0; i < instr_options.length; i++) {
    if (instr_options[i].innerHTML == "other"){
        other_option = instr_options[i]
    }
}
//const other_option = instr_select.querySelectorAll('[value="5"]')[0];
instr_select.removeChild(other_option);
instr_select.appendChild(other_option);
selected_instr = instr_options[instr_select.selectedIndex].innerHTML

// hide initial other field
window.addEventListener('load', function () {
    if(!(selected_instr == "other")){
        jQuery('#other').hide();
    }
})

// toggle "please specify" field
jQuery('#id_instrument').on('change', function() {
    var options = this.getElementsByTagName("option");
    var optionHTML = options[this.selectedIndex].innerHTML;
    selected_instr = instr_options[instr_select.selectedIndex].innerHTML
    if (optionHTML == 'other' ) {
        jQuery('#other').show();
    }
    else {
        jQuery('#other').hide();
    }
});



//// Tag controls
const suggested_tags_original = ["jazz", "ballad", "swing", "bebop",
"waltz", "latin", "bossa", "salsa",
"montuno", "funk", "country", "rock",
"metal", "scales", "blues", "gospel",
"spiritual", "turnaround", "even_eights", "shuffle",
"ending", "exercise"];
var suggested_tags = suggested_tags_original.slice()

const suggestedTagContainer = document.querySelector('.suggested-tag-container');
const tagContainer = document.querySelector('.tag-container');
const tagsInput = document.querySelector('.tag-container input');
const hiddenTagsInput = document.getElementById('id_tags') // hidden input
hiddenTagsInput.type = "hidden"

var tags = [];

function createTag(label, close="") {
    const div = document.createElement('div');
    div.setAttribute('class', 'tag');
    const span = document.createElement('span');
    span.innerHTML = label;
    div.appendChild(span);
    if (close){
        const closeBtn = document.createElement('span');
        closeBtn.setAttribute('class', 'icon icon-close-solid');
        closeBtn.setAttribute('data-item', label);
        div.appendChild(closeBtn);
    }
    return div;
}



function updateTags(){

    // remove all tags (reset)
    document.querySelectorAll('.tag-section .tag').forEach(function(tag){
        tag.parentElement.removeChild(tag);
    });

    // update selected tags
    tags.slice().reverse().forEach(function(tag){
        tagContainer.prepend(createTag(tag, close="Yes"));
    });

    // update suggested tags
    suggested_tags.forEach(function(tag){
        suggestedTagContainer.appendChild(createTag(tag, close=""));
    });
    // update hidden tag field
    hiddenTagsInput.value = tags.join(",")
}

updateTags()


// input tags

function sanitizeKey(key){
    key = key.replace(/^#+/g, '');
    key = key.replace(/^\s+/g, '');
    key = key.replace(/\s+$/g, '');
    key = key.replace(/\s+/g, '_');
    key = key.toLowerCase();
    return key;
}




// add keyword

function add_kw(keyword){
        keyword = sanitizeKey(keyword);
        if (tags.indexOf(keyword) < 0) {
            tags.push(keyword);
            let st_index = suggested_tags.indexOf(keyword)
            if (st_index >= 0){
                    suggested_tags.splice(st_index,1);
            }
        }
        updateTags();
        tagsInput.value = '';
}


tagsInput.addEventListener('keyup', function(e){
    let keyword = tagsInput.value
    if (e.key == 'Enter' && keyword != ""){
        add_kw(keyword);
    }
});




// delete tag from input list
tagContainer.addEventListener('click', function(e){
    if (e.target.tagName == 'svg'){
        let keyword = e.target.getAttribute('data-item');
        if (suggested_tags_original.indexOf(keyword) >= 0 && suggested_tags.indexOf(keyword) < 0){
            suggested_tags.push(keyword);
        }
        let t_index = tags.indexOf(keyword);
        tags.splice(t_index,1);
        updateTags();
    }
});


// select tag from suggested list
suggestedTagContainer.addEventListener('click', function(e){
    if (e.target.tagName == 'SPAN'){
        let keyword = e.target.innerHTML;
        tags.push(keyword);
        let st_index = suggested_tags.indexOf(keyword);
        suggested_tags.splice(st_index,1);
        updateTags();
    }
});





//// check form

const submit_btn = document.getElementById("submit");
const other_field = document.getElementById("id_other");

function checkForm(){
    let status_audio = "pass"
    let status_instrument = "pass"
    let status_chords = "pass"
    let status_keywords = "pass"
    let form_status = "fail"

    // check audio file
    if (typeof audio == 'undefined') {
        file_upload_error.innerHTML = "Please select an audio file."
        status_audio = "fail"
    } else {
        file_upload_error.innerHTML = ""
        status_audio = "pass"
    }

    // check if other instrument specified
    if (instr_select.value == ''){
        instrument_error.innerHTML = "Please specify an instrument."
        status_instrument = "fail"
    } else if (selected_instr == "other" && other_field.value == ""){
        instrument_error.innerHTML = "Please specify an instrument."
        status_instrument = "fail"
    } else {
        instrument_error.innerHTML = ""
        status_instrument = "pass"
    }


    // check chords
    if (document.getElementById("id_chord_seq").value == "x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x"){
        chords_error.innerHTML = "Please enter at least one chord."
        status_chords = "fail"
    } else {
        chords_error.innerHTML = ""
        status_chords = "pass"
    }

    if (tags.length == 0){
        keywords_error.innerHTML = "Please enter at least one keyword."
        status_keywords = "fail"
    } else {
        keywords_error.innerHTML = ""
        status_keywords = "pass"
    }

    // check if all fields correct
    if(status_audio == "pass" && status_instrument == "pass" && status_chords == "pass" && status_keywords == "pass"){
        form_status = "pass"
    }

    // submit form
    if (form_status == "pass"){
        submit_btn.click()
    }

}

