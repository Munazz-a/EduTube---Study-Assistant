async function sendToBackend(){
    const link = document.getElementById("link").value;
    localStorage.setItem("videoLink", link);
    window.location.href = "summary.html";

    if(!videoLink){
        alert("No video Link found!!");
        return;
    }

    const response = await fetch("http://localhost:3000/transcribe", {
        method : "POST",
        headers : { "Content-Type" : "application/json" },
        body : JSON.stringify({ videoLink })
    })
    const data = await response.json();

    if(data.transcript){
        document.getElementById("output").innerHTML = data.transcript;
    } else {
        document.getElementById("output").innerHTML = data.error;
    }
}