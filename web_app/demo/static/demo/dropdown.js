let firstDropdown;
let secondDropdown;

let removedItemDropdownOne;
let removedItemDropdownTwo;

let dropdownOneSelected = false;
let dropdownTwoSelected = false;

function createDropdowns() {
    document.getElementById("startStopButton").disabled = true;

    firstDropdown = document.getElementById("dropdownOne");
    secondDropdown = document.getElementById("dropdownTwo");

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

    $('#dropdownOne').select2({
        placeholder: "Start city"
    });

    $('#dropdownTwo').select2({
        placeholder: "Target city"
    });
}

function findElement(list, value) {
    for (let i = 0; i < list.length; i++) {
        if (list[i].value === value) {
            return i;
        }
    }
    return -1;
}

function dropdownOneSelect() {
    const firstSelected = firstDropdown.options[firstDropdown.selectedIndex];
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
    const secondSelected = secondDropdown.options[secondDropdown.selectedIndex];
    if (removedItemDropdownOne != null) {
        firstDropdown.add(removedItemDropdownOne);
    }
    firstDropdown.options[findElement(firstDropdown.options, secondSelected.value)].remove();
    removedItemDropdownOne = secondSelected.cloneNode(true);

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
    const firstSelected = firstDropdown.options[firstDropdown.selectedIndex].value;
    const secondSelected = secondDropdown.options[secondDropdown.selectedIndex].value;

    return [firstSelected, secondSelected];
}

function GetSelectionText() {
    const firstSelected = firstDropdown.options[firstDropdown.selectedIndex].text;
    const secondSelected = secondDropdown.options[secondDropdown.selectedIndex].text;

    return [firstSelected, secondSelected];
}