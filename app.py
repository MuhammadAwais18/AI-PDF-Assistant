import streamlit as st

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="AI PDF Chat (RAG)",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# Session State
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False

# ----------------------------
# Header
# ----------------------------
st.title("📄 AI PDF Chat (RAG)")
st.caption(
    "Upload a PDF and ask questions using Retrieval-Augmented Generation (RAG)."
)

# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    st.header("📁 Upload PDF")

    uploaded_file = st.file_uploader(
        "Choose a PDF",
        type=["pdf"]
    )

    st.divider()

    st.header("ℹ️ About")

    st.info(
        "This application allows you to chat with your PDF "
        "using AI, semantic search, and Retrieval-Augmented Generation (RAG)."
    )

# ----------------------------
# Main Area
# ----------------------------
if uploaded_file is None:
    st.info("👈 Upload a PDF from the sidebar to begin.")
    st.stop()

st.success(f"Loaded: {uploaded_file.name}")

st.divider()

st.subheader("💬 Chat")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_question = st.chat_input(
    "Ask a question about your PDF..."
)

if user_question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        st.info(
            "RAG pipeline will be connected in the next step."
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": "RAG pipeline will be connected in the next step."
        }
    )