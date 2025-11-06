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
                    if (row) {
                        row.classList.remove("green-background", "red-background");
                        if (data.status === "Оказана") {
                            row.classList.add("green-background");
                        } else if (data.status === "Отменено") {
                            row.classList.add("red-background");
                        }
                    }
                    // Кнопки остаются активными для многократного изменения статуса
                }
            })
            .catch(error => console.error("Ошибка:", error));
        });
    });

    // Обработчик для формы переноса, если элемент существует
    const rescheduleForm = document.getElementById("rescheduleForm");
    if (rescheduleForm) {
        rescheduleForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const appointmentId = document.getElementById("reschedule_appointment_id").value;
            const newDate = document.getElementById("new_date").value;
            const newTime = document.getElementById("new_time").value;
            const reason = document.getElementById("reschedule_reason").value;
            
            let formData = new FormData();
            formData.append("new_date", newDate);
            formData.append("new_time", newTime);
            formData.append("reason", reason);
            
            fetch(`/appointments/${appointmentId}/reschedule`, {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    document.getElementById("status-" + appointmentId).textContent = data.new_status;
                    disableButtons(appointmentId);
                    alert("Запись перенесена");
                    hideRescheduleForm();
                } else {
                    alert("Ошибка: " + data.error);
                }
            })
            .catch(err => alert("Ошибка запроса: " + err));
        });
    }

    // Обработчик кнопки "Отмена" в форме переноса, если она существует
    const cancelRescheduleBtn = document.getElementById("cancel-reschedule-btn");
    if (cancelRescheduleBtn) {
        cancelRescheduleBtn.addEventListener("click", function () {
            hideRescheduleForm();
        });
    }

    function disableButtons(appointmentId) {
        const buttonsForId = document.querySelectorAll(`.status-btn[data-id="${appointmentId}"]`);
        buttonsForId.forEach(btn => btn.disabled = false); // Теперь не блокируем, чтобы можно было менять статус повторно
    }

    function showRescheduleForm(appointmentId) {
        const rescheduleFormContainer = document.getElementById("reschedule-form");
        if (rescheduleFormContainer) {
            document.getElementById("reschedule_appointment_id").value = appointmentId;
            rescheduleFormContainer.style.display = "block";
        }
    }

    function hideRescheduleForm() {
        const rescheduleFormContainer = document.getElementById("reschedule-form");
        if (rescheduleFormContainer) {
            rescheduleFormContainer.style.display = "none";
        }
    }
});
