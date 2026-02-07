import streamlit as st
import google.generativeai as genai
import ncert_manager
import os
from streamlit_mic_recorder import speech_to_text


# --- 1. CONFIGURATION & PREMIUM UI/UX ENGINE ---
st.set_page_config(page_title="LUMINA AI", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    /* Import Premium Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@400;600&display=swap');

    /* Global Theme Overrides */
    .stApp {
        background-color: #0b0f1a !important;
        font-family: 'Inter', sans-serif;
    }

    /* 1. PREMIUM TITLE ARCHITECTURE */
    .main-title {
        background: linear-gradient(135deg, #60A5FA 0%, #A855F7 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.8rem !important;
        font-weight: 850 !important;
        text-align: center;
        letter-spacing: -1.5px;
        padding-top: 40px !important;
        padding-bottom: 20px !important;
        filter: drop-shadow(0px 10px 20px rgba(96, 165, 250, 0.2));
    }

    /* 2. SIDEBAR GLASSMORPHISM & SPACING */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.98) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    [data-testid="stSidebar"] * { color: #E2E8F0 !important; }
    div[data-testid="stSidebarNav"] li { margin: 8px 0px; border-radius: 10px; }

    /* 3. PREMIUM FLASHCARD & GLASS SYSTEM */
    div[data-testid="stVerticalBlock"] > div[style*="border"], 
    div.stMarkdown div[style*="background-color"],
    .stExpander {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(16px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(16px) saturate(180%) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 24px !important;
        padding: 25px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4) !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        margin-bottom: 15px !important;
    }

    .stExpander:hover {
        transform: translateY(-5px) scale(1.005);
        border: 1px solid rgba(96, 165, 250, 0.4) !important;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6) !important;
    }

    /* 4. KEYWORD HIGHLIGHTING (Replaced Pill Badges with Blue Bold) */
    strong {
        color: #60A5FA !important; /* Lumina Blue */
        font-weight: 700 !important;
        text-shadow: 0px 0px 8px rgba(96, 165, 250, 0.3); /* Subtle glow */
    }

    /* 5. READABILITY SHIELD */
    div[style*="background-color"] p, 
    div[style*="background-color"] li,
    div[style*="background-color"] span {
        color: #F8FAFC !important;
        line-height: 1.8 !important;
        font-size: 1.05rem !important;
    }

    /* 6. ELITE BUTTON DESIGN */
    .stButton>button {
        width: 100%; border-radius: 12px !important; height: 55px !important; 
        font-weight: 700 !important; 
        background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%) !important; 
        color: white !important; border: 1px solid rgba(255, 255, 255, 0.1) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3) !important;
        text-transform: uppercase; letter-spacing: 1.2px;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%) !important;
        transform: translateY(-4px);
        box-shadow: 0 12px 25px rgba(124, 58, 237, 0.5) !important;
    }

    /* 7. BRANDED SLIDER TRACK */
    .stSlider [data-baseweb="slider"] > div > div {
        background: linear-gradient(90deg, #2563EB 0%, #A855F7 100%) !important;
    }
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background-color: #FFFFFF !important;
        border: 2px solid #2563EB !important;
    }

    /* 8. INPUT FIELD ENHANCEMENT */
    .stTextInput input, .stSelectbox div, .stTextArea textarea {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        color: white !important;
    }

    /* 9. CBSE TOPPER'S BOX */
    .topper-box {
        background: rgba(254, 243, 199, 0.1) !important;
        padding: 20px; border-radius: 12px; border-left: 5px solid #F59E0B;
        color: #FDE68A !important; backdrop-filter: blur(5px);
    }

    .section-header {
        font-size: 1.8rem; 
        background: linear-gradient(90deg, #60A5FA, #A855F7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        border-bottom: 2px solid rgba(96, 165, 250, 0.3); padding-bottom: 10px; margin-top: 40px;
    }

    
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR SETUP ---
with st.sidebar:
    st.title("LUMINA 🧠")
    st.caption("Learning, Understanding & Mastery through Intelligent Neural Architecture")
    
    # Secure API Key Input
    # Secure API Key Input (Hardcoded for Backend)
    # api_key = st.text_input("Enter Google Gemini API Key", type="password")
    api_key = "AIzaSyCqNX4Pq11bQXrku54AT_rNhQrNSFZ87-w"
    
    # if not api_key:
    #     st.warning("⚠️ Paste API Key to Start")
    #     st.stop()
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash-lite')

    st.markdown("---")
    mode = st.radio("Select Mode", [
        "📚 Learning Path", 
        "📝 Exam Generator", 
        "🔍 Thinking Debugger",
        "🗂️ Flashcards",
        "🧠 Concept Transfer Intelligence (CTI)",
        "🔢 Arithmetic Solving",
    ])

# --- AI FUNCTION ---
def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# --- HELP GUIDE COMPONENT ---
def render_help_guide():
    with st.popover("❓", use_container_width=True):
        st.markdown("""
        ### 🌟 How to use LUMINA
        
        **1. 📚 Learning Path**
        - **Goal:** Deep understanding of a specific topic.
        - **Math Mode:** Generates formulas & mental models (No PDF).
        - **Science Mode:** Fetches NCERT diagrams + AI Visuals.
        - **Cognitive Depth:** Choose 'Short', 'Assessment', or 'Long' to tune the explanation.

        **2. 📝 Exam Generator**
        - **Goal:** Practice writing high-scoring answers.
        - **Input:** Speak or type a question.
        - **Marks:** Select 2, 3, 5, or 7 marks for CBSE-style structure.
        - **Output:** Textbook-accurate answer + Marking Scheme.

        **3. 🔍 Thinking Debugger**
        - **Goal:** Fix misconceptions.
        - **Action:** Type a concept (even if wrong).
        - **Result:** AI finds the "Logic Gap" and corrects it.

        **4. 🗂️ Flashcards**
        - **Goal:** Quick revision.
        - **Action:** Enter a topic -> Get 5 Q&A cards.
        
        **5. 🧠 CTI (Viva)**
        - **Goal:** Test your conviction.
        - **Action:** Enter the "Interview Room". The AI Examiner will cross-question you.

        **6. 🔢 Arithmetic Solving**
        - **Goal:** Solve mathematical problems.
        - **Action:** Enter a problem and get a step-by-step solution.
        """)

# --- MAIN LAYOUT LOGIC ---
# Place the Help button at the very top right using columns
# We use a large ratio to push the button to the edge
h_col1, h_col2 = st.columns([15, 1])
with h_col2:
    render_help_guide()

# --- MODE 1: LEARNING PATH (The Final Optimized Master Rebuild) ---
if mode == "📚 Learning Path":
    st.markdown('<div class="main-title">LUMINA Learning Path</div>', unsafe_allow_html=True)
    
    # 1. Input Section
    col1, col2, col3 = st.columns(3)
    user_class = col1.selectbox("Class", ["9th", "10th", "11th", "12th"])
    
    # Conditional Subject Logic
    if user_class in ["9th", "10th"]:
        sub_options = ["Science", "Mathematics"]
    else:
        sub_options = ["Physics", "Chemistry", "Biology", "Mathematics"]
        
    subject = col2.selectbox("Subject", sub_options)
    
    # Enhanced Chapter Selection
    # Class 10
    if user_class and "10" in user_class:
        if "science" in subject.lower():
            chapter_names = ncert_manager.get_class_10_science_chapters()
            selected_chapter = col3.selectbox("Chapter Name", chapter_names)
            chapter_num = ncert_manager.CLASS_10_SCIENCE_CHAPTERS[selected_chapter]
        elif "math" in subject.lower():
            chapter_names = ncert_manager.get_class_10_math_chapters()
            selected_chapter = col3.selectbox("Chapter Name", chapter_names)
            chapter_num = ncert_manager.CLASS_10_MATH_CHAPTERS[selected_chapter]
        else:
            chapter_num = col3.text_input("Chapter Number", placeholder="e.g. 1")
    
    # Class 9
    elif user_class and "9" in user_class:
        if "science" in subject.lower():
            chapter_names = ncert_manager.get_class_9_science_chapters()
            selected_chapter = col3.selectbox("Chapter Name", chapter_names)
            chapter_num = ncert_manager.CLASS_9_SCIENCE_CHAPTERS[selected_chapter]
        elif "math" in subject.lower():
            chapter_names = ncert_manager.get_class_9_math_chapters()
            selected_chapter = col3.selectbox("Chapter Name", chapter_names)
            chapter_num = ncert_manager.CLASS_9_MATH_CHAPTERS[selected_chapter]
        else:
            chapter_num = col3.text_input("Chapter Number", placeholder="e.g. 1")

    # Class 11
    elif user_class and "11" in user_class:
        sub_lower = subject.lower() if subject else ""
        if "physics" in sub_lower:
            chapter_names = ncert_manager.get_class_11_physics_chapters()
            selected_chapter = col3.selectbox("Chapter Name", chapter_names)
            chapter_num = ncert_manager.CLASS_11_PHYSICS_CHAPTERS[selected_chapter]
        elif "chemistry" in sub_lower:
            chapter_names = ncert_manager.get_class_11_chemistry_chapters()
            selected_chapter = col3.selectbox("Chapter Name", chapter_names)
            chapter_num = ncert_manager.CLASS_11_CHEMISTRY_CHAPTERS[selected_chapter]
        elif "biology" in sub_lower:
            chapter_names = ncert_manager.get_class_11_biology_chapters()
            selected_chapter = col3.selectbox("Chapter Name", chapter_names)
            chapter_num = ncert_manager.CLASS_11_BIOLOGY_CHAPTERS[selected_chapter]
        elif "math" in sub_lower:
            chapter_names = ncert_manager.get_class_11_math_chapters()
            selected_chapter = col3.selectbox("Chapter Name", chapter_names)
            chapter_num = ncert_manager.CLASS_11_MATH_CHAPTERS[selected_chapter]
        else:
            chapter_num = col3.text_input("Chapter Number", placeholder="e.g. 1")

    # Class 12
    elif user_class and "12" in user_class:
        sub_lower = subject.lower() if subject else ""
        if "physics" in sub_lower:
            chapter_names = ncert_manager.get_class_12_physics_chapters()
            selected_chapter = col3.selectbox("Chapter Name", chapter_names)
            chapter_num = ncert_manager.CLASS_12_PHYSICS_CHAPTERS[selected_chapter]
        elif "chemistry" in sub_lower:
            chapter_names = ncert_manager.get_class_12_chemistry_chapters()
            selected_chapter = col3.selectbox("Chapter Name", chapter_names)
            chapter_num = ncert_manager.CLASS_12_CHEMISTRY_CHAPTERS[selected_chapter]
        elif "biology" in sub_lower:
            chapter_names = ncert_manager.get_class_12_biology_chapters()
            selected_chapter = col3.selectbox("Chapter Name", chapter_names)
            chapter_num = ncert_manager.CLASS_12_BIOLOGY_CHAPTERS[selected_chapter]
        elif "math" in sub_lower:
            chapter_names = ncert_manager.get_class_12_math_chapters()
            selected_chapter = col3.selectbox("Chapter Name", chapter_names)
            chapter_num = ncert_manager.CLASS_12_MATH_CHAPTERS[selected_chapter]
        else:
            chapter_num = col3.text_input("Chapter Number", placeholder="e.g. 1")

    else:
        chapter_num = col3.text_input("Chapter Number", placeholder="e.g. 10")

    topic = st.text_input("Topic/Question", placeholder="Enter the specific concept...")
    
    # Cognitive Depth Control
    depth = st.select_slider("Cognitive Depth", options=["Default (Short)", "Assessment (Exp + Quiz + Questions)", "Long (Detailed)"])

    if st.button("Generate Learning Path"):
        if not topic:
            st.error("Please enter a topic.")
        else:
            with st.spinner("Analyzing Knowledge Graph & Scaling Math..."):
                # Define constraints based on depth
                word_limit = "120 words" if depth == "Default (Short)" else "450 words"
                include_extras = "YES" if depth == "Assessment (Exp + Quiz + Questions)" else "NO"
                
                # MASTER PROMPT: Strictly forcing Math formatting and Easy Analogies
                master_prompt = f"""
                Act as an expert tutor for {user_class}. Topic: {topic} ({subject} - Chapter {chapter_num}).
                
                STRICT RULES:
                1. ANALOGY: Use a very simple, everyday relatable example (like a car, kitchen items, or sports).
                2. MATH FORMAT: You must provide a solved example. Use this structure exactly:
                   **The Problem:** [Scenario]
                   **The Formula:** [LaTeX Formula]
                   **Step-by-Step Solution:** [Numbered LaTeX steps]
                   **Final Result:** [LaTeX answer]
                
                STRICT TAGS FOR PARSING:
                [FOUNDATION]: List 2 prerequisites and a 3-step study order.
                [EXPLANATION]: Provide the easy analogy and simple concept explanation (under {word_limit}).
                [VISUAL]: Describe a diagram or mental image.
                [MATH]: Provide the mathematical breakdown in the strict format mentioned above.
                [MISCONCEPTIONS]: List 2 common mistakes and their corrections.

                [QUIZ]: 
                CRITICAL: If {include_extras} == "NO", leave this section COMPLETELY EMPTY. Do not write any questions.
                If {include_extras} == "YES", provide 3 MCQs. Format: Q: [Quest] | A: [Opt] | B: [Opt] | C: [Opt] | D: [Opt] | Correct: [Ans]. Separate with '---'.

                [PRACTICE]: 
                CRITICAL: If {include_extras} == "NO", leave this section COMPLETELY EMPTY. Do not write any questions.
                If {include_extras} == "YES", provide 3 open-ended conceptual/numerical questions. Format: PQ: [Question] | Ans: [Answer]. Separate with '###'.
                """
                
                # FIX: Initialize variable to avoid NameError
                full_response = ask_gemini(master_prompt)

                # 2. PARSING & DISPLAY LOGIC
                try:
                    def get_section(content, start, end):
                        if start in content and end in content:
                            return content.split(start)[1].split(end)[0].strip()
                        return ""

                    foundations = get_section(full_response, "[FOUNDATION]", "[EXPLANATION]")
                    explanation = get_section(full_response, "[EXPLANATION]", "[VISUAL]")
                    visual_desc = get_section(full_response, "[VISUAL]", "[MATH]")
                    math_way = get_section(full_response, "[MATH]", "[MISCONCEPTIONS]")
                    
                    if "[QUIZ]" in full_response and include_extras == "YES":
                        misconceptions = get_section(full_response, "[MISCONCEPTIONS]", "[QUIZ]")
                        quiz_raw = get_section(full_response, "[QUIZ]", "[PRACTICE]")
                        practice_raw = full_response.split("[PRACTICE]")[1].strip()
                    else:
                        # 1. Grab everything after the Misconceptions tag
                        raw_misc = full_response.split("[MISCONCEPTIONS]")[1].strip()
                        
                        # 2. IMPROVED CLEANING: Explicitly remove "NO" and any leftover tags
                        # This stops the "NO" from appearing in Short/Long mode
                        misconceptions = raw_misc.split("[QUIZ]")[0].split("[PRACTICE]")[0].strip()
                        
                        # Final check to remove a standalone "NO" if it's the last word
                        if misconceptions.endswith("NO"):
                            misconceptions = misconceptions[:-2].strip()
                        
                        # 3. Keep assessment variables empty so they don't display
                        quiz_raw, practice_raw = "", ""
                    # --- UI DISPLAY ---
                    st.markdown('### 🏛️ 1. Foundations')
                    st.info(foundations)

                    st.markdown('### 📖 2. The Concept')
                    st.markdown(explanation)

                    col_v, col_m = st.columns(2)
                    with col_v:
                        with st.container(border=True):
                            st.subheader("🖼️ The Visual Way")
                            
                            # --- NCERT INTEGRATION ATTEMPT ---
                            # --- NCERT INTEGRATION ATTEMPT ---
                            ncert_image = None
                            # Skip for Math as requested
                            if "math" not in subject.lower():
                                try:
                                    with st.spinner("Searching NCERT Database..."):
                                        pdf_path, msg = ncert_manager.download_ncert_pdf(user_class, subject, chapter_num)
                                        if pdf_path:
                                            st.caption(f"✅ NCERT Source Found: {os.path.basename(pdf_path)}")
                                            ncert_image = ncert_manager.extract_relevant_image(pdf_path, topic)
                                        else:
                                            st.caption(f"⚠️ NCERT Search: {msg}")
                                except Exception as e:
                                    st.caption(f"NCERT Error: {e}")
                            else:
                                st.caption("Mathematical Subject: Using AI Visualization & Mental Models.")

                            # DISPLAY LOGIC
                            if ncert_image:
                                st.image(ncert_image, caption=f"NCERT Diagram: {topic} (Official)", width='stretch')
                                st.success("Official NCERT Diagram extracted successfully.")
                            else:
                                # FALLBACK TO AI GENERATION
                                st.caption("Using AI Visualization (NCERT diagram not found or extracted).")
                                img_topic = topic.replace(" ", "_")
                                diagram_url = f"https://pollinations.ai/p/educational_scientific_diagram_of_{img_topic}_{subject}_labeled_clear_background?width=800&height=600&seed=42"
                                st.image(diagram_url, caption=f"AI Visualization: {topic}", width='stretch')
                                
                                with st.expander("🔍 Click to Zoom / View Full Diagram"):
                                    st.image(diagram_url, width='stretch')
                            
                            st.write(visual_desc)
                            
                            # --- NEW: MENTAL MODEL VISUALIZATION ---
                            # Only runs if it's likely a chemical/math topic to save token/time
                            if "chem" in subject.lower() or "science" in subject.lower() or "math" in subject.lower():
                                try:
                                    mental_prompt = f"""
                                    Create a "Mental Model" visualization for '{topic}'.
                                    If it's a chemical, show the 2D structural formula (like Ethanol or Benzene) using simple ASCII/text art.
                                    If it's a math/physics concept, show the core equation or a simple text diagram.
                                    
                                    Style: Clean, spacious, easy to read on a dark background. 
                                    Format: Return ONLY the ASCII/Equation inside a code block. NO explanation.
                                    """
                                    mental_art = ask_gemini(mental_prompt)
                                    if "```" in mental_art: # Simple check if it returned code
                                        st.markdown("### 🧠 Mental Structure")
                                        st.caption("Visualize this structure/equation in your mind:")
                                        st.markdown(mental_art)
                                except Exception:
                                    pass

                    with col_m:
                        with st.container(border=True):
                            st.subheader("🔢 The Mathematical Way")
                            st.markdown(math_way)
                    
                    with st.expander("🔍 3. Common Pitfalls & Corrections"):
                        st.warning(misconceptions)

                    # Assessment Section (Only displays if assessment mode is active)
                    if include_extras == "YES" and (quiz_raw or practice_raw):
                        st.markdown('### ✍️ 4. Assessment Zone')
                        tab_mcq, tab_practice = st.tabs(["Multiple Choice Quiz", "3 Practice Questions"])
                        
                        with tab_mcq:
                            if quiz_raw:
                                for i, q_item in enumerate(quiz_raw.split('---')):
                                    if "|" in q_item:
                                        m = q_item.split("|")
                                        st.write(f"**Q{i+1}: {m[0].replace('Q:', '').strip()}**")
                                        c1, c2 = st.columns(2)
                                        c1.write(f"**A)** {m[1].replace('A:', '').strip()}")
                                        c2.write(f"**B)** {m[2].replace('B:', '').strip()}")
                                        c1.write(f"**C)** {m[3].replace('C:', '').strip()}")
                                        c2.write(f"**D)** {m[4].replace('D:', '').strip()}")
                                        with st.expander("Reveal Answer"):
                                            st.success(f"Correct: {m[5].replace('Correct:', '').strip()}")
                                        st.markdown("---")
                        
                        with tab_practice:
                            if practice_raw:
                                for i, p_item in enumerate(practice_raw.split('###')[:3]):
                                    if "|" in p_item:
                                        p_parts = p_item.split("|")
                                        st.write(f"**Question {i+1}:** {p_parts[0].replace('PQ:', '').strip()}")
                                        with st.expander("Check Solution"):
                                            st.success(p_parts[1].replace('Ans:', '').strip())

                except Exception as e:
                    st.error(f"Structure error: {e}")
                    st.markdown(full_response)

# --- MODE 2: EXAM-AWARE (CBSE OPTIMIZED) ---
elif mode == "📝 Exam Generator":
    st.markdown('<div class="main-title">Exam Answer Engine</div>', unsafe_allow_html=True)
    
    # --- 1. SESSION STATE INITIALIZATION ---
    if 'exam_question_text' not in st.session_state:
        st.session_state.exam_question_text = ""

    # --- 2. VOICE INPUT LOGIC ---
    st.markdown("### 🎙️ Ask by Voice")
    # Capture audio
    spoken_text = speech_to_text(
        start_prompt="Start recording", 
        stop_prompt="Stop recording", 
        language='en', 
        use_container_width=True, 
        just_once=True, 
        key='exam_mic'
    )
    
    # Update session state if new voice input is received
    if spoken_text:
        st.session_state.exam_question_text = spoken_text

    # --- 3. THE INPUT BOX ---
    # The value is tied to session_state so it survives the button click
    q_exam = st.text_input(
        "Enter Exam Question", 
        value=st.session_state.exam_question_text,
        placeholder="Type here or use the microphone above..."
    )
    
    # Manual update: If user types manually, sync it to session state
    st.session_state.exam_question_text = q_exam
    
    # Updated Marks options to include 2 Marks
    marks = st.select_slider("Target Marks (CBSE Style)", options=["2 Marks", "3 Marks", "5 Marks", "7 Marks"])
    
    if st.button("Generate CBSE Answer"):
        if not q_exam:
            st.warning("Please enter a question first.")
        else:
            with st.spinner("Drafting textbook-accurate answer..."):
                # REFINED PROMPT WITH STRICT WORD LIMITS, KEYWORDS, AND FORMULAS
                exam_prompt = f"""
                Act as a strict CBSE Board Examiner. Write a high-scoring, school-level answer for: '{q_exam}'.
                Target Marks: {marks}.
                
                STRICT CONTENT RULES:
                1. TEXTBOOK ONLY: Use only standard school level textbook knowledge. NO external "extra" information.
                2. KEYWORDS: You MUST **bold** every critical technical keyword essential for scoring marks.
                3. FORMULAS: Include standard formulas using LaTeX where applicable.
                4. LANGUAGE: Use formal, proper school-level English suitable for board exams.
                
                STRICT STRUCTURE & WORD LIMITS:
                - If 2 Marks: 50–80 words. Provide one clear definition + one factual statement + two distinct points.
                - If 3 Marks: 100–150 words. Present three distinct points or logical steps. Do NOT use an unnecessary introduction.
                - If 5 Marks: 150–200 words. Start with a brief introduction followed by 4 to 5 key explanatory bullet points.
                - If 7 Marks: 200–300 words. Include a short introduction, a detailed structured explanation or derivation, and a diagram description or formula.
                
                OUTPUT FORMAT:
                1. The Answer (with bold keywords).
                2. A section at the end called [MARKING SCHEME] showing how the {marks} are awarded.
                3. A final section called [EXAM TIP] for a topper-style presentation.
                """
                
                full_response = ask_gemini(exam_prompt)
                
                # Parsing logic to separate marking scheme and tips for better UI
                main_ans = full_response.split("[MARKING SCHEME]")[0].strip()
                
                scheme_tip = ""
                if "[MARKING SCHEME]" in full_response:
                    scheme_tip = full_response.split("[MARKING SCHEME]")[1].strip()

                # Display Section
                st.success(f"Generated {marks} CBSE Response (Textbook Standard):")
                
                # Answer Box
                with st.container(border=True):
                    st.markdown(main_ans)
                
                # Extra Exam Insights
                if scheme_tip:
                    with st.expander("📊 Examiner Insights: Marking Scheme & Tips"):
                        st.info(scheme_tip.replace("[EXAM TIP]", "\n\n**💡 EXAM TIP:**"))
                
                # Download Button
                st.download_button(
                    label="📂 Download CBSE Answer assessment",
                    data=full_response,
                    file_name=f"CBSE_{marks.replace(' ', '_')}_Solution.txt",
                    mime="text/plain"
                )

# =========================================================
# MODE 3: THINKING DEBUGGER (Diagnostic Version)
# =========================================================
elif mode == "🔍 Thinking Debugger":
    st.markdown('<div class="main-title">🧠 Thinking Debugger</div>', unsafe_allow_html=True)
    st.info("Input your understanding of a topic. LUMINA will analyze it for errors.")

    # --- 1. SESSION STATE INITIALIZATION ---
    # This prevents the text from disappearing when the 'Analyze' button is clicked
    if 'debug_text' not in st.session_state:
        st.session_state.debug_text = ""

    # --- 2. VOICE INPUT LOGIC ---
    st.markdown("### 🎙️ Explain by Voice")
    spoken_debug = speech_to_text(
        start_prompt="Click to Start Speaking", 
        stop_prompt="Stop Recording", 
        language='en', 
        use_container_width=True, 
        just_once=True, 
        key='debugger_mic'
    )
    
    # Update the state if new speech is captured
    if spoken_debug:
        st.session_state.debug_text = spoken_debug

    # --- 3. THE TEXT AREA ---
    # The value is tied to session_state
    user_thought = st.text_area(
        "Your Reasoning:", 
        value=st.session_state.debug_text,
        placeholder="Example: 'I think heavy objects fall faster than light objects because gravity pulls them harder.'",
        height=150
    )
    
    # Sync manual typing back to session state
    st.session_state.debug_text = user_thought
    
    if st.button("Analyze & Debug"):
        if not user_thought:
            st.warning("Please enter your statement first!")
        else:
            with st.spinner("Analyzing logical consistency..."):
                debug_prompt = f"""
                User's Statement: "{user_thought}"
                
                Task: Perform a deep logical analysis.
                
                Format the output exactly like this:
                1. **STATUS:** [Declare 'TRUE' or 'FALSE' or 'PARTIALLY CORRECT']
                2. **THE FLAW:** Identify the specific part of the user's sentence that is scientifically or logically wrong.
                3. **THE REASON:** Explain why that specific part is wrong (the 'Logic Gap').
                4. **THE CORRECT CONCEPT:** Provide the scientifically accurate explanation.
                5. **VERDICT:** A 1-sentence wrap-up of what the user needs to change in their mental model.
                
                Tone: Professional, direct, and clinical.
                """
                
                response = ask_gemini(debug_prompt)
                
                # UI Display
                if "FALSE" in response.upper() or "PARTIALLY" in response.upper():
                    st.error("Diagnostic Result:")
                else:
                    st.success("Diagnostic Result:")
                    
                st.markdown(response)
# --- MODE 4: FLASHCARDS  ---
elif mode == "🗂️ Flashcards":
    st.markdown('<div class="main-title">Revision Tools</div>', unsafe_allow_html=True)
    rev_topic = st.text_input("Enter Topic")
    
    col1, col2 = st.columns(2)
    if col1.button("Generate Flashcards"):
        if not rev_topic:
            st.warning("Enter a topic first!")
        else:
            with st.spinner("Creating Interactive Flashcards..."):
                # We force the AI to use a split character '|' between Q and A
                fc_prompt = f"""Create 5 flashcards for {rev_topic}. 
                Follow this format EXACTLY for each card:
                Q: [Question] | A: [Answer]
                Separate each card with '---'. 
                Do not include any introductory or concluding text."""
                
                raw_response = ask_gemini(fc_prompt)
                cards = raw_response.split('---')
                
                st.markdown("### 🗂️ Tap to Reveal Answers")
                
                for i, card in enumerate(cards):
                    if "|" in card:
                        # Split the single card into Question and Answer
                        parts = card.split("|")
                        question = parts[0].replace("Q:", "").strip()
                        answer = parts[1].replace("A:", "").strip()
                        
                        # Use an expander to hide the answer
                        with st.expander(f"🎴 Card {i+1}: {question}"):
                            st.success(f"**Answer:** {answer}")
 
# --- MODE 5: CONCEPT TRANSFER INTELLIGENCE (CTI) - VIVA/INTERVIEW EDITION ---
elif mode == "🧠 Concept Transfer Intelligence (CTI)":
    st.markdown('<div class="main-title">Concept Transfer Intelligence</div>', unsafe_allow_html=True)
    
    # Initialize Session State
    if "cti_active" not in st.session_state:
        st.session_state.cti_active = False
        st.session_state.cti_finished = False
        st.session_state.cti_turn = 0
        st.session_state.cti_history = [] 
        st.session_state.cti_dna = ""      
        st.session_state.cti_evals = []    

    # 1. START SCREEN (The Waiting Room)
    if not st.session_state.cti_active:
        st.info("🎓 **The Examination Room:** You are entering a viva/interview. The examiner will test your logic, not your memory. Answer clearly and defend your reasoning.")
        
        topic_input = st.text_input("Candidate, what topic are we discussing today?", placeholder="e.g., Thermodynamics, Market Equilibrium, Data Structures...")
        
        if st.button("Enter Viva Room"):
            if topic_input:
                st.session_state.cti_active = True
                with st.spinner("Examiner is reviewing the concept..."):
                    # LAYER 1: INTERNAL DNA (Hidden)
                    dna_p = f"Analyze '{topic_input}'. Core Principle, Hidden Assumptions, Comfort Zone. Focus on technical accuracy."
                    st.session_state.cti_dna = ask_gemini(dna_p)
                    
                    # LAYER 2: THE OPENING QUESTION (Updated for Student Level)
                    start_p = f"""
                    Topic: {topic_input}
                    DNA: {st.session_state.cti_dna}
                    Persona: Act as a Senior School Teacher or a Technical Interviewer for College Freshmen.
                    Tone: Formal, inquisitive, and firm.
                    
                    Task: Set up a practical, real-world scenario where {topic_input} applies.
                    DIFFICULTY RULE: Match the level of a Class 9 to College 1st Year student.
                    SCENARIO RULE: Use relatable examples (e.g., sports, household objects, simple gadgets). 
                    NO textbook examples. DO NOT explain the answer. 
                    Stop after the question.
                    """
                    first_q = ask_gemini(start_p)
                    st.session_state.cti_history.append({"role": "assistant", "content": first_q})
                    st.session_state.cti_turn = 1
                    st.rerun()

    # 2. THE INTERROGATION (The Viva Loop)
    elif not st.session_state.cti_finished:
        st.progress(min(st.session_state.cti_turn / 12, 1.0), text=f"Interview Progress: Level {st.session_state.cti_turn}")

        for msg in st.session_state.cti_history:
            role_icon = "👨‍🏫" if msg["role"] == "assistant" else "🎓"
            with st.chat_message(msg["role"], avatar=role_icon):
                st.write(msg["content"])

        # --- VOICE INPUT FOR VIVA ---
        st.write("---")
        st.markdown("### 🎙️ Record Your Answer")
        # capturing the speech
        spoken_reply = speech_to_text(language='en', use_container_width=True, just_once=True, key=f'viva_mic_{st.session_state.cti_turn}')

        user_reply = st.chat_input("State your reasoning, candidate...")
        
        # If the user spoke, we treat the spoken text as the reply
        final_reply = user_reply if user_reply else spoken_reply

        if final_reply:
            st.session_state.cti_history.append({"role": "user", "content": final_reply})
            
            with st.spinner("Examiner is evaluating your logic..."):
                # LAYER 3 & 4 (Updated for Student Level)
                loop_p = f"""
                DNA: {st.session_state.cti_dna}
                History: {st.session_state.cti_history}
                Persona: Senior School/College Interviewer. 
                
                TASK 1 (Hidden Debug): Analyze the candidate's answer. Are they using jargon to hide a lack of understanding? Is their logic sound?
                TASK 2 (Follow-up): 
                - Difficulty must remain at Class 9 - College 1st Year level. 
                - Use simple, direct vocabulary.
                - If they are correct, challenge an assumption or move to a harder RELATABLE edge-case.
                - If they are wrong, ask a 'cross-question' that forces them to see their own mistake.
                - If turn >= 7 or they've proven mastery, respond with [TERMINATE].
                
                FORMAT:
                EVAL: [Hidden Thinking Debugger Analysis]
                NEXT: [Interviewer's next question or [TERMINATE]]
                """
                res = ask_gemini(loop_p)
                
                if "NEXT:" in res:
                    parts = res.split("NEXT:")
                    st.session_state.cti_evals.append(parts[0].replace("EVAL:", "").strip())
                    next_step = parts[1].strip()
                else:
                    next_step = res

                if "[TERMINATE]" in next_step:
                    st.session_state.cti_finished = True
                    st.rerun()
                else:
                    st.session_state.cti_turn += 1
                    st.session_state.cti_history.append({"role": "assistant", "content": next_step})
                    st.rerun()

    # 3. FINAL EVALUATION (The Feedback Session)
    else:
        st.subheader("🏛️ Interview Concluded")
        st.write("The examiner has finished the questioning. Review your performance below.")
        
        if st.button("📂 Review Examiner's Feedback"):
            st.markdown("### 🔍 Internal Logic Evaluation")
            user_msgs = [m for m in st.session_state.cti_history if m["role"] == "user"]
            for i, msg in enumerate(user_msgs):
                if i < len(st.session_state.cti_evals): # Safety check
                    with st.expander(f"Question {i+1} - Candidate Response Analysis"):
                        st.write(f"**Your Argument:** {msg['content']}")
                        st.info(f"**Examiner's Internal Note:** {st.session_state.cti_evals[i]}")
            
            st.markdown("### 📊 Final Concept Competency Map")
            final_p = f"""
            Based on these evaluations: {st.session_state.cti_evals}, provide:
            1. Strong Concepts (Logic was robust)
            2. Fragile Logic (Where they struggled or guessed)
            3. Weak  (Verdict on deep understanding vs rote learning for their grade level)
            """
            st.success(ask_gemini(final_p))

        if st.button("Reset for New Interview"):
            st.session_state.clear()


# =========================================================
# MODE 6: ARITHMETIC SOLVING (NCERT Class 8-12)
# =========================================================
elif mode == "🔢 Arithmetic Solving":
    st.markdown('<div class="main-title">🔢 Arithmetic Solving</div>', unsafe_allow_html=True)
    st.info("Strictly for Mathematical Operations. Follows NCERT step-by-step logic.")

    # 1. SESSION STATE FOR PERSISTENCE
    if 'arithmetic_q' not in st.session_state:
        st.session_state.arithmetic_q = ""

    # 2. ALIGNED INPUT SECTION (Same Line Layout)
    # Using columns to align 'Select Class' and 'Ask by Voice'
    col1, col2 = st.columns([2, 4], gap="large")
    
    with col1:
        st.markdown("**Select Class**")
        grade_level = st.selectbox(
            "Select Class", 
            ["Class 9", "Class 10", "Class 11", "Class 12"],
            label_visibility="collapsed",
            key="math_grade_select"
        )
    
    with col2:
        # Aligning the header with the dropdown's top margin
        st.markdown("### 🎙️ Ask by Voice")
        spoken_math = speech_to_text(
            language='en', 
            use_container_width=True, 
            just_once=True, 
            key=f'arith_mic_{grade_level}' 
        )
        if spoken_math:
            st.session_state.arithmetic_q = spoken_math

    # 3. TEXT AREA SECTION
    st.markdown("**Enter Math Problem:**")
    user_problem = st.text_area(
        "Enter Math Problem:", 
        value=st.session_state.arithmetic_q,
        placeholder="e.g., Integrate log x to the power 5 or solve a profit/loss problem...",
        height=150,
        label_visibility="collapsed"
    )
    st.session_state.arithmetic_q = user_problem

    # 4. SOLVER ENGINE
    if st.button("SOLVE THE MATHEMATICAL WAY", use_container_width=True):
        if not user_problem:
            st.warning("Please enter a mathematical operation to solve.")
        else:
            with st.spinner(f"Solving using {grade_level} NCERT methodology..."):
                math_prompt = f"""
                User Grade: {grade_level}
                Problem: {user_problem}

                STRICT RULES:
                1. Solve ONLY if this is a Mathematical/Arithmetic operation.
                2. Use the exact NCERT {grade_level} textbook approach.
                3. Follow the systematic 'Mathematical Way' format.

                FORMAT OF OUTPUT:
                # 🔢 The Mathematical Way
                
                **The Problem:** [Restate problem clearly]
                
                **The Formula:** [State the specific NCERT formula in LaTeX]
                
                **Step-by-Step Solution:**
                1. **Identify the given values:** [List variables with units]
                2. **Rearrange/Substitute:** [Show the formula with numbers]
                3. **Calculate:** [Show clear arithmetic steps]
                4. **Simplification:** [Final reduction]
                
                **Final Result:** > $$[Final Answer Boxed]$$

                **Teacher's Tip:** [Specific exam hack for this topic]
                
                ---
                ## 🔄 Reoccurring Exam Questions
                - **Easy (NCERT):** [1 basic question]
                - **Medium (Board Level):** [1 reoccurring question]
                - **Hard (HOTS):** [1 challenging logic question]
                """
                
                solution = ask_gemini(math_prompt)
                
                st.markdown("---")
                st.markdown(solution)
                
                # Visual Support for Concepts
                if "refraction" in user_problem.lower() or "sin" in user_problem.lower():
                    st.write("")

                st.download_button("Download Solution", solution, file_name=f"{grade_level}_Solution.txt")
