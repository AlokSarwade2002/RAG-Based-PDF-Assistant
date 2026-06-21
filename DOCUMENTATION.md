# Smart PDF Chatbot - Project Documentation

## 1. What this project does

This repository implements a **PDF chatbot** using a **Retrieval-Augmented Generation (RAG)** approach.

The app lets a user:
- upload one or more PDF documents,
- search them by asking natural language questions,
- receive answers grounded in the uploaded PDF content.

It uses a combination of:
- PDF parsing,
- text chunking,
- embeddings,
- a FAISS vector similarity store,
- a Gemini LLM for answer generation,
- a Streamlit user interface.

---

## 2. Main files and their roles

### `app.py`
- This is the Streamlit application entry point.
- It builds the user interface, sidebar, file upload area, chat display, and chat input.
- It creates and maintains session state for:
  - chat sessions,
  - active session history,
  - the RAG pipeline,
  - history storage.
- After PDFs are uploaded, it initializes `RAGPipeline` and `HistoryManager`.
- When the user asks a question, it passes the query to the pipeline and shows the response.

### `rag_pipeline.py`
- This file defines the `RAGPipeline` class.
- It connects the vector store, history manager, and language model.
- It performs these steps:
  1. retrieve the most similar PDF chunks for the query,
  2. build a prompt using document context and previous chat history,
  3. ask the LLM for a response,
  4. save the user question and assistant answer to history.

### `vectorstore_manager.py`
- Manages PDF loading, text splitting, embedding, and FAISS vectorstore creation.
- It caches the vectorstore locally in `faiss_cache/kb_index.pkl`.
- It also saves PDF metadata so it can detect when PDFs change.
- If the PDFs change or the cache is missing, it rebuilds the index.
- It uses:
  - `PyPDFLoader` to read PDF pages,
  - `RecursiveCharacterTextSplitter` to split text into chunks,
  - `HuggingFaceEmbeddings` to compute text embeddings,
  - `FAISS` to store vectors.

### `chat_gemini.py`
- Wraps the Gemini API client.
- Loads the API key from the `.env` file using `python-dotenv`.
- Configures `google.generativeai` and sends prompts to the Gemini model.
- Returns the model text output.

### `history_manager.py`
- Saves and loads chat history for a session.
- History is stored in JSON files under `chat_history/{session_id}.json`.
- Each saved turn contains a `role` (`user` or `assistant`) and `content`.

### `session_manager.py`
- Manages chat sessions inside Streamlit state.
- Creates new sessions with unique IDs.
- Renames sessions when requested.
- Keeps a list of messages for each session.

### `.env`
- Stores API keys used by the project.
- Example entries:
  ```
  OPENAI_API_KEY=your_api_key_here
  GEMINI_API_KEY=your_api_key_here
  GROQ_API_KEY=your_api_key_here
  ```
- `chat_gemini.py` currently uses `GEMINI_API_KEY`.

---

## 3. Data and flow overview

### Uploading PDFs
- The user uploads PDF files using the Streamlit file uploader.
- The app saves uploaded PDFs into a local `data/` directory.

### Indexing PDFs
- `VectorStoreManager` reads all uploaded PDFs.
- It splits document text into overlapping chunks.
- It creates embeddings for each chunk.
- It stores embeddings in a FAISS vector index for fast similarity search.

### Asking a question
1. The user types a question in the chat input.
2. `RAGPipeline.ask()` retrieves the top 3 most relevant chunks.
3. It creates a prompt with:
   - document context,
   - chat history,
   - the user question.
4. The Gemini model generates an answer.
5. The question and answer are saved to history.
6. The app displays the result in the chat UI.

### Session and history management
- Sessions are stored in `st.session_state.sessions`.
- The user can create a new chat or rename a chat.
- Each session’s messages are saved to disk in `chat_history/`.
- Chat history is reloaded when needed.

---

## 4. How to run the project

1. Install dependencies from `requirements.txt`.
2. Create a `.env` file in the repo root with your API key.
3. Run the app with:
   ```bash
   streamlit run app.py
   ```
4. Open the displayed Streamlit URL in your browser.

---

## 5. Key points to understand the code

- `app.py` is the UI and controller.
- `rag_pipeline.py` is the brain that connects search and LLM output.
- `vectorstore_manager.py` builds and reuses the knowledge index.
- `chat_gemini.py` sends prompts to the language model.
- `history_manager.py` persists conversation history.
- `session_manager.py` keeps multiple chat sessions organized.

---

## 6. Notes for easy maintenance

- If you want to switch LLMs, update `chat_gemini.py` or add a new wrapper file.
- If you want better persistence, save the FAISS cache and session files to a stable location.
- To support more PDF types or text extraction improvements, adjust `PyPDFLoader` or add new loaders.

---

## 7. Helpful summary

This app is a simple RAG chatbot built with Streamlit. It reads PDFs, makes searchable embeddings, and answers questions using a Gemini model. The code is separated into UI, retrieval, embedding, model API, session handling, and history persistence.

If you want, I can also add a `Quick Start` section inside the `README.md` next. 