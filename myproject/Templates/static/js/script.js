// <<<<<<< HEAD
console.log("Ancestor Tree Loaded");
// =======
const form = document.getElementById("familyForm");

const popup = document.getElementById("popup");

/* ================= FORM SUBMIT ================= */

if(form && popup){

    form.addEventListener("submit", function(event){

        event.preventDefault();

        popup.style.display = "flex";

    });

}

/* ================= CLOSE POPUP ================= */

function closePopup(){

    if(popup){

        popup.style.display = "none";

    }

}

/* ================= SAME AS ABOVE ================= */

document.addEventListener("DOMContentLoaded", function(){

    const checkbox = document.getElementById(
        "sameAsContact"
    );

    if(checkbox){

        checkbox.addEventListener("change", function(){

            const contactNumber = document.getElementById(
                "contact_number_1"
            ).value;

            const whatsappInput = document.getElementById(
                "whatsapp_number"
            );

            if(this.checked){

                whatsappInput.value = contactNumber;

            }else{

                whatsappInput.value = "";

            }

        });

    }

    /* ================= PREVENT ENTER SUBMIT ================= */

    const form = document.getElementById(
        "familyForm"
    );

    if(form){

        form.addEventListener("keypress", function(e){

            if(e.key === "Enter"){

                e.preventDefault();

            }

        });

    }

});
>>>>>>> 8ebdfc5afa92d8f6a7ab89cac4eec97ef5552f33
