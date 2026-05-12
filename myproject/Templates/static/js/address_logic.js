const addressData = {
    "Gujarat": {
        "Ahmedabad": {
            "City": { "Ahmedabad City": "380001", "Maninagar": "380008" },
            "Daskroi": { "Bakrol": "382430", "Bareja": "382425" }
        },
        "Gandhinagar": {
            "Gandhinagar": { "Sector 1": "382001", "Sector 10": "382010" },
            "Kalol": { "Adalaj": "382421", "Kalol City": "382721" }
        },
        "Gir Somnath": {
            "Veraval": { "Veraval City": "362265", "Prabhas Patan": "362268", "Adri": "362266" },
            "Talala": { "Talala City": "362150", "Sasan Gir": "362135", "Borvav": "362150" },
            "Sutrapada": { "Sutrapada City": "362275", "Dhamlej": "362275" },
            "Kodinar": { "Kodinar City": "362720", "Chhara": "362720" },
            "Una": { "Una City": "362560", "Delvada": "362510" },
            "Gir Gadhada": { "Gir Gadhada City": "362530", "Dhokadva": "362530" }
        }
    },
    "Maharashtra": {
        "Mumbai": {
            "Mumbai City": { "Colaba": "400005", "Dadar": "400014" },
            "Mumbai Suburban": { "Andheri": "400053", "Bandra": "400050" }
        },
        "Pune": {
            "Pune City": { "Shivajinagar": "411005", "Kothrud": "411038" },
            "Haveli": { "Hadapsar": "411028", "Loni Kalbhor": "412201" }
        }
    }
};

document.addEventListener('DOMContentLoaded', function() {
    // Basic Controls
    const stateSelect = document.getElementById('state');
    const addressTypeSelect = document.getElementById('address_type');
    
    // UI Panels
    const cityFieldsPanel = document.getElementById('city_fields');
    const villageFieldsPanel = document.getElementById('village_fields');

    // Village Path Fields
    const districtSelect = document.getElementById('district');
    const talukaSelect = document.getElementById('taluka');
    const villageSelect = document.getElementById('village');
    const villagePincode = document.getElementById('village_pincode');

    // Labels & Warnings
    const stateWarning = document.getElementById('state-warning');
    const typeLabel = document.getElementById('type-label');
    const districtWarning = document.getElementById('district-warning');
    const talukaLabel = document.getElementById('taluka-label');
    const talukaWarning = document.getElementById('taluka-warning');
    const villageLabel = document.getElementById('village-label');

    function resetSelect(select, placeholder, disable = true) {
        if (select) {
            select.innerHTML = `<option value="">-- ${placeholder} --</option>`;
            select.disabled = disable;
        }
    }

    // Initialize States
    for (let state in addressData) {
        let option = document.createElement('option');
        option.value = state;
        option.textContent = state;
        stateSelect.appendChild(option);
    }

    // 1. State -> Address Type
    stateSelect.addEventListener('change', function() {
        if (this.value) {
            addressTypeSelect.disabled = false;
            stateWarning.style.display = 'none';
            typeLabel.style.display = 'block';
        } else {
            addressTypeSelect.disabled = true;
            addressTypeSelect.value = '';
            stateWarning.style.display = 'block';
            typeLabel.style.display = 'none';
            togglePath('');
        }
    });

    // 2. Address Type -> Path Selection
    addressTypeSelect.addEventListener('change', function() {
        togglePath(this.value);
    });

    function togglePath(type) {
        if (type === 'City') {
            cityFieldsPanel.style.display = 'block';
            villageFieldsPanel.style.display = 'none';
        } else if (type === 'Village') {
            cityFieldsPanel.style.display = 'none';
            villageFieldsPanel.style.display = 'block';
            
            // Reset Village sequence
            resetSelect(districtSelect, 'Select District', false);
            let districts = addressData[stateSelect.value];
            for (let d in districts) {
                let opt = document.createElement('option');
                opt.value = d; opt.textContent = d;
                districtSelect.appendChild(opt);
            }
            
            // Initial Village Path state: Labels hidden, Warnings shown
            districtWarning.style.display = 'block';
            talukaLabel.style.display = 'none';
            talukaWarning.style.display = 'block';
            villageLabel.style.display = 'none';
        } else {
            cityFieldsPanel.style.display = 'none';
            villageFieldsPanel.style.display = 'none';
        }
    }

    // --- VILLAGE PATH LOGIC ---
    districtSelect.addEventListener('change', function() {
        resetSelect(talukaSelect, 'Select Taluka', !this.value);
        
        if (this.value) {
            districtWarning.style.display = 'none';
            talukaLabel.style.display = 'block';
            
            let talukas = addressData[stateSelect.value][this.value];
            for (let t in talukas) {
                let opt = document.createElement('option');
                opt.value = t; opt.textContent = t;
                talukaSelect.appendChild(opt);
            }
        } else {
            districtWarning.style.display = 'block';
            talukaLabel.style.display = 'none';
        }
    });

    talukaSelect.addEventListener('change', function() {
        resetSelect(villageSelect, 'Select Village', !this.value);
        
        if (this.value) {
            talukaWarning.style.display = 'none';
            villageLabel.style.display = 'block';
            
            let villages = addressData[stateSelect.value][districtSelect.value][this.value];
            for (let v in villages) {
                let opt = document.createElement('option');
                opt.value = v; opt.textContent = v;
                villageSelect.appendChild(opt);
            }
        } else {
            talukaWarning.style.display = 'block';
            villageLabel.style.display = 'none';
        }
    });

    villageSelect.addEventListener('change', function() {
        if (this.value) {
            villagePincode.value = addressData[stateSelect.value][districtSelect.value][talukaSelect.value][this.value];
        } else {
            villagePincode.value = '';
        }
    });
});
