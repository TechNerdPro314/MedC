document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll(".status-btn");

    buttons.forEach(button => {
        button.addEventListener("click", function () {
            const appointmentId = this.getAttribute("data-id");
            const status = this.getAttribute("data-status");

            const formData = new FormData();
            formData.append("appointment_id", appointmentId);
            formData.append("status", status);

            fetch("/update_status", {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    // Обновляем статус в ячейке
                    document.getElementById(`status-${appointmentId}`).textContent = data.status;
                    
                    // Меняем цвет строки в зависимости от статуса
                    const row = document.getElementById(`row-${appointmentId}`);
                    row.classList.remove("green-background", "red-background");
                    if (data.status === "Оказана") {
                        row.classList.add("green-background");
                    } else if (data.status === "Не оказана") {
                        row.classList.add("red-background");
                    }
                    // Кнопки остаются активными (не блокируются)
                }
            })
            .catch(error => console.error("Ошибка:", error));
        });
    });
});
