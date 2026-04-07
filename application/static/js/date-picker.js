document.addEventListener("DOMContentLoaded", function () {
    const yearSelect = document.getElementById("year");
    const monthSelect = document.getElementById("month");
    const daySelect = document.getElementById("day");

    if (!yearSelect || !monthSelect || !daySelect) return;

    function daysInMonth(year, month) {
        return new Date(year, month, 0).getDate();
    }

    function updateDays() {
        const selectedYear = parseInt(yearSelect.value, 10);
        const selectedMonth = parseInt(monthSelect.value, 10);
        const currentDay = parseInt(daySelect.value, 10);

        const maxDays = daysInMonth(selectedYear, selectedMonth);

        daySelect.innerHTML = "";

        for (let d = 1; d <= maxDays; d++) {
            const option = document.createElement("option");
            option.value = d;
            option.textContent = d;

            if (d === Math.min(currentDay, maxDays)) {
                option.selected = true;
            }

            daySelect.appendChild(option);
        }
    }

    yearSelect.addEventListener("change", updateDays);
    monthSelect.addEventListener("change", updateDays);

    updateDays();
});