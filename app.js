let zipCodeTB = document.getElementById("zipCodeTB")
let submitButton = document.getElementById("submitButton")
let resultsContainer = document.getElementById("resultsContainer")

async function fetchZone(zip) {

    let response = await fetch(`https://phzmapi.org/${zip}.json`);
    console.log(zip);
    let zoneResults = await response.json();
    
    return zoneResults;
}

submitButton.addEventListener("click", async () => {
    //code to call fetchZone and display results will go in here
    let zipCode = zipCodeTB.value

    const zipCodeRegex = /^\d{5}$/

    //if the test returns true it will run the original functions
    if (zipCodeRegex.test(zipCode)) {

        let result = await fetchZone(zipCode)

    let zone = `<div class=”zoneDisplay”>
        <h2> Your Growing Zone </h2>
        <span>Zone: ${result.zone}</span>
        <span>Temp Range: ${result.temperature_range}</span>
        <span>Lat: ${result.coordinates.lat}</span>
        <span>Lon: ${result.coordinates.lon}</span>
        </div>`

        resultsContainer.innerHTML = zone
        zipCodeTB.value = " "

    //else if the test returns false it will populate a message into the results container for the user
    } else {
        resultsContainer.innerHTML = "Please enter a valid zip code"
        zipCodeTB.value = " "
  }})