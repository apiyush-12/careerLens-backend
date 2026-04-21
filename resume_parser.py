import pdfplumber

def extract_text_from_pdf(file_path):

    text = ""

    try:
        with pdfplumber.open(file_path) as pdf:

            for page in pdf.pages:
                try:
                    extracted = page.extract_text()

                    if extracted:
                        text += extracted + "\n"

                except Exception as page_error:
                    print("Page error:", page_error)
                    continue

    except Exception as e:
        print("PDF open error:", e)

    return text.strip()