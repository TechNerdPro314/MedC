document.addEventListener("DOMContentLoaded", function () {
    const patientSelect = document.getElementById("patient_id");
    const appointmentsTable = document.getElementById("appointments_table");
    const medicationForm = document.getElementById("medication_form");
    const medicationNameInput = document.getElementById("medication_name");
    const dosageInput = document.getElementById("dosage");
    const selectedAppointmentInput = document.getElementById("selected_appointment_id");
    const selectedPatientInput = document.getElementById("selected_patient_id");

    window.loadAppointments = function () {
        const patientId = patientSelect.value;
        selectedPatientInput.value = patientId;

        fetch(`/get_appointments/${patientId}`)
            .then(response => response.json())
            .then(data => {
                appointmentsTable.innerHTML = `
                    <tr>
                        <th>Врач</th>
                        <th>Специализация</th>
                        <th>Услуга</th>
                        <th>Дата</th>
                        <th>Время</th>
                        <th>Действие</th>
                    </tr>
                `;

                data.forEach(appointment => {
                    const row = document.createElement("tr");
                    row.innerHTML = `
                        <td>${appointment.doctor}</td>
                        <td>${appointment.specialization}</td>
                        <td>${appointment.service}</td>
                        <td>${appointment.date}</td>
                        <td>${appointment.time}</td>
                        <td><button onclick="selectAppointment(${appointment.id})">Выбрать</button></td>
                    `;
                    appointmentsTable.appendChild(row);
                });
            });
    };

    window.selectAppointment = function (appointmentId) {
        selectedAppointmentInput.value = appointmentId;
        medicationForm.style.display = "block";
    };

    medicationForm.addEventListener("submit", function (event) {
        event.preventDefault();

        fetch("/add_medication", {
            method: "POST",
            body: new FormData(medicationForm)
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            medicationForm.reset();
            medicationForm.style.display = "none";
        });
    });
});
