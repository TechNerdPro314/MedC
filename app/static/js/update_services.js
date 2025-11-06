// app/static/js/update_services.js

document.addEventListener("DOMContentLoaded", function () {
    const doctorSelect = document.getElementById("doctor_id");
    const serviceSelect = document.getElementById("service_id");
    const serviceInput = document.getElementById("selected_service");

    const servicesBySpecialization = JSON.parse(doctorSelect.getAttribute("data-services"));

    if (doctorSelect) {
        doctorSelect.addEventListener("change", function () {
            updateServices();
        });
    }

    if (serviceSelect) {
        serviceSelect.addEventListener("change", function () {
            updateSelectedService();
        });
    }

    function updateServices() {
        serviceSelect.innerHTML = "";
        serviceInput.value = ""; // Очищаем скрытое поле

        const selectedDoctor = doctorSelect.options[doctorSelect.selectedIndex];
        const specialization = selectedDoctor.getAttribute("data-specialization");

        if (specialization && servicesBySpecialization[specialization]) {
            servicesBySpecialization[specialization].forEach(service => {
                const option = document.createElement("option");
                option.value = service.name;
                option.textContent = `${service.name} - ${service.price} руб.`;
                serviceSelect.appendChild(option);
            });

            // Устанавливаем первую услугу как выбранную
            serviceSelect.selectedIndex = 0;
            updateSelectedService();
        } else {
            const defaultOption = document.createElement("option");
            defaultOption.textContent = "Нет доступных услуг";
            serviceSelect.appendChild(defaultOption);
        }
    }

    function updateSelectedService() {
        serviceInput.value = serviceSelect.value; // Обновляем скрытое поле
    }
});
