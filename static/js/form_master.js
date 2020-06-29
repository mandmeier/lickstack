var selectedList = document.querySelectorAll(".selected")
var optionsContainer = document.querySelector(".options-container")
var optionsList = optionsContainer.querySelectorAll(".option")


// update chord seq upon change of chords
function updateChordSeq(){
    let chord_seq = "x"
    for (let chord of selectedList) {
        chord_seq = chord_seq + chord.dataset["value"] + "x"
    }
    document.getElementById("id_chord_seq").value = chord_seq
}



optionsList.forEach(o => {
    o.addEventListener("click", () => {
        optionsContainer.previousSibling.innerHTML = o.querySelector("label").innerHTML;
        optionsContainer.style.display = 'none';
        // add value to data field
        optionsContainer.previousSibling.dataset["value"] = o.querySelector("input").getAttribute("id")
        updateChordSeq()
    })
})


for (let i = 0; i < selectedList.length; i++) {

    selectedList[i].addEventListener("click", () => {
         //remove options
        optionsContainer.parentNode.removeChild(optionsContainer);
        //add beneath  current field
        selectedList[i].parentNode.insertBefore(optionsContainer, selectedList[i].nextSibling);
        optionsContainer.style.display = 'block';
        //optionsContainerList[i].classList.toggle("active");
    })

}


$('body').click(function(evt){
        console.log(evt.target)
        if(evt.target.className == "form-chords-row")
            return;
        if($(evt.target).closest('.form-chords-row').length)
            return;
        optionsContainer.style.display = 'none';
});



// // hide chord seq field
// const chord_seq_field = document.getElementById("chord_seq_field");
// chord_seq_field.style.display = "none";

//// reset chords button
const reset_chords_btn = document.getElementById("reset_chords")

reset_chords_btn.addEventListener("click", function(){
    for (let chord of selectedList) {
        chord.dataset["value"] = "."
        chord.innerHTML = "&nbsp;&nbsp;&#45;"
    };
    updateChordSeq();
})

// Time Signature Controls
function changeLayout() {
    if (document.getElementById("id_time_signature_1").checked){
        $(".4th").show();
        $(".form-chords-row .chord-select-box").css("width","11.5%");
    } else if (document.getElementById("id_time_signature_2").checked){
        $(".4th").hide();
        $(".form-chords-row .chord-select-box").css("width","15.33%");
        $(".4th").each(function( index ) {
            $(this).find('.selected').attr('data-value', '.')
            $(this).find('.selected').html('&nbsp;&nbsp;&#45;');
        });
    }
    updateChordSeq();
};

time_sign_input = document.getElementById('time-signature')
time_sign_input.addEventListener("change", function(){
 changeLayout();
});

