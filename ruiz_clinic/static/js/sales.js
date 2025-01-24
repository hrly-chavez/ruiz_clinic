document.addEventListener("DOMContentLoaded", () => {
    const filterDate = document.getElementById("filter-date");
    const earnings = document.getElementById("total-earnings");
    const productsSold = document.getElementById("products-sold");
    const productList = document.querySelector(".product-list"); // Updated selector for product list
    const patientBalanceList = document.getElementById("patient-balance-list");

    function fetchSalesData(date) {
        fetch(`/api/sales/?date=${date}`)
            .then(response => response.json())
            .then(data => {
                // Update total earnings and number of products sold
                earnings.textContent = `₱ ${data.sales_total}`;
                productsSold.textContent = data.products_sold_count;

                // Clear previous product items
                productList.innerHTML = "";

                if (data.products_sold.length === 0) {
                    productList.innerHTML = "<p>No products sold today.</p>";
                } else {
                    data.products_sold.forEach(product => {
                        const name = product.name || null; // Set null if value is missing
                        const category = product.category || null;
                        const brand = product.brand || null;
                        const qty = product.qty || 0; // Replace null with 0
                        const price = product.price || 0; // Replace null with 0

                        // Dynamically hide columns with null or "N/A"
                        const item = document.createElement("div");
                        item.classList.add("product-item");
                        item.innerHTML = `
                            ${name ? `<span>${name}</span>` : ""}
                            ${category ? `<span>${category}</span>` : ""}
                            ${brand ? `<span>${brand}</span>` : ""}
                            ${qty > 0 ? `<span>Qty: ${qty}</span>` : ""}
                            ${price > 0 ? `<span>₱ ${price}</span>` : ""}
                        `;
                        productList.appendChild(item);
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
