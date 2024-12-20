import PyPDF2

def extract_pdf_content(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Get the number of pages
            num_pages = len(pdf_reader.pages)
            print(f"Number of pages: {num_pages}")
            
            # Extract text from all pages
            content = ""
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                content += page.extract_text()
            
            return content
            
    except Exception as e:
        print(f"Error reading PDF: {str(e)}")
        return None

if __name__ == "__main__":
    pdf_path = "TimeTable Project Details.pdf"
    content = extract_pdf_content(pdf_path)
    
    if content:
        print("\nPDF Content:")
        print("-" * 50)
        print(content)
        print("-" * 50)
