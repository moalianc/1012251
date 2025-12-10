import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- Page Configuration ---
st.set_page_config(page_title="1112251", layout="wide", page_icon="⚡")

# --- CSS for Professional Look ---
st.markdown("""
<style>
    .stTextArea textarea { font-family: 'Consolas', monospace; }
    div[data-testid="stToolbar"] { visibility: hidden; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.title("1012251")
st.write("Class Diagram & Questions.")

# --- Sidebar: API & Status ---
with st.sidebar:
    st.header("Settings")
    # لجلب المفتاح من الأسرار لضمان الأمان
    if "GOOGLE_API_KEY" in st.secrets:
        st.success("Activated")
        api_key = st.secrets["GOOGLE_API_KEY"]
    else:
        st.error("Key Not Found")
        st.info("Add Key.")
        api_key = None

# --- Main Layout ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Diagram")
    uploaded_file = st.file_uploader("Add", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, caption="Diagram Context", use_column_width=True)

with col2:
    st.subheader("Text")
    questions = st.text_area("Text here...", height=400, placeholder="...")

# --- Execution Logic ---
if st.button("Start", type="primary", use_container_width=True):
    if not api_key:
        st.error("Key first.")
    elif not uploaded_file or not questions:
        st.warning("Info Required.")
    else:
        try:
            # 1. Configure API
            genai.configure(api_key=api_key)
            
            # 2. Initialize Model (CORRECTED to Gemini 3)
            # استخدام أحدث موديل متوفر بقدرات التفكير المنطقي
            model = genai.GenerativeModel('gemini-3-pro-preview')
            
            image = Image.open(uploaded_file)
            
            with st.spinner('...'):
                
                # --- Advanced Prompt for Perfect M251 Solution ---
                prompt = f"""
                You are an Expert Java Instructor.
                
                OBJECTIVE:
                Generate a COMPLETE, ERROR-FREE solution for the M251 Object Oriented Programming exam based on the provided Class Diagram and Questions.
                
                STRICT CONSTRAINTS (Clean Code Standards):
                1. **Language:** English ONLY.
                2. **No Chatting:** Do not write introductions like "Here is the code". Start immediately with the solution.
                3. **OOP Best Practices:**
                   - All attributes must be `private`.
                   - All methods must be `public` (unless specified otherwise).
                   - Use `@Override` for `toString`, `equals`, and `compareTo`.
                   - Add Javadoc comments (`/** ... */`) for every class and method.
                4. **Error Handling:** Use `try-catch` blocks for File I/O operations (Scanner/File).
                5. **Format:** Output the solution in clearly separated blocks ready for copy-pasting.
                
                REQUIRED OUTPUT SECTIONS:
                
                ### SECTION 1: PROJECT STRUCTURE
                **Project Name:** [Extract from question, e.g., Name_ID]
                **Files to Create:** [List all .java and .txt files]
                
                ### SECTION 2: JAVA CLASSES
                (Write the code for the Abstract class/Interface first, then Child classes, then the Laundry/Manager class)
                
                ### SECTION 3: TEST CLASS
                (The main class with public static void main)
                
                ### SECTION 4: DATA FILE CONTENT
                (The exact content of the .txt file)
                
                ### SECTION 5: EXPECTED CONSOLE OUTPUT
                (Simulate the run and show exact output)
                
                INPUT DATA:
                {questions}
                """
                
                # 3. Generate Content
                response = model.generate_content([prompt, image])
                
                # 4. Display Result
                st.markdown("### Answer")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Error: {e}")
            st.warning("Note: Make sure Key has access.")