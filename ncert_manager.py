import os
import requests
import fitz  # PyMuPDF
from PIL import Image
import io

# --- CONFIGURATION ---
NCERT_BASE_URL = "https://ncert.nic.in/textbook/pdf/"
STORAGE_DIR = "ncert_books"

# --- MAPPING (Simplified for Major Subjects) ---
# Format: {Class: {Subject: "BookCode"}}
# BookCode usually follows: 
# Class 9 Science: iesc1
# Class 10 Science: jesc1
# Class 11 Physics: keph1 (Part 1), keph2 (Part 2)
# Class 12 Physics: leph1 (Part 1), leph2 (Part 2)

BOOK_CODES = {
    "9": {
        "Science": "iesc1",
        "Maths": "iemh1",
        "Social Science": "iess", # This is complex, split into history/geo etc. ignoring for now or using generic
    },
    "10": {
        "Science": "jesc1",
        "Maths": "jemh1",
    },
    "11": {
        "Physics": "keph1", # Part 1 default
        "Chemistry": "kech1",
        "Biology": "kebo1",
        "Maths": "kemh1",
    },
    "12": {
        "Physics": "leph1", # Part 1 default
        "Chemistry": "lech1",
        "Biology": "lebo1",
        "Maths": "lemh1",
    }
}

CLASS_10_SCIENCE_CHAPTERS = {
    "Chemical Reactions and Equations": 1,
    "Acids, Bases and Salts": 2,
    "Metals and Non-metals": 3,
    "Carbon and its Compounds": 4,
    "Life Processes": 5,
    "Control and Coordination": 6,
    "How do Organisms Reproduce?": 7,
    "Heredity": 8,
    "Light – Reflection and Refraction": 9,
    "The Human Eye and the Colourful World": 10,
    "Electricity": 11,
    "Magnetic Effects of Electric Current": 12,
    "Our Environment": 13
}

CLASS_9_SCIENCE_CHAPTERS = {
    "Matter in Our Surroundings": 1,
    "Is Matter Around Us Pure": 2,
    "Atoms and Molecules": 3,
    "Structure of the Atom": 4,
    "The Fundamental Unit of Life": 5,
    "Tissues": 6,
    "Motion": 7,
    "Force and Laws of Motion": 8,
    "Gravitation": 9,
    "Work and Energy": 10,
    "Sound": 11,
    "Improvement in Food Resources": 12
}


# --- CLASS 11 MAPPINGS (Rationalized 2024-25) ---
CLASS_11_PHYSICS_CHAPTERS = {
    "Units and Measurements": 1,
    "Motion in a Straight Line": 2,
    "Motion in a Plane": 3,
    "Laws of Motion": 4,
    "Work, Energy and Power": 5,
    "System of Particles and Rotational Motion": 6,
    "Gravitation": 7,
    "Mechanical Properties of Solids": 8,
    "Mechanical Properties of Fluids": 9,
    "Thermal Properties of Matter": 10,
    "Thermodynamics": 11,
    "Kinetic Theory": 12,
    "Oscillations": 13,
    "Waves": 14
}

CLASS_11_CHEMISTRY_CHAPTERS = {
    "Some Basic Concepts of Chemistry": 1,
    "Structure of Atom": 2,
    "Classification of Elements and Periodicity in Properties": 3,
    "Chemical Bonding and Molecular Structure": 4,
    "Thermodynamics": 5,
    "Equilibrium": 6,
    "Redox Reactions": 7,
    "Organic Chemistry - Some Basic Principles and Techniques": 8,
    "Hydrocarbons": 9
}

CLASS_11_BIOLOGY_CHAPTERS = {
    "The Living World": 1,
    "Biological Classification": 2,
    "Plant Kingdom": 3,
    "Animal Kingdom": 4,
    "Morphology of Flowering Plants": 5,
    "Anatomy of Flowering Plants": 6,
    "Structural Organisation in Animals": 7,
    "Cell: The Unit of Life": 8,
    "Biomolecules": 9,
    "Cell Cycle and Cell Division": 10,
    "Photosynthesis in Higher Plants": 11,
    "Respiration in Plants": 12,
    "Plant Growth and Development": 13,
    "Breathing and Exchange of Gases": 14,
    "Body Fluids and Circulation": 15,
    "Excretory Products and their Elimination": 16,
    "Locomotion and Movement": 17,
    "Neural Control and Coordination": 18,
    "Chemical Coordination and Integration": 19
}

