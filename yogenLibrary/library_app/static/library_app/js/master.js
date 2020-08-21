function myFunction(elementName) {
    selectedLabel = document.getElementsByName(elementName)[0].selectedOptions[0].label
    console.log(selectedLabel);
    document.getElementsByName("1-author_name")[0].value = selectedLabel
}