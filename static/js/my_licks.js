//

const control_btns = document.getElementsByClassName("control-btn")



for (let btn of control_btns) {
    if (btn.value == display) {
        btn.style.background="#C00001"
        btn.style.color="#f9f9f9"
        if (display == "favorites") {
            let star = btn.querySelector("#mylicks-star")
            star.style.color="#f9f9f9"
            }
        }
    }

