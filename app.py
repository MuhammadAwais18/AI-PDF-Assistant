import streamlit as st

from utils.pdf_loader import load_pdf
from utils.embeddings import create_vector_store
from utils.chat import process_chat
from utils.database import (
    create_database,
    get_history,
    clear_history
)
# ---------------------------------------
# Page Configuration
# ---------------------------------------

st.set_page_config(
    page_title="AI PDF Chat (RAG)",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------
# Database
# ---------------------------------------

create_database()

# ---------------------------------------
# Session State
# ---------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "current_pdf" not in st.session_state:
    st.session_state.current_pdf = None

# ---------------------------------------
# Header
# ---------------------------------------

st.title("📄 AI PDF Chat (RAG)")

st.caption(
    "Upload a PDF and ask intelligent questions using AI and Retrieval-Augmented Generation."
)

# ---------------------------------------
# Sidebar
# ---------------------------------------

with st.sidebar:

    st.header("📁 Upload PDF")

    uploaded_files = st.file_uploader(
        "Choose PDF file(s)",
        type=["pdf"],
        accept_multiple_files=True
    )

    st.divider()

    st.header("📜 Previous Chats")

    @st.cache_data
    def load_chat_history():
        return get_history()

    history = load_chat_history()

    if history:

        for question, answer, created_at in history[:10]:

            with st.expander(created_at):

                st.markdown(f"**Q:** {question}")

                st.markdown(f"**A:** {answer}")

    else:

        st.info("No chat history found.")

    st.divider()

    st.header("ℹ️ About")

    st.info(
        """
AI PDF Chat lets you upload documents,
search them semantically using FAISS,
and ask questions powered by OpenRouter AI.
"""
    )

    st.divider()

    st.subheader("🗑 Chat")

    if st.button(
      "Clear Chat",
      use_container_width=True
     ):

      clear_history()

      st.session_state.messages = []

      st.rerun()

# ---------------------------------------
# PDF Processing
# ---------------------------------------
if uploaded_files:

    current_pdf_names = sorted(
        [file.name for file in uploaded_files]
    )

    if st.session_state.current_pdf != current_pdf_names:

        combined_text = ""

        with st.spinner("Reading PDF(s)..."):

            for file in uploaded_files:

                combined_text += (
                    "\n\n"
                    f"========== {file.name} ==========\n\n"
                )

                combined_text += load_pdf(file)

        with st.spinner("Creating Vector Database..."):

            vectorstore = create_vector_store(
                combined_text
            )

        st.session_state.vectorstore = vectorstore

        st.session_state.current_pdf = current_pdf_names

        st.session_state.messages = []

        st.success(
            f"{len(uploaded_files)} PDF(s) processed successfully."
        )

else:

    st.info("👈 Upload one or more PDFs from the sidebar.")

    st.stop()


# ---------------------------------------
# Chat Interface
# ---------------------------------------

st.divider()

st.subheader("💬 Chat with your PDF")

# Display previous chat messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# Chat input
question = st.chat_input(
    "Ask anything about your PDF..."
)

if question:

    # Store user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            answer = process_chat(
                st.session_state.vectorstore,
                question
            )

        placeholder = st.empty()

        streamed_text = ""

        for word in answer.split():

            streamed_text += word + " "

            placeholder.markdown(streamed_text + "▌")

            import time

            time.sleep(0.03)

        placeholder.markdown(streamed_text)
        
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )
# ---------------------------------------
# Sidebar Status
# ---------------------------------------

with st.sidebar:

    st.divider()

    st.header("📄 Current PDF")

    if st.session_state.current_pdf:

        if isinstance(
            st.session_state.current_pdf,
            list
        ):

            st.success(
                f"{len(st.session_state.current_pdf)} PDF(s) Loaded"
            )

            for pdf in st.session_state.current_pdf:

                st.write(f"📄 {pdf}")

        else:

            st.success(
                st.session_state.current_pdf
            )

    else:

        st.info("No PDF uploaded.")

# ---------------------------------------
# Statistics
# ---------------------------------------

st.divider()

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Messages",
        len(st.session_state.messages)
    )

with col2:

    if st.session_state.vectorstore:

        st.metric(
            "Vector Database",
            "Ready ✅"
        )

    else:

        st.metric(
            "Vector Database",
            "Not Ready ❌"
        )

# ---------------------------------------
# Footer
# ---------------------------------------

st.divider()

st.caption(
    """
Built with ❤️ using

• Streamlit

• LangChain

• FAISS

• HuggingFace Embeddings

• OpenRouter AI

• SQLite
"""
)