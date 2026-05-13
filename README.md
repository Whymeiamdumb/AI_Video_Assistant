# 🎥 AI Video Assistant

> Turn long videos and meetings into searchable knowledge.

An end-to-end AI-powered video assistant that can:

* 📥 Download audio from YouTube videos
* 📂 Process uploaded local audio/video files
* ✂️ Chunk large audio intelligently
* 🧠 Transcribe audio locally using Whisper AI
* 🌍 Translate Hindi speech into English
* 📋 Generate detailed summaries, action items, and key insights
* 🔎 Chat with your video using RAG (Retrieval-Augmented Generation)

Built using **Python, Streamlit, LangChain LCEL, Whisper, ChromaDB, and HuggingFace Embeddings**.

---

# 🚀 Features

## 🎬 Video & Audio Input

Supports:

* YouTube video links
* Local uploaded audio/video files

The system automatically extracts audio and prepares it for transcription.

---

## ✂️ Smart Audio Chunking

Large audio files are split into smaller chunks for:

* Faster transcription
* Lower memory usage
* Better reliability for long videos

Think of it like slicing a huge textbook into chapters before reading it.

---

## 🧠 Local Whisper AI Transcription

Uses OpenAI Whisper locally for high-quality speech recognition.

### Benefits

* No paid transcription API
* Works offline
* Accurate multilingual transcription
* Supports long-form content

---

## 🌍 Hindi → English Translation

If Hindi audio is detected, the assistant can translate transcripts into English using lightweight translation pipelines.

Useful for:

* Lectures
* Podcasts
* Interviews
* Regional content

---

## 📋 AI Summarization

After transcription, the assistant generates:

* Concise summaries
* Key discussion points
* Important insights
* Action items
* Decisions taken in the meeting/video

Powered using:

* LangChain LCEL
* Mistral API / compatible LLMs

---

## 🔎 Chat With Your Video (RAG)

The project also implements a vector-based Retrieval-Augmented Generation pipeline.

### How it works

1. Transcript is split into chunks
2. Chunks are converted into embeddings
3. Stored inside ChromaDB
4. Relevant chunks are retrieved when user asks questions

This allows users to ask:

* “What did the speaker say about AI agents?”
* “Summarize the marketing discussion”
* “What were the action items?”
* “At what point did they discuss deployment?”

Instead of searching manually through a 2-hour video.

---

# 🛠️ Tech Stack

## 🎤 Audio & Video Processing

* `yt-dlp`
* `pydub`
* `ffmpeg-python`

---

## 🧠 Speech Recognition

* `openai-whisper`
* `torch`
* `torchaudio`

---

## 🌍 Translation

* `deep-translator`

---

## 🔗 LLM + LangChain

* `langchain`
* `langchain-core`
* `langchain-community`

---

## 🧠 RAG Pipeline

* `chromadb`
* `sentence-transformers`
* `langchain-huggingface`

---

## 🖥️ Frontend

* `streamlit`
* `streamlit-extras`

---

## 📄 Export & Utilities

* `fpdf2`
* `reportlab`
* `python-dotenv`
* `numpy`
* `tqdm`

---

# 📂 Project Workflow

```text
YouTube URL / Local File
            │
            ▼
    Audio Extraction
            │
            ▼
      Audio Chunking
            │
            ▼
   Whisper Transcription
            │
            ▼
(Optional) Hindi Translation
            │
            ▼
      Transcript Creation
            │
     ┌──────┴──────┐
     ▼             ▼
 Summarization     RAG Pipeline
     │             │
     ▼             ▼
 Summary      Ask Questions
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/ai-video-assistant.git
cd ai-video-assistant
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Install FFmpeg

FFmpeg is required for audio extraction and processing.

### Windows

Download from:

```text
https://ffmpeg.org/download.html
```

Add FFmpeg to PATH.

### Linux

```bash
sudo apt install ffmpeg
```

### Mac

```bash
brew install ffmpeg
```

---

# 🔐 Environment Variables

Create a `.env` file:

```env
MISTRAL_API_KEY=your_api_key_here
```

---

# ▶️ Run The App

```bash
streamlit run app.py
```

---

# 🧪 Example Use Cases

## 🎓 Students

* Summarize lectures
* Create study notes
* Ask questions from recorded classes

---

## 💼 Meetings

* Extract action items
* Generate meeting summaries
* Track decisions

---

## 🎙️ Podcasts & Interviews

* Convert long conversations into searchable knowledge

---

# 📸 Future Improvements

* Speaker diarization
* Timestamp-based navigation
* Multi-language support
* Semantic video search
* PDF/Markdown exports
* Real-time transcription
* Docker deployment
* Cloud deployment support

---

# 🧠 What I Learned Building This

This project helped explore real-world AI engineering concepts like:

* Audio preprocessing
* Local AI inference
* RAG architecture
* Vector databases
* Embeddings
* Prompt engineering
* LangChain LCEL pipelines
* Streamlit app development

It started as a simple transcription tool and evolved into a full AI-powered video understanding system.

---

# 🤝 Contributing

Pull requests and suggestions are welcome.

If you find bugs or want to improve the project, feel free to open an issue.

---

# 📜 License

This project is licensed under the MIT License.

---

# ⭐ If You Like This Project

Give the repository a star and share it with others.

It helps more than you think.

