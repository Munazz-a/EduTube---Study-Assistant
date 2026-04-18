# 🎓 EduTube – AI-Powered Study Assistant

> An AI-powered platform that allows users to query educational video transcripts using a Retrieval-Augmented Generation (RAG) pipeline.

---

## 📌 Overview

EduTube helps students quickly understand long educational videos by allowing them to ask questions and receive accurate, context-aware answers. It processes transcript data and uses AI to generate responses in real time.

---

## 🧠 Features

* ✅ Ask questions from video transcripts
* ✅ RAG-based intelligent retrieval system
* ✅ FastAPI backend for AI processing
* ✅ Node.js server for API handling
* ✅ Supports multiple users concurrently
* ✅ Efficient semantic search using FAISS

---

## 📸 Screenshots

### 🏠 Home Page
![Home](/Screenshots/Home.png)

### 💬 Summary 
![Query](/Screenshots/Summary.png)

### 📊 query Interface
![Results](/Screenshots/qna.png)

---

## 🏗️ Tech Stack

**Backend:**

* FastAPI
* Node.js (Express)

**AI / ML:**

* Sentence Transformers (`all-MiniLM-L6-v2`)
* FAISS
* OpenAI API

**Other Tools:**

* Python
* NumPy
* Nodemon

---

## ⚙️ How It Works

1. Transcripts are divided into chunks
2. Chunks are converted into embeddings
3. FAISS index is created for fast retrieval
4. User query is embedded and matched
5. Node.js server handles API requests
6. FastAPI processes AI logic
7. AI generates final answer

---

## 🚀 Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Munazz-a/EduTube---Study-Assistant.git
cd EduTube---Study-Assistant
```

### 2️⃣ Setup Python Backend (FastAPI)

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

### 3️⃣ Setup Node.js Server

```bash
npm install
nodemon server.js
```

---

## 🔑 Environment Variables

Create a `.env` file:

```
OPENAI_API_KEY=your_api_key
```


## 🎯 Future Improvements

*  Add frontend UI
*  Support video upload directly
*  Improve retrieval accuracy using hybrid search
*  Deploy on cloud VM

