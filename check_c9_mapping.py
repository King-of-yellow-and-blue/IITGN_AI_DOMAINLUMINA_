
import fitz
import os

pdf_path = "ncert_books/iesc107.pdf"

if os.path.exists(pdf_path):
    doc = fitz.open(pdf_path)
    # Load first page only for title
    text = doc.load_page(0).get_text()
    
    print(f"--- HEAD of {pdf_path} ---")
    print(text[:1000])
    
    if "Diversity" in text:
        print("DETECTED: Diversity (Old Ch 7)")
    elif "Motion" in text:
        print("DETECTED: Motion (New Ch 7 / Old Ch 8)")
    elif "Force" in text:
        print("DETECTED: Force (New Ch 8 / Old Ch 9)")
    else:
        print("Title not found in first page.")
else:
    print("iesc107.pdf not found.")