# --- CLASS 12 MAPPINGS (Rationalized 2024-25) ---
CLASS_12_PHYSICS_CHAPTERS = {
    "Electric Charges and Fields": 1,
    "Electrostatic Potential and Capacitance": 2,
    "Current Electricity": 3,
    "Moving Charges and Magnetism": 4,
    "Magnetism and Matter": 5,
    "Electromagnetic Induction": 6,
    "Alternating Current": 7,
    "Electromagnetic Waves": 8,
    "Ray Optics and Optical Instruments": 9,
    "Wave Optics": 10,
    "Dual Nature of Radiation and Matter": 11,
    "Atoms": 12,
    "Nuclei": 13,
    "Semiconductor Electronics": 14
}

CLASS_12_CHEMISTRY_CHAPTERS = {
    "Solutions": 1,
    "Electrochemistry": 2,
    "Chemical Kinetics": 3,
    "The d- and f- Block Elements": 4,
    "Coordination Compounds": 5,
    "Haloalkanes and Haloarenes": 6,
    "Alcohols, Phenols and Ethers": 7,
    "Aldehydes, Ketones and Carboxylic Acids": 8,
    "Amines": 9,
    "Biomolecules": 10
}

CLASS_12_BIOLOGY_CHAPTERS = {
    "Sexual Reproduction in Flowering Plants": 1,
    "Human Reproduction": 2,
    "Reproductive Health": 3,
    "Principles of Inheritance and Variation": 4,
    "Molecular Basis of Inheritance": 5,
    "Evolution": 6,
    "Human Health and Disease": 7,
    "Microbes in Human Welfare": 8,
    "Biotechnology: Principles and Processes": 9,
    "Biotechnology and its Applications": 10,
    "Organisms and Populations": 11,
    "Ecosystem": 12,
    "Biodiversity and Conservation": 13
}

def get_class_10_science_chapters(): return list(CLASS_10_SCIENCE_CHAPTERS.keys())
def get_class_9_science_chapters(): return list(CLASS_9_SCIENCE_CHAPTERS.keys())
def get_class_11_physics_chapters(): return list(CLASS_11_PHYSICS_CHAPTERS.keys())
def get_class_11_chemistry_chapters(): return list(CLASS_11_CHEMISTRY_CHAPTERS.keys())
def get_class_11_biology_chapters(): return list(CLASS_11_BIOLOGY_CHAPTERS.keys())
def get_class_12_physics_chapters(): return list(CLASS_12_PHYSICS_CHAPTERS.keys())
def get_class_12_chemistry_chapters(): return list(CLASS_12_CHEMISTRY_CHAPTERS.keys())

# --- MATH CHAPTERS ---
CLASS_9_MATH_CHAPTERS = {
    "Number Systems": 1, "Polynomials": 2, "Coordinate Geometry": 3, "Linear Equations in Two Variables": 4, 
    "Introduction to Euclid's Geometry": 5, "Lines and Angles": 6, "Triangles": 7, "Quadrilaterals": 8, 
    "Circles": 9, "Heron's Formula": 10, "Surface Areas and Volumes": 11, "Statistics": 12
}

CLASS_10_MATH_CHAPTERS = {
    "Real Numbers": 1, "Polynomials": 2, "Pair of Linear Equations in Two Variables": 3, "Quadratic Equations": 4, 
    "Arithmetic Progressions": 5, "Triangles": 6, "Coordinate Geometry": 7, "Introduction to Trigonometry": 8, 
    "Some Applications of Trigonometry": 9, "Circles": 10, "Areas Related to Circles": 11, 
    "Surface Areas and Volumes": 12, "Statistics": 13, "Probability": 14
}

CLASS_11_MATH_CHAPTERS = {
    "Sets": 1, "Relations and Functions": 2, "Trigonometric Functions": 3, "Complex Numbers and Quadratic Equations": 4, 
    "Linear Inequalities": 5, "Permutations and Combinations": 6, "Binomial Theorem": 7, "Sequences and Series": 8, 
    "Straight Lines": 9, "Conic Sections": 10, "Introduction to Three Dimensional Geometry": 11, 
    "Limits and Derivatives": 12, "Statistics": 13, "Probability": 14
}

CLASS_12_MATH_CHAPTERS = {
    "Relations and Functions": 1, "Inverse Trigonometric Functions": 2, "Matrices": 3, "Determinants": 4, 
    "Continuity and Differentiability": 5, "Applications of Derivatives": 6, "Integrals": 7, 
    "Application of Integrals": 8, "Differential Equations": 9, "Vector Algebra": 10, 
    "Three Dimensional Geometry": 11, "Linear Programming": 12, "Probability": 13
}

