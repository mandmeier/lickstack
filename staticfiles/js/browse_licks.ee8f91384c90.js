

//// Instrument Choice
var suggested_instruments = suggested_instruments_original.slice()

const suggestedInstrumentContainer = document.getElementById('#suggested-instr-container');
const instrumentContainer = document.getElementById('instr-container');
const instrumentsInput = document.getElementById('instr-container-input');
const hiddenInstrumentsInput = document.getElementById('instr_seq') // hidden input
hiddenInstrumentsInput.required = false;
hiddenInstrumentsInput.type = "hidden"

var instruments = [];

function createTag(label, close="") {
    const div = document.createElement('div');
    div.setAttribute('class', 'tag');
    const span = document.createElement('span');
    span.innerHTML = label;
    span.setAttribute('data-item', label);
    div.appendChild(span);
    if (close){
        const closeBtn = document.createElement('span');
        closeBtn.setAttribute('class', 'icon icon-close-solid');
        closeBtn.setAttribute('data-item', label);
        div.appendChild(closeBtn);
    }
    return div;
}


function updateInstruments(){
    // remove all instruments (reset)
    document.querySelectorAll('#instr-section .tag').forEach(function(tag){
        tag.parentElement.removeChild(tag);
    });

    // update selected instruments
    instruments.slice().reverse().forEach(function(tag){
        instrumentContainer.prepend(createTag(tag, close="Yes"));
    });

    // update suggested instruments
    suggested_instruments.forEach(function(tag){
        suggestedInstrumentContainer.appendChild(createTag(tag, close=""));
    });
    // update hidden tag field
    hiddenInstrumentsInput.value = instruments.join(",")
}

updateInstruments()


// input instruments
function sanitizeKey(key){
    key = key.replace(/^#+/g, '');
    key = key.replace(/^\s+/g, '');
    key = key.replace(/\s+$/g, '');
    key = key.replace(/\s+/g, '_');
    key = key.toLowerCase();
    return key;
}



function addInstrument(instrument){
    instrument = sanitizeKey(instrument);
    if (instruments.indexOf(instrument) < 0) {
        instruments.push(instrument);
        let st_index = suggested_instruments.indexOf(instrument)
        if (st_index >= 0){
                suggested_instruments.splice(st_index,1);
        }
    }
    updateInstruments();
    instrumentsInput.value = '';
}


instrumentsInput.addEventListener('keyup', function(e){
    let instrument = instrumentsInput.value
    if (e.key == 'Enter' && instrument != ""){
        addInstrument(instrument)
    }
});


// delete tag from input list
instrumentContainer.addEventListener('click', function(e){
    if (e.target.tagName == 'SPAN'){
        let instrument = e.target.getAttribute('data-item');
        if (suggested_instruments_original.indexOf(instrument) >= 0 && suggested_instruments.indexOf(instrument) < 0){
            suggested_instruments.push(instrument);
        }
        let t_index = instruments.indexOf(instrument);
        instruments.splice(t_index,1);
        updateInstruments();
    }
});

// select tag from suggested list
suggestedInstrumentContainer.addEventListener('click', function(e){
    if (e.target.tagName == 'SPAN'){
        let instrument = e.target.innerHTML;
        instruments.push(instrument);
        let st_index = suggested_instruments.indexOf(instrument);
        suggested_instruments.splice(st_index,1);
        updateInstruments();
    }
});


//// Keyword chice

const suggested_keywords_original = ["jazz", "ballad", "swing", "bebop", "waltz", "latin", "bossa", "salsa", "montuno", "funk", "country", "rock", "metal", "scales", "blues", "gospel", "spiritual", "turnaround", "even_eights", "shuffle"];
var suggested_keywords = suggested_keywords_original.slice()

const suggestedKeywordContainer = document.getElementById('#suggested-keyword-container');
const keywordContainer = document.getElementById('keyword-container');
const keywordsInput = document.getElementById('keyword-container-input');
const hiddenKeywordsInput = document.getElementById('id_tags') // hidden input
hiddenKeywordsInput.required = false;
hiddenKeywordsInput.type = "hidden"

var keywords = [];



function updateKeywords(){
    // remove all keywords (reset)
    document.querySelectorAll('#keyword-section .tag').forEach(function(tag){
        tag.parentElement.removeChild(tag);
    });

    // update selected keywords
    keywords.slice().reverse().forEach(function(tag){
        keywordContainer.prepend(createTag(tag, close="Yes"));
    });

    // update suggested keywords
    suggested_keywords.forEach(function(tag){
        suggestedKeywordContainer.appendChild(createTag(tag, close=""));
    });
    // update hidden tag field
    hiddenKeywordsInput.value = keywords.join(",")
}

updateKeywords()


// input keywords



function addKeyword(keyword){
    keyword = sanitizeKey(keyword);
    if (keywords.indexOf(keyword) < 0) {
        keywords.push(keyword);
        let st_index = suggested_keywords.indexOf(keyword)
        if (st_index >= 0){
                suggested_keywords.splice(st_index,1);
        }
    }
    updateKeywords();
    keywordsInput.value = '';
}



keywordsInput.addEventListener('keyup', function(e){
    let keyword = keywordsInput.value
    if (e.key == 'Enter' && keyword != ""){
        addKeyword(keyword);
    }
});


// delete tag from input list
keywordContainer.addEventListener('click', function(e){
    if (e.target.tagName == 'SPAN'){
        let keyword = e.target.getAttribute('data-item');
        if (suggested_keywords_original.indexOf(keyword) >= 0 && suggested_keywords.indexOf(keyword) < 0){
            suggested_keywords.push(keyword);
        }
        let t_index = keywords.indexOf(keyword);
        keywords.splice(t_index,1);
        updateKeywords();
    }
});

// select tag from suggested list
suggestedKeywordContainer.addEventListener('click', function(e){
    if (e.target.tagName == 'SPAN'){
        let keyword = e.target.innerHTML;
        keywords.push(keyword);
        let st_index = suggested_keywords.indexOf(keyword);
        suggested_keywords.splice(st_index,1);
        updateKeywords();
    }
});






//// store form data in cookies



var today = new Date();
var expiry = new Date(today.getTime() + 1 * 24 * 60 * 60 * 1000); // plus 1 day

function setCookie(name, value){
    document.cookie=name + "=" + escape(value) + "; path=/; expires=" + expiry.toGMTString();
}

function getCookie(name){
    var re = new RegExp(name + "=([^;]+)");
    var value = re.exec(document.cookie);
    return (value != null) ? unescape(value[1]) : null;
}

const form = document.forms[0]

// store form values in cookies



var isChrome = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);
if (isChrome == false && getCookie("isChrome") != 'notified'){
    setCookie('isChrome', 'notified');
    alert("Hi there, the LickStack is under development and currently not optimized for your browser. For best experience I recommend using Google Chrome. Thanks!");
}




