# 🤖 Smart PDF Chatbot

*A Generative AI-powered RAG chatbot for interactive document querying.*

*Bot Link: https://aipdfchatbot-aruk.streamlit.app*

<img width="1857" height="907" alt="image" src="https://github.com/user-attachments/assets/d052de15-0347-4d4f-bd14-536440b4cad9" />



---

## 📘 Overview

The **Smart PDF Chatbot** allows users to upload PDF documents and chat naturally with them.
It uses **Retrieval-Augmented Generation (RAG)** to provide **contextual, document-grounded answers** powered by modern LLMs (OpenAI, Gemini, or Groq).

You can ask questions directly from your uploaded files, get concise and relevant answers, and even rename or manage chat sessions — all within a modern Streamlit UI.

---

## 🚀 Features

* 📄 **PDF Upload & Parsing:** Upload one or multiple PDFs dynamically.
* 🧠 **RAG-based Answering:** Combines vector similarity search with LLM reasoning.
* 💬 **Persistent Chat Sessions:** Save, view, and rename previous conversations.
* 🎨 **Modern UI Design:** Glassy dark theme with rounded chat bubbles and smooth animations.
* 🧾 **Context-Aware Responses:** If an answer isn’t in the PDF, the chatbot clearly explains that.
* 🔄 **Auto-Updating Knowledge Base:** Add, remove, or update documents without reconfiguration.

---

## 🏗️ System Architecture

```
┌──────────────────────────────┐
│        User Interface        │
│  (Streamlit Web App)         │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│   RAG Pipeline (LangChain)   │
│  1. Retrieve context chunks  │
│  2. Construct dynamic prompt │
│  3. Generate response (LLM)  │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│  Vector Store (FAISS Index)  │
│  + Embeddings (HuggingFace)  │
└──────────────────────────────┘
```

---

## ⚙️ Tech Stack

| Component            | Technology                                                  |
| -------------------- | ----------------------------------------------------------- |
| **Frontend**         | Streamlit                                                   |
| **LLM Integration**  | OpenAI / Gemini / Groq                                      |
| **Text Processing**  | LangChain (`PyPDFLoader`, `RecursiveCharacterTextSplitter`) |
| **Embeddings**       | HuggingFace Sentence Transformers                           |
| **Vector Storage**   | FAISS                                                       |
| **State Management** | Streamlit `session_state`                                   |
| **Styling**          | Custom CSS (dark glassy theme)                              |

---

## 🧩 Project Structure

```
📂 Smart-PDF-Chatbot/
├── app.py                        # Streamlit UI + main logic
├── rag_pipeline.py               # RAG retrieval and generation logic
├── vectorstore_manager.py        # Embedding & FAISS handling
├── chat_OpenAI.py / chat_Gemini.py  # LLM client wrappers
├── session_manager.py            # Chat session handling
├── history_manager.py            # Saves chat history
├── data/                         # Uploaded PDFs
├── faq_questions.json (optional) # Keyword-based suggestion data
└── requirements.txt              # Dependencies
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/aruk3002/RAG_PDF_CHATBOT.git
cd smart-pdf-chatbot
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate    # On Windows
# OR
source venv/bin/activate # On Mac/Linux
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Add Your API Key

Create a `.env` file in the project root and add your key:

```
OPENAI_API_KEY=your_api_key_here
# or
GEMINI_API_KEY=your_api_key_here
# or
GROQ_API_KEY=your_api_key_here
```

*(Make sure `.env` is added to `.gitignore` to protect your key)*

### 5️⃣ Run the App

```bash
streamlit run app.py
```

Then open your browser at `http://localhost:8501/`

---

## 💬 How It Works

1. **Upload PDFs:**
   PDFs are stored under the `data/` folder and processed by LangChain’s `PyPDFLoader`.

2. **Vector Embedding:**
   Each document is chunked, embedded using HuggingFace models, and stored in a FAISS vector index.

3. **Query Flow:**

   * User asks a question.
   * Relevant chunks are retrieved from FAISS.
   * LLM generates an answer **grounded in PDF context**.
   * If the answer isn’t in the document, it politely informs the user.

4. **Session Management:**
   Conversations are saved per session.
   You can rename chats manually in the sidebar.

---

## 🧾 Example Interaction

**User:**

> What is the definition of manufacturing?

**Bot:**

> The definition of manufacturing is not mentioned directly in the document, but the file discusses manufacturing processes such as production efficiency and quality control. Generally, manufacturing refers to converting raw materials into finished goods using labor and machinery.

---

## 🔄 Knowledge Base Updates

* To **add new PDFs**, simply upload them via the UI.
  → The embeddings and FAISS index update automatically.

* To **update or replace documents**, re-upload the updated file.
  → The system re-embeds only that document.

* To **remove old data**, delete the PDF from the `data/` folder.
  → On the next session, the chatbot reflects the change.

No retraining or reconfiguration required.


---

## 🧠 Future Improvements

* 🔍 Add keyword-based question suggestions from the PDF
* 💾 Persistent FAISS index storage between runs
* 🧩 Multi-user session isolation
* 🗑 Chat delete & export options

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create your feature branch
3. Submit a pull request

---

## 👨‍💻 Author

**Chandan Aruk**
📊 Data Analyst | 💡 AI & Data Science Enthusiast

📧 Linkedin [https://linkedin.com/in/chandan-aruk]