def get_class_9_math_chapters(): return list(CLASS_9_MATH_CHAPTERS.keys())
def get_class_10_math_chapters(): return list(CLASS_10_MATH_CHAPTERS.keys())
def get_class_11_math_chapters(): return list(CLASS_11_MATH_CHAPTERS.keys())
def get_class_12_math_chapters(): return list(CLASS_12_MATH_CHAPTERS.keys())
def get_class_12_biology_chapters(): return list(CLASS_12_BIOLOGY_CHAPTERS.keys())

def get_book_code(class_grade, subject, chapter_num=1):
    """
    Returns the NCERT book code based on class, subject, and chapter.
    """
    import re
    
    # 1. Normalize Class Input (e.g., "10th Grade" -> "10")
    class_str = str(class_grade).strip()
    class_match = re.search(r'\d+', class_str)
    if class_match:
        class_grade = class_match.group()
    else:
        # Fallback or keep as is if no digits found (though likely invalid)
        class_grade = class_str

    subject = subject.lower()
    
    # 2. Normalize Chapter Input (e.g., "Chapter 1" -> 1)
    chap_str = str(chapter_num).strip()
    chap_match = re.search(r'\d+', chap_str)
    if chap_match:
        chapter_num = int(chap_match.group())
    else:
        # Default to 1 if parsing fails
        chapter_num = 1
    
    if class_grade == "10":
        if "science" in subject: return "jesc1", chapter_num
        if "math" in subject: return "jemh1", chapter_num
        if "english" in subject: return "jefp1", chapter_num # First Flight
    
    elif class_grade == "9":
        if "science" in subject: return "iesc1", chapter_num
        if "math" in subject: return "iemh1", chapter_num

    elif class_grade == "11":
        if "physics" in subject:
            # Part 1: Ch 1-8, Part 2: Ch 9-14 (Reset to 1)
            return ("keph1", chapter_num) if chapter_num <= 8 else ("keph2", chapter_num - 8)
        if "chemistry" in subject:
            # Part 1: Ch 1-6, Part 2: Ch 7-X (Reset to 1)
            return ("kech1", chapter_num) if chapter_num <= 6 else ("kech2", chapter_num - 6) 
        if "biology" in subject: return "kebo1", chapter_num

    elif class_grade == "12":
        if "physics" in subject:
            # Part 1: Ch 1-8, Part 2: Ch 9-14 (Reset to 1)
            return ("leph1", chapter_num) if chapter_num <= 8 else ("leph2", chapter_num - 8)
        if "chemistry" in subject:
            # Part 1: Ch 1-5, Part 2: Ch 6-10 (Reset to 1)
            return ("lech1", chapter_num) if chapter_num <= 5 else ("lech2", chapter_num - 5)
        if "biology" in subject: return "lebo1", chapter_num
            
    return None

def download_ncert_pdf(class_grade, subject, chapter_num):
    """
    Downloads the specific chapter PDF from NCERT website.
    """
    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)

    book_code, final_chapter_num = get_book_code(class_grade, subject, chapter_num)
    if not book_code:
        return None, "Book code not found for this Class/Subject."

    # Format chapter number (e.g., 1 -> 01)
    chap_str = str(final_chapter_num).zfill(2)
    
    # Construct Filename and URL
    # Pattern: [book_code][chapter].pdf -> jesc101.pdf
    pdf_name = f"{book_code}{chap_str}.pdf"
    file_path = os.path.join(STORAGE_DIR, pdf_name)
    
    # URL construction
    url = f"{NCERT_BASE_URL}{pdf_name}"
    
    # Check if already exists
    if os.path.exists(file_path):
        return file_path, "Loaded from cache."
    
    # Download with Retry Logic
    import time
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
            # Use short timeout only for connect, longer for read
            response = requests.get(url, stream=True, headers=headers, timeout=(5, 20))
            
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                return file_path, "Download successful."
            elif response.status_code == 404:
                 return None, f"Chapter not found (404). URL: {url}"
            else:
                if attempt < max_retries - 1:
                    time.sleep(1) # Wait before retry
                    continue
                return None, f"Failed to download. Status: {response.status_code}"
                
        except (requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError, requests.exceptions.Timeout) as e:
            if attempt < max_retries - 1:
                print(f"Download error {e}. Retrying ({attempt+1}/{max_retries})...")
                time.sleep(2)
            else:
                return None, f"Network Error after retries: {e}"
        except Exception as e:
            return None, f"Error: {e}"
            
    return None, "Download failed after retries."

