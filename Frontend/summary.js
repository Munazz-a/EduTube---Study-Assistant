async function startTranscripting(){
    const videoLink = localStorage.getItem('videoLink');

    document.getElementById("summary").innerText = "⏳ Transcribing... please wait";

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