<<<<<<< HEAD
# Skill: High-Precision NCERT Extraction & Interactive Labeling

## Phase 1: NCERT Image Retrieval
- *Action:* Use fitz to parse local PDFs or BeautifulSoup to scrape the official NCERT repository.
- *Logic:* Search for the specific figure or diagram that matches the user's topic (e.g., "Refraction of Light").
- *Accuracy:* The image must be the official diagram from the NCERT textbook, not a generic placeholder.

## Phase 2: Interactive Labeling
- *Mapping:* Identify the text labels inside the extracted NCERT image.
- *UI:* Create clickable "hotspots" over these labels using a transparent HTML overlay.
=======
# Skill: High-Precision NCERT Extraction & Interactive Labeling

## Phase 1: NCERT Image Retrieval
- *Action:* Use fitz to parse local PDFs or BeautifulSoup to scrape the official NCERT repository.
- *Logic:* Search for the specific figure or diagram that matches the user's topic (e.g., "Refraction of Light").
- *Accuracy:* The image must be the official diagram from the NCERT textbook, not a generic placeholder.

## Phase 2: Interactive Labeling
- *Mapping:* Identify the text labels inside the extracted NCERT image.
- *UI:* Create clickable "hotspots" over these labels using a transparent HTML overlay.
>>>>>>> 7a16fead81d78061ecb1a77ea6528f87c946d5f5
- *Explanation:* When clicked, show a brief, high-accuracy explanation of that specific label (e.g., "What is an Incident Ray?") in a dark-themed popover.