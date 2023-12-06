// Function to fetch data from a single endpoint
function fetchData(url, customName) {
    return fetch(url)
        .then(response => response.json())
        .then(data => {
            const nombre = customName; // Use the custom name
            const venta = data.venta;

            return { nombre, venta };
        });
}

// Function to fetch data from all endpoints and populate the table
function fetchAndPopulateData() {
    const tableBody = document.getElementById("dataContainer");

    // Define a mapping of API endpoints to custom names
    const apiEndpoints = {
        "https://dolarapi.com/v1/dolares/solidario": "Dolar Solidario",
        "https://dolarapi.com/v1/dolares/oficial": "Dolar Oficial",
        "https://dolarapi.com/v1/dolares/blue": "Dolar Blue"
    };

    // Create an array of promises to fetch data from all endpoints concurrently
    const fetchPromises = Object.entries(apiEndpoints).map(([url, customName]) =>
        fetchData(url, customName)
    );

    // Use Promise.all to wait for all promises to resolve
    Promise.all(fetchPromises)
        .then(dataArray => {
            // Clear existing data in the table body
            while (tableBody.firstChild) {
                tableBody.removeChild(tableBody.firstChild);
            }

            // Populate the table with the fetched data
            dataArray.forEach(({ nombre, venta }) => {
                const row = document.createElement("tr");
                const nombreCell = document.createElement("td");
                const ventaCell = document.createElement("td");

                nombreCell.innerText = nombre;
                ventaCell.innerText = venta;

                row.appendChild(nombreCell);
                row.appendChild(ventaCell);

                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            // Handle errors if any of the fetch requests fails
            console.error("Error fetching data:", error);
        });
}

// Call the fetchAndPopulateData function initially
fetchAndPopulateData();

// Set up a 5-second interval to refresh data periodically
setInterval(fetchAndPopulateData, 3000); // 3000 milliseconds = 3 seconds
