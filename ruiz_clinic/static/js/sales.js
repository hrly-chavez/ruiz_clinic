document.addEventListener("DOMContentLoaded", () => {
    const filterDate = document.getElementById("filter-date");
    const modal = document.getElementById("patient-modal");
    const closeModal = document.querySelector(".close-btn");
    const viewBalanceBtn = document.getElementById("view-patient-balance");

    viewBalanceBtn.addEventListener("click", () => {
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
        console.log("Selected date:", selectedDate);
        // Add logic to update dashboard data based on the selected date
    });
});