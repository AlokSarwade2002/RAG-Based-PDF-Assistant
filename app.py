import streamlit as st
from rag_pipeline import RAGPipeline
from history_manager import HistoryManager
import os

# -------------------------------
# Streamlit Page Configuration
# -------------------------------
st.set_page_config(
    page_title="📄 PDF Chatbot",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# Modern UI Styling
# -------------------------------
st.markdown("""
<style>
/* ===== Global Base Styling ===== */
body {
    font-family: 'Inter', sans-serif;
    transition: all 0.3s ease-in-out;
}

/* ===== Default (Light Mode) ===== */
body {
    background-color: #f8fafc;
    color: #1e293b;
}

/* ===== Main Container ===== */
.main {
    background: linear-gradient(145deg, #ffffff, #f1f5f9);
    padding: 1rem 2rem;
    border-radius: 1rem;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.08);
}

/* ===== Title ===== */
h1 {
    text-align: center;
    color: #2563eb;
    font-size: 2.2rem !important;
    font-weight: 700;
    text-shadow: 0 0 6px rgba(37,99,235,0.15);
}

/* ===== Sidebar ===== */
[data-testid="stSidebar"] {
    background: #f1f5f9;
    border-right: 1px solid rgba(148,163,184,0.3);
}
.sidebar-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: #1e40af;
    margin-bottom: 1rem;
}

/* ===== Buttons ===== */
button[kind="primary"] {
    background: linear-gradient(90deg, #3b82f6, #2563eb);
    color: white;
    border: none;
    border-radius: 0.6rem;
    font-weight: 600;
    transition: all 0.3s ease-in-out;
}
button[kind="primary"]:hover {
    background: linear-gradient(90deg, #2563eb, #1d4ed8);
    transform: scale(1.02);
}

/* ===== File Uploader ===== */
[data-testid="stFileUploader"] {
    background: #f8fafc;
    border: 1px dashed #3b82f6;
    border-radius: 1rem;
    padding: 1rem;
    color: #1e293b;
}

/* ===== Chat Messages ===== */
.stChatMessage {
    padding: 1rem;
    border-radius: 1rem;
    margin: 0.5rem 0;
    line-height: 1.5;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.stChatMessage[data-testid="stChatMessage-user"] {
    background: linear-gradient(145deg, #dbeafe, #93c5fd);
    color: #1e3a8a;
    text-align: right;
    border-top-right-radius: 0;
}

.stChatMessage[data-testid="stChatMessage-assistant"] {
    background: #e2e8f0;
    color: #1e293b;
    border-top-left-radius: 0;
}

/* ===== Chat Input ===== */
[data-testid="stChatInputContainer"] {
    background: #f1f5f9;
    border-top: 1px solid rgba(148,163,184,0.3);
    padding-top: 0.5rem;
}
textarea {
    background-color: #ffffff;
    color: #1e293b !important;
    border: 1px solid rgba(148,163,184,0.4);
    border-radius: 0.7rem;
}

/* ===== Info Boxes ===== */
.stInfo, .stWarning, .stError {
    border-radius: 0.8rem !important;
    background-color: #f8fafc !important;
}

/* ===== Footer ===== */
footer {
    visibility: hidden;
}

/* ====== Dark Mode ====== */
@media (prefers-color-scheme: dark) {
    body {
        background-color: #0f172a;
        color: #e2e8f0;
    }
    .main {
        background: linear-gradient(145deg, #0f172a, #1e293b);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.4);
    }
    h1 {
        color: #38bdf8;
        text-shadow: 0 0 10px rgba(56,189,248,0.3);
    }
    [data-testid="stSidebar"] {
        background: #1e293b;
        border-right: 1px solid rgba(148,163,184,0.15);
    }
    .sidebar-title {
        color: #93c5fd;
    }
    [data-testid="stFileUploader"] {
        background: rgba(30, 41, 59, 0.9);
        border: 1px dashed #38bdf8;
        color: #e2e8f0;
    }
    .stChatMessage[data-testid="stChatMessage-user"] {
        background: linear-gradient(145deg, #1e3a8a, #3b82f6);
        color: #ffffff;
    }
    .stChatMessage[data-testid="stChatMessage-assistant"] {
        background: rgba(30, 41, 59, 0.9);
        color: #e2e8f0;
    }
    [data-testid="stChatInputContainer"] {
        background: rgba(15, 23, 42, 0.95);
        border-top: 1px solid rgba(148,163,184,0.2);
    }
    textarea {
        background-color: rgba(30, 41, 59, 0.85);
        color: #e2e8f0 !important;
        border: 1px solid rgba(148,163,184,0.3);
    }
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Initialize Session State
# -------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_user_query" not in st.session_state:
    st.session_state.last_user_query = None

# Clear chat history button in sidebar
if st.sidebar.button("🗑️ Clear Chat History", use_container_width=True):
    st.session_state.chat_history = []
    st.session_state.last_user_query = None
    st.sidebar.success("Chat history cleared!")
    st.rerun()

# -------------------------------
# Main Title
# -------------------------------
st.title("🤖 Smart PDF Chatbot")


st.markdown("""
<div style="
    background: rgba(56,189,248,0.1);
    border: 1px solid rgba(56,189,248,0.3);
    padding: 0.8rem 1rem;
    border-radius: 0.7rem;
    text-align:center;
    color:#93c5fd;
    font-weight:500;
    margin-bottom:1rem;
">
✨ Ask questions from your PDFs — AI will answer only from your documents.
</div>
""", unsafe_allow_html=True)

st.caption("Upload your knowledge base PDFs and ask questions intelligently.")

# -------------------------------
# File Upload Section
# -------------------------------
uploaded_files = st.file_uploader("📥 Upload PDF files", accept_multiple_files=True, type="pdf")

if uploaded_files:
    pdf_paths = []
    os.makedirs("data", exist_ok=True)
    for file in uploaded_files:
        file_path = os.path.join("data", file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        pdf_paths.append(file_path)

    # Initialize persistent pipeline and history manager
    if "pipeline" not in st.session_state or st.session_state.pipeline is None:
        st.session_state.pipeline = RAGPipeline(pdf_paths)
        st.session_state.history_manager = HistoryManager()
        # Load existing history
        st.session_state.chat_history = st.session_state.history_manager.load_history()

    pipeline = st.session_state.pipeline
    history_manager = st.session_state.history_manager

    # -------------------------------
    # Display Previous Chat
    # -------------------------------
    if len(st.session_state.chat_history) == 0:
        st.markdown("<p style='text-align:center; color:gray;'>💬 Start chatting with your PDFs!</p>", unsafe_allow_html=True)
    else:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # -------------------------------
    # Chat Input
    # -------------------------------
    user_query = st.chat_input("💭 Ask a question about your PDFs...")

    if user_query:
        # Avoid duplicate processing on rerun
        if user_query != st.session_state.get("last_user_query", None):
            st.session_state.last_user_query = user_query

            with st.chat_message("user"):
                st.markdown(user_query)

            answer = pipeline.ask(user_query)

            with st.chat_message("assistant"):
                st.markdown(answer)

            # Save to history manager
            history_manager.save_turn("user", user_query)
            history_manager.save_turn("assistant", answer)

            # Update chat history
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
        else:
            st.stop()
else:
    st.info("📘 Upload your PDFs to start chatting. Your session will be saved automatically.")
