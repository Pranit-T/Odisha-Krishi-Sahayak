const translations = {
    en: {
        title: "Odisha Krishi Sahayak - Dashboard",
        appTitle: "Odisha Krishi Sahayak",
        appTagline: "Your Partner in Farming",
        settingsBtn: "English",
        cardTitle: "Farmer Details",
        firstNameLabel: "First Name",
        firstNamePlaceholder: "Enter your first name",
        middleNameLabel: "Middle Name",
        middleNamePlaceholder: "Enter your middle name",
        lastNameLabel: "Last Name",
        lastNamePlaceholder: "Enter your last name",
        mobileNoLabel: "Mobile Number",
        mobileNoPlaceholder: "Enter your 10-digit mobile number",
        emailLabel: "Email Address",
        emailPlaceholder: "Enter your email address",
        aadhaarNoLabel: "Aadhaar Number",
        aadhaarNoPlaceholder: "Enter your 12-digit Aadhaar number",
        addressLabel: "Address",
        addressPlaceholder: "Enter your full address",
        saveBtnText: "Save Details",
        footerText: "Odisha Krishi Sahayak - Empowering Farmers with Data-Driven Insights",
        alertSuccess: "Farmer details saved successfully!",
        alertError: "Please fill out all required fields.",
    },
    or: {
        title: "ଓଡ଼ିଶା କୃଷି ସହାୟକ - ଡାସବୋର୍ଡ",
        appTitle: "ଓଡ଼ିଶା କୃଷି ସହାୟକ",
        appTagline: "ଆପଣଙ୍କର କୃଷି ସାଥୀ",
        settingsBtn: "ଓଡ଼ିଆ",
        cardTitle: "ଚାଷୀଙ୍କ ବିବରଣୀ",
        firstNameLabel: "ପ୍ରଥମ ନାମ",
        firstNamePlaceholder: "ଆପଣଙ୍କର ପ୍ରଥମ ନାମ ପ୍ରବେଶ କରନ୍ତୁ",
        middleNameLabel: "ମଧ୍ୟ ନାମ",
        middleNamePlaceholder: "ଆପଣଙ୍କର ମଧ୍ୟ ନାମ ପ୍ରବେଶ କରନ୍ତୁ",
        lastNameLabel: "ଶେଷ ନାମ",
        lastNamePlaceholder: "ଆପଣଙ୍କର ଶେଷ ନାମ ପ୍ରବେଶ କରନ୍ତୁ",
        mobileNoLabel: "ମୋବାଇଲ୍ ନମ୍ବର",
        mobileNoPlaceholder: "ଆପଣଙ୍କର 10-ଅଙ୍କ ବିଶିଷ୍ଟ ମୋବାଇଲ୍ ନମ୍ବର ପ୍ରବେଶ କରନ୍ତୁ",
        emailLabel: "ଇମେଲ୍ ଠିକଣା",
        emailPlaceholder: "ଆପଣଙ୍କ ଇମେଲ୍ ଠିକଣା ପ୍ରବେଶ କରନ୍ତୁ",
        aadhaarNoLabel: "ଆଧାର ନମ୍ବର",
        aadhaarNoPlaceholder: "ଆପଣଙ୍କର 12-ଅଙ୍କ ବିଶିଷ୍ଟ ଆଧାର ନମ୍ବର ପ୍ରବେଶ କରନ୍ତୁ",
        addressLabel: "ଠିକଣା",
        addressPlaceholder: "ଆପଣଙ୍କର ପୂରା ଠିକଣା ପ୍ରବେଶ କରନ୍ତୁ",
        saveBtnText: "ବିବରଣୀ ସେଭ୍ କରନ୍ତୁ",
        footerText: "ଓଡ଼ିଶା କୃଷି ସହାୟକ - ତଥ୍ୟ-ଆଧାରିତ ଦୃଷ୍ଟିକୋଣ ସହିତ ଚାଷୀମାନଙ୍କୁ ସଶକ୍ତ କରିବା",
        alertSuccess: "ଚାଷୀଙ୍କ ବିବରଣୀ ସଫଳତାର ସହିତ ସେଭ୍ ହୋଇଗଲା!",
        alertError: "ଦୟାକରି ସମସ୍ତ ଆବଶ୍ୟକୀୟ ଫିଲ୍ଡ ଭରନ୍ତୁ।",
    }
};

