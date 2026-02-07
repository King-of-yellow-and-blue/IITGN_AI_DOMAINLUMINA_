
import ncert_manager
from PIL import Image
import os

# Test on Class 10 Ch 10 (Light) - known good
pdf_path = "ncert_books/jesc110.pdf" 
topic = "Concave Mirror"

print(f"Testing extraction on {pdf_path} for '{topic}'...")

if os.path.exists(pdf_path):
    img = ncert_manager.extract_relevant_image(pdf_path, topic)
    if img:
        print(f"Success! Image extracted.")
        print(f"Size: {img.size}")
        print(f"Format: {img.format}")
        # Save for manual inspection if needed, or just trust the filters
        img.save("test_extracted_img.png")
        print("Saved to test_extracted_img.png")
    else:
        print("Failed to extract image (or filtered out).")
else:
    print("PDF not found.")
