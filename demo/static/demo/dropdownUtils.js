function populateDropdowns() {
    for (var i = 0; i < cities.length; i++) {
        var element = document.createElement("option");
        element.text = cities[i][3];
        element.value = cities[i][0];
        firstDropdown.appendChild(element);
    }
    for (var i = 0; i < cities.length; i++) {
        var element = document.createElement("option");
        element.text = cities[i][3];
        element.value = cities[i][0];
        secondDropdown.appendChild(element);
    }
}

function initDropdowns() {
    firstDropdown.selectedIndex = 0;
    secondDropdown.selectedIndex = 1;

    var firstSelected = firstDropdown.options[firstDropdown.selectedIndex];
    var secondSelected = secondDropdown.options[secondDropdown.selectedIndex];

    firstDropdown.options[findElement(firstDropdown.options, secondSelected.value)].remove();
    secondDropdown.options[findElement(secondDropdown.options, firstSelected.value)].remove();

    removedItemDropdownOne = secondSelected.cloneNode(true);
    removedItemDropdownTwo = firstSelected.cloneNode(true);
}

function findElement(list, value) {
    for (var i = 0; i < list.length; i++) {
        if (list[i].value == value) {
            return i;
        }
    }
    return -1;
}

function dropdownOneSelect() {
    var firstSelected = firstDropdown.options[firstDropdown.selectedIndex];
    if (removedItemDropdownTwo != null) {
        secondDropdown.add(removedItemDropdownTwo);
    }
    secondDropdown.options[findElement(secondDropdown.options, firstSelected.value)].remove();
    removedItemDropdownTwo = firstSelected.cloneNode(true);

    drawCities();
}

function dropdownTwoSelect() {
    var secondSelected = secondDropdown.options[secondDropdown.selectedIndex];
    if (removedItemDropdownOne != null) {
        firstDropdown.add(removedItemDropdownOne);
    }
    firstDropdown.options[findElement(firstDropdown.options, secondSelected.value)].remove();
    removedItemDropdownOne = secondSelected.cloneNode(true);

    drawCities();
}

function GetSelectionValue() {
    var firstSelected = firstDropdown.options[firstDropdown.selectedIndex].value;
    var secondSelected = secondDropdown.options[secondDropdown.selectedIndex].value;

    return [firstSelected, secondSelected];
}