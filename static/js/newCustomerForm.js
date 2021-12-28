// To show or hide vehicle_type attributes
// Adapted logic from: https://stackoverflow.com/questions/44832785/show-hide-elements-based-on-a-selected-option-with-javascript
var el2 = document.getElementById("accountTypeFormControlSelect1");
el2.addEventListener("change", function() {
    var elems = document.querySelectorAll(
        ".individual, .business"
        )
    var buttons_ = document.querySelectorAll(
        ".find, .add"
        )
    for (var i = 0; i < elems.length; i++) {
        elems[i].style.display = 'none'
    }
    if (this.selectedIndex === 1) {
        document.querySelector('.business').style.display = 'block';
    } else if (this.selectedIndex === 2) {
        document.querySelector('.individual').style.display = 'block';
    }
}, false);
