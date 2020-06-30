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

function storeLickFormValues(form){

    // remember chord seq
    setCookie("f_chord_seq", form.elements["chord_seq"].value);


    // only remember instrument if it is not 'other'
    if (selected_instr != 'other'){
        setCookie("id_instrument", form.elements['id_instrument'].value);
    } else {
        setCookie("id_instrument", '');
    }
    // remember tags
    setCookie("tags", tags);

    // remember ts

    if (form.elements['id_time_signature_2'].checked){
        setCookie("newlick_ts", "34");
    } else {
        setCookie("newlick_ts", "44");
    }


}










function getLickFormValues(){


    // populate chords
    const chds = getCookie("f_chord_seq").split('x').slice(1,17)
    populateChords(chds)


    if (getCookie("id_instrument") == null){
        form.elements['id_instrument'].value = ""
        jQuery('#id_other')[0].value = "";
    } else {
        form.elements['id_instrument'].value = getCookie("id_instrument");
    }

    if (getCookie("tags") != null){
        getCookie("tags").split(',').forEach(keyword => add_kw(keyword));
    }

    if (getCookie("newlick_ts") == '34'){
        form.elements['id_time_signature_2'].checked = true;
    } else {
        form.elements['id_time_signature_1'].checked = true;
    }
    changeLayout()


}

getLickFormValues()