let currentLang = 'en';

function updateUI(lang) {
    const t = translations[lang];
    document.title = t.title;
    document.getElementById('app-title').textContent = t.appTitle;
    document.getElementById('app-tagline').textContent = t.appTagline;
    document.getElementById('settings-btn-text').textContent = t.settingsBtn;
    document.getElementById('farmer-details-card').querySelector('.card-title').textContent = t.cardTitle;
    
    // Update labels and placeholders
    const updateInput = (id, labelText, placeholderText) => {
        const input = document.getElementById(id);
        if (input) {
            const label = input.closest('.input-group').querySelector('label');
            if (label) label.textContent = labelText;
            input.placeholder = placeholderText;
        }
    };

    updateInput('first-name', t.firstNameLabel, t.firstNamePlaceholder);
    updateInput('middle-name', t.middleNameLabel, t.middleNamePlaceholder);
    updateInput('last-name', t.lastNameLabel, t.lastNamePlaceholder);
    // Mobile number requires finding the label differently due to nested structure
    document.getElementById('mobile-no').closest('.input-group').querySelector('label').textContent = t.mobileNoLabel;
    document.getElementById('mobile-no').placeholder = t.mobileNoPlaceholder;

    updateInput('email', t.emailLabel, t.emailPlaceholder);
    updateInput('aadhaar-no', t.aadhaarNoLabel, t.aadhaarNoPlaceholder);
    updateInput('address', t.addressLabel, t.addressPlaceholder);

    document.getElementById('save-details-btn').querySelector('span').textContent = t.saveBtnText;
    document.getElementById('footer-text').textContent = t.footerText;

    // Update dropdown text (just in case they need to be refreshed)
    document.querySelector('[data-lang="en"] .lang-text').textContent = "English";
    document.querySelector('[data-lang="or"] .lang-text').textContent = "ଓଡ଼ିଆ (Odia)";
}

function showNotification(message, type = 'error') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type}`;
    notification.style.display = 'block';

    setTimeout(() => {
        notification.style.display = 'none';
    }, 5000);
}

// --- Language Toggle Logic ---

const settingsBtn = document.getElementById('settings-btn');
const languageDropdown = document.getElementById('language-dropdown');
const languageOptions = document.querySelectorAll('.language-option');

settingsBtn.addEventListener('click', function() {
    languageDropdown.style.display = languageDropdown.style.display === 'block' ? 'none' : 'block';
});

languageOptions.forEach(option => {
    option.addEventListener('click', function() {
        const lang = this.getAttribute('data-lang');
        
        languageOptions.forEach(opt => {
            opt.classList.remove('active');
            opt.querySelector('i').className = 'fas'; // Remove check icon
        });
        this.classList.add('active');
        this.querySelector('i').className = 'fas fa-check'; // Add check icon
        
        currentLang = lang;
        updateUI(currentLang);
        
        languageDropdown.style.display = 'none';
    });
});

document.addEventListener('click', function(event) {
    if (!settingsBtn.contains(event.target) && !languageDropdown.contains(event.target)) {
        languageDropdown.style.display = 'none';
    }
});

// --- Form Logic (Save Details) ---

document.getElementById('save-details-btn').addEventListener('click', function() {
    // Note: Only required fields are checked for this demo logic
    const firstName = document.getElementById('first-name').value;
    const lastName = document.getElementById('last-name').value;
    const mobileNo = document.getElementById('mobile-no').value;
    const aadhaarNo = document.getElementById('aadhaar-no').value;
    const address = document.getElementById('address').value;

    if (firstName && lastName && mobileNo && aadhaarNo && address) {
        // Here you would typically send data to a server
        showNotification(translations[currentLang].alertSuccess, 'success');
    } else {
        showNotification(translations[currentLang].alertError, 'error');
    }
});

// --- Initialization ---

document.addEventListener('DOMContentLoaded', () => {
    updateUI(currentLang);
});