// To show or hide vehicle_type attributes
// Adapted logic from: https://stackoverflow.com/questions/44832785/show-hide-elements-based-on-a-selected-option-with-javascript
var el2 = document.getElementById("vehicleTypeFormControlSelect1");
el2.addEventListener("change", function() {
    var elems = document.querySelectorAll(
        ".SUV, .Convertible, .Car, .Truck, .Van"
        )
    for (var i = 0; i < elems.length; i++) {
        elems[i].style.display = 'none'
    }
    if (this.selectedIndex === 3) {
        document.querySelector('.SUV').style.display = 'block';
    } else if (this.selectedIndex === 2) {
        document.querySelector('.Convertible').style.display = 'block';
    } else if (this.selectedIndex === 1) {
        document.querySelector('.Car').style.display = 'block';
    } else if (this.selectedIndex === 4) {
        document.querySelector('.Truck').style.display = 'block';
    } else if (this.selectedIndex === 5) {
        document.querySelector('.Van').style.display = 'block';
    }
}, false);
