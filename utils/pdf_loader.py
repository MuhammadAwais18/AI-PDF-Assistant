from pypdf import PdfReader


def load_pdf(file) -> str:
    """
    Extract text from uploaded PDF file.
    """

    try:

        reader = PdfReader(file)

        pages = []

        for page_number, page in enumerate(reader.pages, start=1):

            text = page.extract_text()

            if text and text.strip():

                pages.append(
                    f"\n[FILE:{file.name}]\n"
                    f"[Page {page_number}]\n"
                    f"{text}"
                )

        if not pages:

            return ""


        return "\n".join(pages)


    except Exception as e:

        raise Exception(
            f"PDF reading failed: {str(e)}"
        )