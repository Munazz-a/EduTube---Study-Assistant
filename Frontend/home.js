async function sendToBackend(){
    const videoLink = document.getElementById("link").value;

    if(!videoLink){
        alert("No video Link found!!");
        return;
    }
    localStorage.setItem('videoLink', videoLink);
    window.location.href = '/summary';
}