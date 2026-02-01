function extractVideoId(url) {
  try {
    const u = new URL(url);
    if (u.hostname.includes("youtu.be")) {
      return u.pathname.slice(1);
    }
    return u.searchParams.get("v");
  } catch {
    return null;
  }
}


async function loadVideo() {
  const videoLink = localStorage.getItem("videoLink");
  const videoId = extractVideoId(videoLink);

  document.getElementById("summary").innerText = "⏳ Fetching transcript...";

  const res = await fetch("/transcribe", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ videoId })
  });

  const data = await res.json();

  if (data.preview) {
    document.getElementById("summary").innerText = data.preview;
  } else {
    document.getElementById("summary").innerText = data.error || "❌ Failed to fetch transcript";
  }
}

loadVideo();



window.askQuestion = async function () {
  const input = document.getElementById("questionInput");
  const question = input.value.trim();
  if (!question) return;

  input.value = "";

  const chatBot = document.getElementById('chatBox');

    //User Message
    const userDiv = document.createElement('div');
    userDiv.className = 'flex justify-end';
    userDiv.innerHTML = `
    <div class="bg-blue-600 text-white p-3 rounded-xl text-sm max-w-[75%]">
        ${question}
    </div>
    `;
    chatBot.appendChild(userDiv);

    //Bot typing
    const botDiv = document.createElement('div');
    botDiv.className = 'flex items-start gap-3';
    botDiv.innerHTML = `
    <div class="bg-blue-600 text-white p-3 rounded-xl text-sm max-w-[75%]">
        ⏳ Thinking...
    </div>
    `;
    chatBot.appendChild(botDiv);

  const res = await fetch("http://localhost:3000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question })
  });

  const data = await res.json();
  // alert(data.answer);

  // Bot Message
    botDiv.innerHTML = `
    <div class="bg-white p-3 rounded-xl shadow text-sm max-w-[75%]">
        ${data.answer}
    </div>
    `;
    // chatBot.appendChild(botDiv);
};

window.downloadPDF = function () {
  const element = document.getElementById("pdfContent");

  const options = {
    margin: 0.5,
    filename: `EduTube_${new Date().toLocaleDateString()}.pdf`,
    image: { type: "jpeg", quality: 0.98 },
    html2canvas: { scale: 2 },
    jsPDF: { unit: "in", format: "a4", orientation: "portrait" }
  };

  html2pdf().set(options).from(element).save();
};

