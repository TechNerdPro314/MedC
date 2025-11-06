document.addEventListener("DOMContentLoaded", function(){
    console.log("Assistant script loaded");

    const chatWindow = document.getElementById("chat-window");
    const chatInput = document.getElementById("chat-input");
    const sendBtn = document.getElementById("send-btn");

    if (!chatWindow || !chatInput || !sendBtn) {
        console.error("Не найдены необходимые элементы (chat-window, chat-input, send-btn).");
        return;
    }

    // Текущий этап диалога: 0 - запрашиваем дату, 1 - запрашиваем ФИО врача
    let conversationStep = 0;
    let selectedDate = "";
    let selectedDoctor = "";

    // Функция для добавления сообщения в окно чата
    function addMessage(text, sender = "assistant") {
        const msgDiv = document.createElement("div");
        msgDiv.classList.add("message", sender);
        msgDiv.textContent = text;
        chatWindow.appendChild(msgDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    // Функция обработки ввода пользователя
    function processUserInput(input) {
        if (conversationStep === 0) {
            selectedDate = input;
            conversationStep++;
            addMessage("Отлично! Вы хотите записаться на " + selectedDate + ". Какого врача вы предпочитаете? Введите ФИО врача.");
        } else if (conversationStep === 1) {
            selectedDoctor = input;
            conversationStep++;
            addMessage("Хорошо, вы выбрали врача " + selectedDoctor + ". Для подтверждения записи нажмите кнопку ниже.");
            const confirmBtn = document.createElement("button");
            confirmBtn.textContent = "Записаться";
            confirmBtn.addEventListener("click", function(){
                window.location.href = "/register/appointment?date=" 
                    + encodeURIComponent(selectedDate) + "&doctor=" 
                    + encodeURIComponent(selectedDoctor);
            });
            chatWindow.appendChild(confirmBtn);
            chatWindow.scrollTop = chatWindow.scrollHeight;
        }
    }

    // Обработчик клика по кнопке "Отправить"
    sendBtn.addEventListener("click", function(){
        console.log("Send button clicked");
        const inputText = chatInput.value.trim();
        if (inputText !== "") {
            addMessage(inputText, "user");
            processUserInput(inputText);
            chatInput.value = "";
        }
    });

    // Начало диалога
    addMessage("Здравствуйте! Я ваш виртуальный помощник. На какую дату вы хотите записаться на приём? (Введите дату в формате ДД.ММ.ГГГГ)");
});
