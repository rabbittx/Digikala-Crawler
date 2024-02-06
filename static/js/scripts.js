
function validateForm() {
    var dbPath = document.forms["settingsForm"]["dbPath"].value;
    var gekoPath = document.forms["settingsForm"]["gekoPath"].value;

    if (dbPath == "" || dbPath == null) {
        alert("DB Path must be filled out");
        return false; 
    }
    if (gekoPath == "" || gekoPath == null) {
        alert("gekoPath must be filled out");
        return false; 
    }

    return true;
}


function showHelpPopup() {
    document.getElementById('helpPopup').style.display = 'block';
}

function hideHelpPopup() {
    document.getElementById('helpPopup').style.display = 'none';
}

