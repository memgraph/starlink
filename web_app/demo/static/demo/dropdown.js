function createDropdowns() {
    firstDropdown = document.getElementById("dropdownOne");
    secondDropdown = document.getElementById("dropdownTwo");

    for(city of cities){
        let element = document.createElement("option");
        element.text = city[3];
        element.value = city[0];
        firstDropdown.appendChild(element);
    }

    for(city of cities){
        let element = document.createElement("option");
        element.text = city[3];
        element.value = city[0];
        secondDropdown.appendChild(element);
    }

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
    focusView();
    drawCities();
}

function dropdownTwoSelect() {
    var secondSelected = secondDropdown.options[secondDropdown.selectedIndex];
    if (removedItemDropdownOne != null) {
        firstDropdown.add(removedItemDropdownOne);
    }
    firstDropdown.options[findElement(firstDropdown.options, secondSelected.value)].remove();
    removedItemDropdownOne = secondSelected.cloneNode(true);
    focusView();
    drawCities();
}

function GetSelectionValue() {
    var firstSelected = firstDropdown.options[firstDropdown.selectedIndex].value;
    var secondSelected = secondDropdown.options[secondDropdown.selectedIndex].value;

    return [firstSelected, secondSelected];
}

function GetSelectionText() {
    var firstSelected = firstDropdown.options[firstDropdown.selectedIndex].text;
    var secondSelected = secondDropdown.options[secondDropdown.selectedIndex].text;

    return [firstSelected, secondSelected];
}