function storeSearchFormValues(form){
    // remember chords
    // for (let i = 0; i < 16; i++){
    //     let chord = 'chord_'+(i+1).toString()
    //     setCookie('s_'+chord, form.elements[chord].value);
    // }

    if (form.elements['id_time_signature_2'].checked){
        setCookie("s_ts", "34");
    } else {
        setCookie("s_ts", "44");
    }

    if (form.elements['include_transposed'].checked) {
        setCookie("s_include_transposed", "checked");
    } else {
        setCookie("s_include_transposed", "unchecked");
    }

    if (form.elements['ignore_extensions'].checked) {
        setCookie("s_ignore_extensions", "checked");
    } else {
        setCookie("s_ignore_extensions", "unchecked");
    }

    if (form.elements['exact_search'].checked) {
        setCookie("s_exact_search", "checked");
    } else {
        setCookie("s_exact_search", "unchecked");
    }

    if (form.elements['must_contain'].checked) {
        setCookie("s_must_contain", "checked");
    } else {
        setCookie("s_must_contain", "unchecked");
    }

    setCookie("s_username_contains", form.elements['username_contains'].value)
    setCookie("s_lick_id", form.elements['lick_id'].value)

    setCookie("s_time_signature", form.elements['time_signature'].value)


    // remember tags
    setCookie("s_instruments", instruments);
    setCookie("s_keywords", keywords);

}


function getSearchFormValues(){
    // for (let i = 0; i < 16; i++){
    //     let chord = 'chord_'+(i+1).toString()
    //     if (getCookie('s_'+chord) == null){
    //         form.elements[chord].value = '.';
    //     } else {
    //         form.elements[chord].value = getCookie('s_'+chord);
    //     }
    // }

    if (getCookie("s_ts") == '34'){
        form.elements['id_time_signature_2'].checked = true;
    } else {
        form.elements['id_time_signature_1'].checked = true;
    }
    changeLayout()


    if (getCookie("s_include_transposed") == 'checked') {
        form.elements['include_transposed'].checked = true;
    } else {
        form.elements['include_transposed'].checked = false;
    }

    if (getCookie("s_ignore_extensions") == 'checked') {
        form.elements['ignore_extensions'].checked = true;
    } else {
        form.elements['ignore_extensions'].checked = false;
    }

    if (getCookie("s_exact_search") == 'checked') {
        form.elements['exact_search'].checked = true;
    } else {
        form.elements['exact_search'].checked = false;
    }

    if (getCookie("s_must_contain") == 'checked') {
        form.elements['must_contain'].checked = true;
    } else {
        form.elements['must_contain'].checked = false;
    }

    form.elements['username_contains'].value = getCookie("s_username_contains");
    form.elements['lick_id'].value = getCookie("s_lick_id");


    if (getCookie("s_time_signature") == null){
        form.elements['time_signature'].value = '';
    } else {
        form.elements['time_signature'].value = getCookie("s_time_signature");
    }


    if (getCookie("s_instruments") != null){
        getCookie("s_instruments").split(',').forEach(instrument => addInstrument(instrument));
    }

    if (getCookie("s_keywords") != null){
        getCookie("s_keywords").split(',').forEach(keyword => addKeyword(keyword));
    }



}

getSearchFormValues()


