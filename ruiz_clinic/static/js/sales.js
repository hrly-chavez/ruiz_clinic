document.addEventListener("DOMContentLoaded", () => {
    const filterDate = document.getElementById("filter-date");
    const earnings = document.getElementById("total-earnings");
    const productsSold = document.getElementById("products-sold");
    const productList = document.getElementById("product-list");
    const viewBalanceBtn = document.getElementById("view-patient-balance");
    const modal = document.getElementById("patient-modal");
    const closeModal = document.querySelector(".close-btn");
    const patientBalanceList = document.getElementById("patient-balance-list");

    function fetchSalesData(date) {
        fetch(`/api/sales/?date=${date}`)
            .then(response => response.json())
            .then(data => {
                earnings.textContent = `₱ ${data.sales_total}`;
                productsSold.textContent = data.products_sold_count;

                productList.innerHTML = ""; // Clear previous items
                if (data.products_sold.length === 0) {
                    productList.innerHTML = "<p>No products sold.</p>";
                } else {
                    data.products_sold.forEach(product => {
                        const item = document.createElement("div");
                        item.classList.add("product-item");
                        item.innerHTML = `
                            <span>${product.name}</span>
                            <span>${product.category}</span>
                            <span>${product.brand}</span>
                            <span>Qty: ${product.qty}</span>
                            <span>₱ ${product.price}</span>
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
                    patientBalanceList.innerHTML = `<tr><td colspan="3">No patient balance.</td></tr>`;
                } else {
                    data.balances.forEach(balance => {
                        const row = document.createElement("tr");
                        row.innerHTML = `
                            <td>${balance.patient_name}</td>
                            <td>₱ ${balance.previous_balance}</td>
                            <td><button class="add-balance-btn">Add</button></td>
                        `;
                        patientBalanceList.appendChild(row);
                    });
                }
            })
            .catch(error => console.error("Error fetching patient balances:", error));
    }

    viewBalanceBtn.addEventListener("click", () => {
        fetchPatientBalances();
        modal.style.display = "flex";
    });

    closeModal.addEventListener("click", () => {
        modal.style.display = "none";
    });

    window.addEventListener("click", (event) => {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });

    filterDate.addEventListener("change", () => {
        const selectedDate = filterDate.value;
        fetchSalesData(selectedDate);
    });

    // Load today's data on page load
    const today = new Date().toISOString().split("T")[0];
    filterDate.value = today;
    fetchSalesData(today);
});
