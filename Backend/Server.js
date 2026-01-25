const express = require("express");
const app = express();
const path = require('path');
require('dotenv').config();
const axios = require("axios");

app.use(express.urlencoded({extended : true}));
app.use(express.json({ limit : "10mb" }));

console.log("STATIC DIR:", path.join(__dirname, "../Frontend"));

app.use(express.static(path.join(__dirname, '../Frontend')));

app.post("/ask", async (req, res) => {
  try {
    const response = await axios.post(
      "http://localhost:8000/chat",
      { question: req.body.question }
    );

    res.json(response.data);
  } catch (err) {
    res.status(500).json({ error: "Python service not reachable" });
  }
});

app.listen(3000, () => {
  console.log("✅ Node backend running at http://localhost:3000");
});