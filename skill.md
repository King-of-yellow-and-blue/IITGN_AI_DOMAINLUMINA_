# Skill: Phased NCERT Extraction & Interactive Labeling

## STEP 1: Accurate NCERT Extraction (Primary Focus)
- *High-Precision Search:* Use fitz (PyMuPDF) and BeautifulSoup to scan NCERT repositories or local folders.
- *Matching Logic:* - The Agent must analyze the current topic (e.g., "Refraction through a Prism").
  - It must cross-reference image captions and "Figure" numbers in the NCERT text to find the exact match.
- *Resolution:* Extract the highest-quality version using PIL.
- *Success Criteria:* The user must see the exact diagram found in the official NCERT textbook for that chapter.

## STEP 2: Interactive Label Implementation (Secondary Focus)
- *Requirement:* Trigger this ONLY after the image from Step 1 is successfully displayed in the "Visual Way" box.
- *Label Mapping:* Detect text within the NCERT image (e.g., "Prism," "Incident Ray").
- *Interaction Logic:*
  - On clicking a label, display a non-intrusive tooltip.
  - The explanation must be a "Short Concept Summary" derived from the physics/subject logic in app.py.
  - Use Tailwind CSS for a sleek, dark-themed popover.