console.log("Ancestor Tree Loaded");

document.addEventListener("DOMContentLoaded", function(){
    const form = document.getElementById("familyForm");
    const personalForm = document.getElementById("personalInfoForm");
    const popup = document.getElementById("popup");
    const checkbox = document.getElementById("sameAsContact");

    /* ================= FORM SUBMIT ================= */
    if(form && popup){
        form.addEventListener("submit", function(event){
            // If you want to use the popup instead of standard redirect, keep this.
            // But currently views.py redirects with success=true.
            // console.log("Form submitted");
        });
    }

    /* ================= CLOSE POPUP ================= */
    window.closePopup = function(){
        if(popup){
            popup.style.display = "none";
        }
    }

    /* ================= SAME AS ABOVE ================= */
    if(checkbox){
        checkbox.addEventListener("change", function(){
            const contactNumber = document.getElementById("contact_number_1").value;
            const whatsappInput = document.getElementById("whatsapp_number");

            if(this.checked){
                whatsappInput.value = contactNumber;
            }else{
                whatsappInput.value = "";
            }
        });
    }

    /* ================= PREVENT ENTER SUBMIT ================= */
    [form, personalForm].forEach(f => {
        if(f){
            f.addEventListener("keypress", function(e){
                if(e.key === "Enter" && e.target.tagName !== "TEXTAREA"){
                    e.preventDefault();
                }
            });
        }
    });
});
