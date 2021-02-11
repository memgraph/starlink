let firstDropdown;
let secondDropdown;

let removedItemDropdownOneValue = -1;
let removedItemDropdownTwoValue = -1;
let removedItemDropdownOneText;
let removedItemDropdownTwoText;

let dropdownOneSelected = false;
let dropdownTwoSelected = false;

function createDropdowns() {
    document.getElementById("startStopButton").disabled = true;

    firstDropdown = document.getElementById("dropdownOne");
    secondDropdown = document.getElementById("dropdownTwo");

    for (let id in city_names) {
        let element = document.createElement("option");
        element.text = city_names[id];
        element.value = id;
        firstDropdown.appendChild(element);
    }

    for (let id in city_names) {
        let element = document.createElement("option");
        element.text = city_names[id];
        element.value = id;
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
    if (removedItemDropdownTwoValue !== -1) {
        $("#dropdownTwo").append(`<option value="${removedItemDropdownTwoValue}">${removedItemDropdownTwoText}</option>`);
    }
    //secondDropdown.options[findElement(secondDropdown.options, firstSelected.value)].remove();
    removedItemDropdownTwoValue = firstSelected.value;
    removedItemDropdownTwoText = firstSelected.text;
    $(`#dropdownTwo option[value=${firstSelected.value}]`).remove();

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
    if (removedItemDropdownOneValue !== -1) {
        $("#dropdownOne").append(`<option value="${removedItemDropdownOneValue}">${removedItemDropdownOneText}</option>`);
    }
    //firstDropdown.options[findElement(firstDropdown.options, secondSelected.value)].remove();
    $(`#dropdownOne option[value=${secondSelected.value}]`).remove();

    removedItemDropdownOneValue = secondSelected.value;
    removedItemDropdownOneText = secondSelected.text;

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