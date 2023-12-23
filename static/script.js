function addInputValue() {
    // Clone the template small decision and append it to the smallDecisions container
    var template = document.querySelector('.vectorValue');
    var clone = template.cloneNode(true);
    clone.querySelector('.weight').value = "";
    document.getElementById('inputVector').appendChild(clone);
}

function fillRandomWeights(){
    var vectorValues = document.querySelectorAll('.vectorValue')
    vectorValues.forEach( function (element){
        var weight = element.querySelector('.weight');
        if(weight.value==="") {
            weight.value = Math.floor(Math.random()*11)-5;
        }
    });
}

function runPerceptron() {
    // Collect data from the form
    var perceptronTitle = document.getElementById('perceptronTitle').value;
    var threshold = document.getElementById('threshold').value;
    var inputVector = [];

    var vectorValueElements = document.querySelectorAll('.vectorValue');
    var isnan = false;
    vectorValueElements.forEach(function (element) {
        var value = element.querySelector('.binaryValue').checked? 1 : 0;
        var weight = parseInt(element.querySelector('.weight').value);

        if(isNaN(value) || isNaN(weight)){
            alert("Enter values for weight");
            isnan = true;
            return;
        }

        inputVector.push({
            value: value,
            weight: weight
        });
    });
    if(isnan===true) return;

    // Make an AJAX request to the backend
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/run_perceptron", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 ){
            if( xhr.status === 200 ) {
                var response = JSON.parse(xhr.responseText);
                console.log(response.output);
                document.getElementById('perceptronOutput').innerText = 'Output: ' + response.output;
                document.getElementById('image').src = response.image_url;
                console.log(response.image_url)
            }
            else {
                alert("Unable to process the request, please check your input values");
            }
        }
    };

    // Send data as JSON to the backend
    xhr.send(JSON.stringify({ title: perceptronTitle, threshold: threshold, input: inputVector }));
}