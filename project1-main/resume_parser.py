import pdfplumber

def extract_text_from_resume(pdf_path):
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


if __name__ == "__main__":

    # path of resume
    resume_path = "uploads/resumes/sample_resume.pdf"

    # extract text
    extracted_text = extract_text_from_resume(resume_path)

    print("----- RESUME TEXT -----\n")
    print(extracted_text)