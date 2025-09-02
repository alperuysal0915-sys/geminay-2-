<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Yapay zeka asistanı - sohbet ve sesli mod">
  <title>Yapay Zeka Asistan</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-300 min-h-screen flex">

  <!-- Sol taraf: Geçmiş -->
  <div class="w-1/4 bg-gray-200 shadow-lg p-4 flex flex-col">
    <h2 class="text-lg font-bold mb-3">Geçmiş</h2>
    <ul id="history" class="flex-1 space-y-2 overflow-y-auto text-sm">
      <!-- Geçmiş konuşmalar buraya gelecek -->
    </ul>
  </div>

  <!-- Sağ taraf: Sohbet -->
  <div class="w-3/4 flex flex-col bg-gray-200 shadow-inner p-6" id="chat-page">
    <h1 class="text-2xl font-bold text-center mb-4">Yapay Zeka Asistan</h1>
    <div id="chat-box" class="flex-1 overflow-y-auto border p-3 rounded-lg mb-4 space-y-2 bg-gray-100">
      <!-- Mesajlar buraya gelecek -->
    </div>
    <div class="flex gap-2 items-center">
      <button onclick="openVoicePage()" class="p-2 bg-gray-400 rounded-full hover:bg-gray-500">
        🎤
      </button>
      <input id="user-input" type="text" placeholder="Bir şey sor..." class="flex-1 border rounded-lg p-2" />
      <button onclick="sendMessage()" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">Gönder</button>
    </div>
  </div>

  <!-- Sesli Sayfa -->
  <div class="hidden w-full flex flex-col items-center justify-center" id="voice-page">
    <h1 class="text-2xl font-bold mb-6">Sesli Asistan</h1>
    <div class="w-48 h-48 rounded-full flex items-center justify-center text-white text-xl font-bold shadow-2xl"
         style="background: radial-gradient(circle at center, skyblue, midnightblue);">
      Dinliyorum 🎧
    </div>
    <button onclick="closeVoicePage()" class="mt-8 px-4 py-2 bg-red-500 text-white rounded-lg">Geri Dön</button>
  </div>

  <script>
    const chatBox = document.getElementById("chat-box");
    const input = document.getElementById("user-input");
    const history = document.getElementById("history");
    const chatPage = document.getElementById("chat-page");
    const voicePage = document.getElementById("voice-page");

    // ⚠️ OpenAI API key'i buraya ekle
    const OPENAI_API_KEY = "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";

    function addMessage(sender, text) {
      const msg = document.createElement("div");
      msg.className = sender === "user" ? "text-right" : "text-left";
      msg.innerHTML = `<span class="inline-block px-3 py-2 rounded-xl ${sender === "user" ? 'bg-blue-500 text-white' : 'bg-gray-400'}">${text}</span>`;
      chatBox.appendChild(msg);
      chatBox.scrollTop = chatBox.scrollHeight;
    }

    function addHistory(item) {
      const li = document.createElement("li");
      li.textContent = item;
      history.appendChild(li);
    }

    async function sendMessage(message) {
      const text = message || input.value.trim();
      if (!text) return;
      addMessage("user", text);
      addHistory("Sen: " + text);
      input.value = "";

      try {
        const res = await fetch("https://api.openai.com/v1/chat/completions", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${OPENAI_API_KEY}`
          },
          body: JSON.stringify({
            model: "gpt-4o-mini",
            messages: [{ role: "user", content: text }]
          })
        });

        const data = await res.json();
        const reply = data.choices?.[0]?.message?.content || "Bir hata oluştu.";
        addMessage("bot", reply);
        addHistory("Bot: " + reply);

        // Eğer sesli sayfa açıksa cevap ver
        if (!chatPage.classList.contains("flex")) speak(reply);

      } catch (err) {
        addMessage("bot", "Sunucuya bağlanırken hata oluştu!");
        addHistory("Bot: Sunucu hatası");
      }
    }

    // Mikrofon sayfasını aç
    function openVoicePage() {
      chatPage.classList.add("hidden");
      voicePage.classList.remove("hidden");
      voicePage.classList.add("flex");
      startListening();
    }

    function closeVoicePage() {
      voicePage.classList.add("hidden");
      chatPage.classList.remove("hidden");
      chatPage.classList.add("flex");
    }

    // Web Speech API ile dinleme
    function startListening() {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRecognition) {
        alert("Tarayıcınız ses tanımayı desteklemiyor!");
        return;
      }

      const recognition = new SpeechRecognition();
      recognition.lang = "tr-TR";
      recognition.start();

      recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        sendMessage(transcript);
      };

      recognition.onerror = function() {
        speak("Ses algılanamadı, tekrar deneyin.");
      };
    }

    // Sesli cevap
    function speak(text) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = "tr-TR";
      speechSynthesis.speak(utterance);
    }
  </script>
</body>
</html>
