async function startTranscripting(){
    const videoLink = localStorage.getItem('videoLink');

    document.getElementById("summary").innerText = "⏳ Summarizing... please wait";

    const response = await fetch("http://localhost:3000/transcribe", {
        method : "POST",
        headers : { "Content-Type" : "application/json" },
        body : JSON.stringify({ videoLink })
    })
    const data = await response.json();

    if(data.transcript){
        document.getElementById("summary").innerHTML = data.transcript;
    } else {
        document.getElementById("summary").innerHTML = data.error;
    }
}
startTranscripting();

// CHATBOT PIPELINE
async function askQuestion(){
    const input = document.getElementById('questionInput');
    const question = input.value.trim();
    if(!question) return;

    input.value = '';

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

    // Fetch 
    const response = await fetch("http://localhost:3000/chat", {
        method : 'POST',
        headers : { 'Content-Type' : 'application/json' },
        body : JSON.stringify({question})
    })
    const data = response.json();
    console.log(data);

    // Bot Message
    botDiv.innerHTML = `
    <div class="bg-white p-3 rounded-xl shadow text-sm max-w-[75%]">
        ${data.answer}
    </div>
    `;
    chatBot.appendChild(botDiv);
}