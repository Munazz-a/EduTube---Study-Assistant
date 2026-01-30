const express = require("express");
const app = express();
const path = require('path');
require('dotenv').config();
const axios = require("axios");

app.use(express.urlencoded({extended : true}));
app.use(express.json({ limit : "10mb" }));

// console.log("STATIC DIR:", path.join(__dirname, "../Frontend"));

app.use(express.static(path.join(__dirname, '../Frontend')));

app.post("/transcribe", async (req, res) => {
  try {
    const response = await axios.post(
      "http://localhost:8000/transcribe",
      { videoId : req.body.videoId }
    );

    res.json(response.data);
  } catch (err) {
    res.status(500).json({ error: "Python transcription service not reachable" });
  }
});
// CHAT
app.post("/chat", async (req, res) => {
  try {
    const response = await axios.post(
      "http://localhost:8000/chat",
      { question : req.body.question }
    );

    res.json(response.data);
  } catch (err) {
    res.status(500).json({ error: "Python chat service not reachable" });
  }
});


app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '../Frontend', 'home.html'));
})
app.get('/summary', (req, res) => {
  res.sendFile(path.join(__dirname, '../Frontend', 'summary.html'));
})

app.listen(3000, () => {
  console.log("✅ Node backend running at http://localhost:3000");
});