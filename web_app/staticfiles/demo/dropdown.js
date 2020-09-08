function createDropdowns() {
    document.getElementById("startStopButton").disabled = true;
    firstDropdown = document.getElementById("dropdownOne");
    secondDropdown = document.getElementById("dropdownTwo");
    /*
        let elementOne = document.createElement("option");
        elementOne.text = "Start city"
        firstDropdown.appendChild(elementOne);

        let elementTwo = document.createElement("option");
        elementTwo.text = "Target city"
        secondDropdown.appendChild(elementTwo);
    */
    for (city of cities) {
        let element = document.createElement("option");
        element.text = city[3];
        element.value = city[0];
        firstDropdown.appendChild(element);
    }

    for (city of cities) {
        let element = document.createElement("option");
        element.text = city[3];
        element.value = city[0];
        secondDropdown.appendChild(element);
    }

    /*
    firstDropdown.selectedIndex = 0;
    secondDropdown.selectedIndex = 1;

    var firstSelected = firstDropdown.options[firstDropdown.selectedIndex];
    var secondSelected = secondDropdown.options[secondDropdown.selectedIndex];

    firstDropdown.options[findElement(firstDropdown.options, secondSelected.value)].remove();
    secondDropdown.options[findElement(secondDropdown.options, firstSelected.value)].remove();

    removedItemDropdownOne = secondSelected.cloneNode(true);
    removedItemDropdownTwo = firstSelected.cloneNode(true);
    */
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

    dropdownOneSelected = true;
    if (dropdownTwoSelected) {
        document.getElementById("startStopButton").disabled = false;
        drawCities();
        focusView();
    } else {
        drawCity(firstSelected.value);
    }
}

function dropdownTwoSelect() {
    var secondSelected = secondDropdown.options[secondDropdown.selectedIndex];
    if (removedItemDropdownOne != null) {
        firstDropdown.add(removedItemDropdownOne);
    }
    firstDropdown.options[findElement(firstDropdown.options, secondSelected.value)].remove();
    removedItemDropdownOne = secondSelected.cloneNode(true);

    drawCity(secondSelected.value);

    dropdownTwoSelected = true;
    if (dropdownOneSelected) {
        document.getElementById("startStopButton").disabled = false;
        drawCities();
        focusView();
    } else {
        drawCity(secondSelected.value);
    }
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