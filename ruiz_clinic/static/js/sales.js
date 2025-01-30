document.addEventListener("DOMContentLoaded", () => {
    const filterDate = document.getElementById("filter-date");
    const earnings = document.getElementById("total-earnings");
    const productsSold = document.getElementById("products-sold");
    const tableBody = document.getElementById("products-table-body"); // Table body for product sold
    const noProductsMessage = document.getElementById("no-products-message"); // Message for no products
    const patientBalanceList = document.getElementById("patient-balance-list");

    function fetchSalesData(date) {
        fetch(`/api/sales/?date=${date}`)
            .then(response => response.json())
            .then(data => {
                // Update total earnings and number of products sold
                earnings.textContent = `₱ ${data.sales_total}`;
                productsSold.textContent = data.products_sold_count;

                // Clear previous product rows
                tableBody.innerHTML = "";

                if (data.products_sold.length === 0) {
                    // Show fallback message if no products sold
                    noProductsMessage.style.display = "block";
                } else {
                    // Hide fallback message and populate table rows
                    noProductsMessage.style.display = "none";

                    data.products_sold.forEach(product => {
                        const row = document.createElement("tr");
                        row.innerHTML = `
                            <td>${product.category || "N/A"}</td>
                            <td>${product.brand || "N/A"}</td>
                            <td>${product.qty || 0}</td>
                            <td>₱ ${product.price || 0}</td>
                        `;
                        tableBody.appendChild(row);
                    });
                }
            })
            .catch(error => console.error("Error fetching sales data:", error));
    }

    function fetchPatientBalances() {
        fetch("/api/patient-balances/")
            .then(response => response.json())
            .then(data => {
                patientBalanceList.innerHTML = ""; // Clear previous entries
    
                if (data.balances.length === 0) {
                    patientBalanceList.innerHTML = `<p style="text-align: center;">No patient balance.</p>`;
                } else {
                    data.balances.forEach(balance => {
                        const item = document.createElement("div");
                        item.classList.add("balance-item");
                        item.innerHTML = `
                            <div class="patient-name">${balance.patient_name}</div>
                            <div class="balance-amount">₱ ${balance.previous_balance}</div>
                        `;
                        patientBalanceList.appendChild(item);
                    });
                }
            })
            .catch(error => console.error("Error fetching patient balances:", error));
    }

    // Event listener for date filter
    filterDate.addEventListener("change", () => {
        const selectedDate = filterDate.value;
        fetchSalesData(selectedDate);
    });

    // Load today's data on page load
    const today = new Date().toISOString().split("T")[0];
    filterDate.value = today;
    fetchSalesData(today); // Fetch sales data
    fetchPatientBalances(); // Fetch patient balances
});
