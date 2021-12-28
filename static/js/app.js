// To toggle buttons for Find and Add Customer
// Adapted logic from: https://stackoverflow.com/questions/17621515/how-to-show-and-hide-input-fields-based-on-radio-button-selection
function hideElems(elems) {
    for (let i = 0; i < elems.length; i++) { 
        console.log(`hidding elements: ${elems[i]}`)
        elems[i].style.display = 'none';
    }
}

function displayElems(elems) {
    for (let i = 0; i < elems.length; i++) { 
        console.log(`displaying elements: ${elems[i]}`)
        elems[i].style.display = 'block';
    }
}

function buttonClassCheck() {
    if (document.getElementById('addButton').checked) {
        displayElems(document.getElementsByClassName('displayedWhenAddRadioSelected'));
        hideElems(document.getElementsByClassName('displayedWhenFindRadioSelected'));
    }
    else {
        displayElems(document.getElementsByClassName('displayedWhenFindRadioSelected'));
        hideElems(document.getElementsByClassName('displayedWhenAddRadioSelected'));
        hideElems(document.getElementsByClassName('hideWhenFindRadioSelected'));
        document.getElementById('accountTypeFormControlSelect1').getElementsByTagName('option')[0].selected = 'selected'
    } 
}