const addressData = {
    "Gujarat": {
        "Ahmedabad": {
            "City": {
                "Ahmedabad City": "380001",
                "Maninagar": "380008"
            },
            "Daskroi": {
                "Bakrol": "382430",
                "Bareja": "382425"
            }
        },
        "Gandhinagar": {
            "Gandhinagar": {
                "Sector 1": "382001",
                "Sector 10": "382010"
            },
            "Kalol": {
                "Adalaj": "382421",
                "Kalol City": "382721"
            }
        },
        "Gir Somnath": {
            "Veraval": {
                "Veraval City": "362265",
                "Prabhas Patan": "362268",
                "Adri": "362266"
            },
            "Talala": {
                "Talala City": "362150",
                "Sasan Gir": "362135",
                "Borvav": "362150"
            },
            "Sutrapada": {
                "Sutrapada City": "362275",
                "Dhamlej": "362275"
            },
            "Kodinar": {
                "Kodinar City": "362720",
                "Chhara": "362720"
            },
            "Una": {
                "Una City": "362560",
                "Delvada": "362510"
            },
            "Gir Gadhada": {
                "Gir Gadhada City": "362530",
                "Dhokadva": "362530"
            }
        }
    },
    "Maharashtra": {
        "Mumbai": {
            "Mumbai City": {
                "Colaba": "400005",
                "Dadar": "400014"
            },
            "Mumbai Suburban": {
                "Andheri": "400053",
                "Bandra": "400050"
            }
        },
        "Pune": {
            "Pune City": {
                "Shivajinagar": "411005",
                "Kothrud": "411038"
            },
            "Haveli": {
                "Hadapsar": "411028",
                "Loni Kalbhor": "412201"
            }
        }
    }
};

document.addEventListener('DOMContentLoaded', function() {
    const stateSelect = document.getElementById('state');
    const districtSelect = document.getElementById('district');
    const talukaSelect = document.getElementById('taluka');
    const villageSelect = document.getElementById('village');
    const pincodeInput = document.getElementById('pincode');

    // Populate States
    for (let state in addressData) {
        let option = document.createElement('option');
        option.value = state;
        option.textContent = state;
        stateSelect.appendChild(option);
    }

    stateSelect.addEventListener('change', function() {
        districtSelect.innerHTML = '<option value="">-- Select District --</option>';
        talukaSelect.innerHTML = '<option value="">-- Select Taluka --</option>';
        villageSelect.innerHTML = '<option value="">-- Select Village --</option>';
        pincodeInput.value = '';

        if (this.value) {
            let districts = addressData[this.value];
            for (let district in districts) {
                let option = document.createElement('option');
                option.value = district;
                option.textContent = district;
                districtSelect.appendChild(option);
            }
        }
    });

    districtSelect.addEventListener('change', function() {
        talukaSelect.innerHTML = '<option value="">-- Select Taluka --</option>';
        villageSelect.innerHTML = '<option value="">-- Select Village --</option>';
        pincodeInput.value = '';

        if (this.value) {
            let talukas = addressData[stateSelect.value][this.value];
            for (let taluka in talukas) {
                let option = document.createElement('option');
                option.value = taluka;
                option.textContent = taluka;
                talukaSelect.appendChild(option);
            }
        }
    });

    talukaSelect.addEventListener('change', function() {
        villageSelect.innerHTML = '<option value="">-- Select Village --</option>';
        pincodeInput.value = '';

        if (this.value) {
            let villages = addressData[stateSelect.value][districtSelect.value][this.value];
            for (let village in villages) {
                let option = document.createElement('option');
                option.value = village;
                option.textContent = village;
                villageSelect.appendChild(option);
            }
        }
    });

    villageSelect.addEventListener('change', function() {
        if (this.value) {
            let pincode = addressData[stateSelect.value][districtSelect.value][talukaSelect.value][this.value];
            pincodeInput.value = pincode;
        } else {
            pincodeInput.value = '';
        }
    });
});
