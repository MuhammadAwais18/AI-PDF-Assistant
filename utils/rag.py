import os

from openai import OpenAI
from dotenv import load_dotenv

from utils.retriever import retrieve_documents

load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)


MODEL = os.getenv("MODEL")


def ask_pdf(
    vectorstore,
    question,
    history=""
):
    """
    Retrieve relevant PDF context and generate AI answer.
    """

    try:

        if vectorstore is None:
            return "❌ No PDF processed. Please upload a PDF first."

        if not question.strip():
            return "❌ Please enter a question."


        docs = retrieve_documents(
            vectorstore,
            question,
            k=4
        )


        if not docs:
            return "I couldn't find relevant information in the PDF."

        sources = sorted(
            {
                (
                    doc.metadata.get("file", "Unknown"),
                    doc.metadata.get("page", "?")
                )
            for doc in docs
            }
        )

        context = "\n\n".join(
            doc.page_content
            for doc in docs
        )


        prompt = f"""
You are an AI PDF Assistant.

You are chatting with the user.

Use the previous conversation whenever it helps answer follow-up questions.

Only answer using the uploaded PDF context.

If the answer is not available in the PDF, reply:

"I couldn't find that information in the uploaded PDF."

PDF Context:

{context}

Conversation History:

{history}

Current Question:

{question}
"""

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=512
        )
        


        if not response:
            return "❌ No response received from AI."


        if not response.choices:
            return "❌ AI returned no answer."


        answer = response.choices[0].message.content

        if not answer:
            return "❌ AI returned an empty response."

        answer += "\n\n---\n📚 **Sources**\n"

        for file_name, page in sources:

            answer += (
                f"\n📄 **{file_name}** — Page {page}"
            )

        if not answer:
            return "❌ Empty AI response."


        return answer


    except Exception as e:

        return f"❌ AI Error: {str(e)}"