document.addEventListener("DOMContentLoaded", () => {
    const filterDate = document.getElementById("filter-date");
    const earnings = document.getElementById("total-earnings");
    const productsSold = document.getElementById("products-sold");
    const productList = document.getElementById("product-list");

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

    filterDate.addEventListener("change", () => {
        const selectedDate = filterDate.value;
        fetchSalesData(selectedDate);
    });

    // Load today's data on page load
    const today = new Date().toISOString().split("T")[0];
    filterDate.value = today;
    fetchSalesData(today);
});
