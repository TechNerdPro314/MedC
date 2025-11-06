function updateDateTime() {
    const now = new Date();
    
    // Форматируем дату и время в российском стиле
    const date = now.toLocaleDateString("ru-RU", { 
        weekday: "long", year: "numeric", month: "long", day: "numeric" 
    });

    const time = now.toLocaleTimeString("ru-RU", { 
        hour: "2-digit", minute: "2-digit", second: "2-digit" 
    });

    document.getElementById("datetime").textContent = `${date}, ${time}`;
}

// Обновляем дату и время каждую секунду
setInterval(updateDateTime, 1000);
updateDateTime();
