import express from "express";
import axios from "axios";

const app = express();
app.use(express.json());

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
  console.log("Node backend running on port 3000");
});
