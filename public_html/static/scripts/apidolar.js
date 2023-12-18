function fetchData(url, customName) {
    return fetch(url)
        .then(response => response.json())
        .then(data => {
            const nombre = customName; 
            const venta = data.venta;

            return { nombre, venta };
        });
}


function fetchAndPopulateData() {
    const tableBody = document.getElementById("dataContainer");


    const apiEndpoints = {
        "https://dolarapi.com/v1/dolares/solidario": "Dolar Solidario",
        "https://dolarapi.com/v1/dolares/oficial": "Dolar Oficial",
        "https://dolarapi.com/v1/dolares/blue": "Dolar Blue"
    };

    
    const fetchPromises = Object.entries(apiEndpoints).map(([url, customName]) =>
        fetchData(url, customName)
    );

   
    Promise.all(fetchPromises)
        .then(dataArray => {
            
            while (tableBody.firstChild) {
                tableBody.removeChild(tableBody.firstChild);
            }

           
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
          
            console.error("Error fetching data:", error);
        });
}


fetchAndPopulateData();

setInterval(fetchAndPopulateData, 3000);