def extract_relevant_image(pdf_path, topic_keywords):
    """
    Scans the PDF for the best matching image based on nearby text.
    Returns: PIL Image object or None
    """
    if not pdf_path or not os.path.exists(pdf_path):
        return None

    doc = fitz.open(pdf_path)
    best_image = None
    best_score = 0
    
    keywords = topic_keywords.lower().split()

    # Combined Logic:
    # 1. Page Scoring: Find pages with keyword matches
    # 2. Image Filtering: On candidate pages, check images for size and content (not blank/black)
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text").lower()
        
        # Scoring based on keyword frequency
        score = sum(text.count(k) for k in keywords)
        
        # Bonus: Look for "Fig." or "Figure" roughly on the page
        if "fig" in text or "figure" in text:
            score += 2
            
        if score > best_score:
            # Check images on this page
            image_list = page.get_images(full=True)
            if image_list:
                max_size = 0  # Initialize max_size for this page's images
                # Iterate through images on this high-scoring page
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    
                    # Filter 1: Size (Skip very small icons)
                    if len(image_bytes) < 1000: # Lowered to ~1KB
                        continue
                        
                    try:
                        pil_img = Image.open(io.BytesIO(image_bytes))
                        
                        # Filter 2: Dimensions (Skip thin strips)
                        w, h = pil_img.size
                        if w < 50 or h < 50:
                            continue
                            
                        # Filter 3: Content (Skip blank/black/uniform images)
                        # Convert to grayscale and calculate variance
                        if pil_img.mode == "CMYK":
                            pil_img = pil_img.convert("RGB")
                            
                        img_gray = pil_img.convert("L")
                        stat = img_gray.getextrema()
                        if stat[0] == stat[1]: # Completely uniform color (black or white)
                            continue
                            
                        # If we passed all filters, this is a candidate
                        # We pick the largest valid image from the highest scoring page
                        if len(image_bytes) > max_size:
                            max_size = len(image_bytes)
                            best_image = pil_img
                            best_score = score
                    except Exception:
                        continue

    return best_image

def download_all_class_10_science():
    """
    Downloads all chapters for Class 10 Science.
    """
    results = []
    print("Starting Bulk Download for Class 10 Science...")
    for chapter_name, chapter_num in CLASS_10_SCIENCE_CHAPTERS.items():
        print(f"Downloading: {chapter_name} (Chapter {chapter_num})...")
        path, msg = download_ncert_pdf("10", "Science", str(chapter_num))
        results.append(f"{chapter_name}: {msg}")
    return results

def download_all_class_9_science():
    """
    Downloads all chapters for Class 9 Science.
    """
    results = []
    print("Starting Bulk Download for Class 9 Science...")
    for chapter_name, chapter_num in CLASS_9_SCIENCE_CHAPTERS.items():
        print(f"Downloading: {chapter_name} (Chapter {chapter_num})...")
        path, msg = download_ncert_pdf("9", "Science", str(chapter_num))
        results.append(f"{chapter_name}: {msg}")
    return results

def download_class_11_pcmb():
    results = []
    print("Downloading Class 11 Physics...")
    for name, num in CLASS_11_PHYSICS_CHAPTERS.items():
        path, msg = download_ncert_pdf("11", "Physics", str(num))
        results.append(f"11-Phy-{name}: {msg}")
    
    print("Downloading Class 11 Chemistry...")
    for name, num in CLASS_11_CHEMISTRY_CHAPTERS.items():
        path, msg = download_ncert_pdf("11", "Chemistry", str(num))
        results.append(f"11-Chem-{name}: {msg}")
        
    print("Downloading Class 11 Biology...")
    for name, num in CLASS_11_BIOLOGY_CHAPTERS.items():
        path, msg = download_ncert_pdf("11", "Biology", str(num))
        results.append(f"11-Bio-{name}: {msg}")
    return results

def download_class_12_pcmb():
    results = []
    print("Downloading Class 12 Physics...")
    for name, num in CLASS_12_PHYSICS_CHAPTERS.items():
        path, msg = download_ncert_pdf("12", "Physics", str(num))
        results.append(f"12-Phy-{name}: {msg}")
        
    print("Downloading Class 12 Chemistry...")
    for name, num in CLASS_12_CHEMISTRY_CHAPTERS.items():
        path, msg = download_ncert_pdf("12", "Chemistry", str(num))
        results.append(f"12-Chem-{name}: {msg}")
        
    print("Downloading Class 12 Biology...")
    for name, num in CLASS_12_BIOLOGY_CHAPTERS.items():
        path, msg = download_ncert_pdf("12", "Biology", str(num))
        results.append(f"12-Bio-{name}: {msg}")
    return results