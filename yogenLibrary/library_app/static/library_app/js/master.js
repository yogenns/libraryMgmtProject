function myFunction(elementName) {
    selectedLabel = document.getElementsByName(elementName)[0].selectedOptions[0].label
    console.log(selectedLabel);
    document.getElementsByName("1-author_name")[0].value = selectedLabel
}

$("#table tr").click(function () {
    console.log("Test")
    document.getElementById('selectedRows').value = $(this).id;
    console.log("Sel Id " + $(this).id);
});