from utils.rag import ask_pdf
from utils.database import save_chat


def process_chat(vectorstore, question):
    """
    Process user question through RAG
    and save conversation history.
    """

    try:

        if vectorstore is None:
            return "❌ Please upload and process a PDF first."


        if not question.strip():
            return "❌ Question cannot be empty."


        answer = ask_pdf(
            vectorstore,
            question
        )


        save_chat(
            question,
            answer
        )


        return answer


    except Exception as e:

        return f"❌ Chat Error: {str(e)}"