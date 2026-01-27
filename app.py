
import streamlit as st
import pandas as pd
import random
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import streamlit.components.v1 as components

# --- Helper Functions (copied/adapted from individual scripts) ---

def load_data():
    try:
        df = pd.read_csv("df_iso15924_scripts.tsv", sep="\t")
        return df
    except FileNotFoundError:
        st.error("Data file 'df_iso15924_scripts.tsv' not found.")
        return None

def get_transliteration_map():
    # Same map as transliterate.py
    vowels = {
        'aa': 'ಆ', 'a': 'ಅ', 'ii': 'ಈ', 'i': 'ಇ', 'uu': 'ಊ', 'u': 'ಉ',
        'e': 'ಎ', 'ee': 'ಏ', 'ai': 'ಐ', 'o': 'ಒ', 'oo': 'ಓ', 'au': 'ಔ',
        'am': 'ಅಂ', 'ah': 'ಅಃ'
    }
    consonants = {
        'k': 'ಕ್', 'kh': 'ಖ್', 'g': 'ಗ್', 'gh': 'ಘ್', 'ng': 'ಙ್',
        'ch': 'ಚ್', 'chh': 'ಛ್', 'j': 'ಜ್', 'jh': 'ಝ್', 'ny': 'ಞ್',
        't': 'ಟ್', 'th': 'ಠ್', 'd': 'ಡ್', 'dh': 'ಢ್', 'n': 'ಣ್',
        'th': 'ತ್', 'd': 'ದ್', 'dh': 'ಧ್', 'n': 'ನ್', 
        'p': 'ಪ್', 'ph': 'ಫ್', 'b': 'ಬ್', 'bh': 'ಭ್', 'm': 'ಮ್',
        'y': 'ಯ್', 'r': 'ರ್', 'l': 'ಲ್', 'v': 'ವ್', 'w': 'ವ್',
        'sh': 'ಶ್', 'shh': 'ಷ್', 's': 'ಸ್', 'h': 'ಹ್', 'l': 'ಳ್'
    }
    matras = {
        'a': '', 'aa': 'ಾ', 'i': 'ಿ', 'ii': 'ೀ', 'u': 'ು', 'uu': 'ೂ', 'ru': 'ೃ',
        'e': 'ೆ', 'ee': 'ೇ', 'ai': 'ೈ', 'o': 'ೊ', 'oo': 'ೋ', 'au': 'ೌ',
    }
    return vowels, consonants, matras

def transliterate(text):
    if not text: return ""
    vowels, consonants, matras = get_transliteration_map()
    result = ""
    i = 0
    n = len(text)
    
    while i < n:
        match_c = None
        len_c = 0
        for width in [3, 2, 1]:
            chunk = text[i:i+width].lower()
            if chunk in consonants:
                match_c = chunk
                len_c = width
                break
        
        if match_c:
            base_char = consonants[match_c][0]
            i += len_c
            match_v = None
            len_v = 0
            for width in [2, 1]:
                if i + width <= n:
                    v_chunk = text[i:i+width].lower()
                    if v_chunk in matras:
                        match_v = v_chunk
                        len_v = width
                        break
            if match_v:
                result += base_char + matras[match_v]
                i += len_v
            else:
                result += consonants[match_c]
        else:
            match_ind_v = None
            len_ind_v = 0
            for width in [2, 1]:
                chunk = text[i:i+width].lower()
                if chunk in vowels:
                    match_ind_v = chunk
                    len_ind_v = width
                    break
            if match_ind_v:
                result += vowels[match_ind_v]
                i += len_ind_v
            else:
                result += text[i]
                i += 1
    return result

def get_kannada_char():
    return chr(random.randint(0x0C85, 0x0CB9))

# --- Page Layout ---

st.set_page_config(page_title="Kannada Script Dasboard", layout="wide", page_icon="🏹")

# --- Custom CSS for Premium UI ---
st.markdown("""
<style>
    /* Gradient Background Line at top */
    .stApp > header {
        background: transparent;
    }
    .main .block-container {
        padding-top: 2rem;
    }
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 4px;
        padding: 10px 20px;
        background-color: #0e1117;
        border: 1px solid #333;
    }
    .stTabs [data-baseweb="tab"]:hover {
        border-color: #FFC400; /* Karnataka Yellow Highlight */
        color: #FFC400;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF0000 !important; /* Karnataka Red */
        color: white !important;
        border: none;
    }
    /* Button Styling */
    .stButton > button {
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(255, 0, 0, 0.2);
    }
    /* Global Font adjustments */
    h1, h2, h3 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Info
with st.sidebar:
    st.title("🏹 Script Explorer")
    st.info("**Kannada** is one of the oldest Dravidian languages with a rich literary history.")
    st.write("---")
    st.write("Developed with ❤️ using Python & Streamlit.")

st.title("🏹 Kannada & Indic Script Explorer")
st.markdown("#### Explore the **history**, **art**, and **utility** of the Kannada script.")

tabs = st.tabs(["📊 Data", "🔡 Transliterate", "🎮 Quiz", "🎨 Creative", "🤖 AI Lab"])

# --- Tab 1: Analysis ---
with tabs[0]:
    st.header("Script Standardization Timeline")
    st.write("") # Spacer to prevent overlap
    df = load_data()
    
    if df is not None:
        indic_scripts = [
            'Brah', 'Deva', 'Knda', 'Taml', 'Telu', 'Mlym', 'Beng', 'Gujr', 
            'Guru', 'Orya', 'Sinh', 'Tibt', 'Khmr', 'Java', 'Bali', 'Newa', 
            'Gran', 'Sidd'
        ]
        
        # Filter and process
        df_indic = df[df['Code'].isin(indic_scripts)].copy()
        df_indic['Date'] = pd.to_datetime(df_indic['Date'])
        df_indic = df_indic.sort_values('Date')
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.dataframe(df_indic[['Code', 'English Name', 'Date']])
            
        with col2:
            # Create color and size arrays for highlighting Kannada
            colors = ['red' if name == 'Kannada' else 'teal' for name in df_indic['English Name']]
            sizes = [250 if name == 'Kannada' else 100 for name in df_indic['English Name']]
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(df_indic['Date'], df_indic['English Name'], color=colors, s=sizes, zorder=3)
            ax.hlines(y=df_indic['English Name'], xmin=df_indic['Date'].min(), xmax=df_indic['Date'], color='skyblue', alpha=0.5, zorder=2)
            
            # Annontate Kannada
            kannada_row = df_indic[df_indic['English Name'] == 'Kannada'].iloc[0]
            ax.annotate('Kannada', (kannada_row['Date'], kannada_row['English Name']), 
                        xytext=(10, 5), textcoords='offset points', color='red', weight='bold')

            ax.set_title('ISO Registration Timeline (Kannada Highlighted)')
            ax.set_xlabel('Date')
            ax.grid(axis='x', linestyle='--', alpha=0.7)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
            fig.autofmt_xdate()
            st.pyplot(fig)

# --- Tab 2: Transliteration ---
with tabs[1]:
    st.header("English -> Kannada Transliteration")
    st.markdown("Type phonetically (e.g., *'kannada'* or *'namaskara'*)")
    
    input_text = st.text_input("Enter text:", "namaskara")
    
    if input_text:
        out = transliterate(input_text)
        st.markdown(f"### Output: `{out}`")
        st.markdown(f"# {out}") # Large display

# --- Tab 3: Quiz ---
with tabs[2]:
    st.header("Script Identification Quiz")
    
    # Quiz Logic with Limits
    # Settings moved to Sidebar to clean up UI
    
    if 'quiz_active' not in st.session_state:
        st.session_state.quiz_active = False

    if not st.session_state.quiz_active:
        st.markdown("### 🧠 Test your knowledge!")
        st.markdown("Configure your quiz in the **sidebar** and click start!")
        
        # Sidebar Control for Quiz
        with st.sidebar:
            st.divider()
            st.header("🎮 Quiz Settings")
            num_q = st.slider("Number of Questions", min_value=3, max_value=20, value=5)
            
        if st.button("🚀 Start Quiz", type="primary"):
            st.session_state.quiz_active = True
            st.session_state.limit = num_q
            st.session_state.score = 0
            st.session_state.total = 0
            st.session_state.current_row = None
            st.session_state.quiz_complete = False
            st.rerun()
            
    elif st.session_state.get('quiz_complete', False):
         st.balloons()
         st.success(f"Quiz Completed! Score: {st.session_state.score} / {st.session_state.total}")
         if st.button("Play Again"):
             st.session_state.quiz_active = False
             st.session_state.quiz_complete = False
             st.rerun()
             
    else:
        # helper to get new question
        def next_question():
            if st.session_state.total >= st.session_state.limit:
                st.session_state.quiz_complete = True
                return

            if df is not None:
                # Hard mode (Indics) by default for fun
                indic_codes = [
                    'Brah', 'Deva', 'Knda', 'Taml', 'Telu', 'Mlym', 'Beng', 'Gujr', 
                    'Guru', 'Orya', 'Sinh', 'Tibt', 'Khmr', 'Java', 'Bali', 'Newa', 
                    'Gran', 'Sidd'
                ]
                st.session_state.current_row = df[df['Code'].isin(indic_codes)].sample(1).iloc[0]
                
        if st.session_state.current_row is None:
            next_question()

        if not st.session_state.quiz_complete:
            row = st.session_state.current_row
            
            # Progress bar
            progress = st.session_state.total / st.session_state.limit
            st.progress(progress, text=f"Question {st.session_state.total + 1} of {st.session_state.limit}")
            
            st.markdown(f"### Which script code is: **{row['English Name']}**?")
            
            # 3 options (1 correct, 2 random)
            if 'options' not in st.session_state or st.session_state.options_code != row['Code']:
                opts = [row['Code']]
                while len(opts) < 3:
                    r = df['Code'].sample(1).iloc[0]
                    if r not in opts: opts.append(r)
                random.shuffle(opts)
                st.session_state.options = opts
                st.session_state.options_code = row['Code'] # track which q this is for

            c1, c2, c3 = st.columns(3)
            
            def check_answer(ans):
                if ans == row['Code']:
                    st.session_state.score += 1
                    st.toast(f"Correct! It is {ans}", icon="✅")
                else:
                    st.toast(f"Wrong! It was {row['Code']}", icon="❌")
                
                st.session_state.total += 1
                next_question()
                st.rerun()

            if c1.button(st.session_state.options[0], use_container_width=True): check_answer(st.session_state.options[0])
            if c2.button(st.session_state.options[1], use_container_width=True): check_answer(st.session_state.options[1])
            if c3.button(st.session_state.options[2], use_container_width=True): check_answer(st.session_state.options[2])


# --- Tab 4: Creative Zone ---
with tabs[3]:
    st.header("🎨 Creative Zone")
    
    col_creative_1, col_creative_2 = st.columns([1, 1])
    
    with col_creative_1:
        st.subheader("🕒 Kannada Digital Clock")
        # Javascript based clock to avoid server reloads
        clock_html = """
        <div style="font-family: 'Helvetica', sans-serif; color: #333; padding: 20px; border-radius: 10px; border: 2px solid #eee; text-align: center; background: #fff;">
            <div id="kannada-clock" style="font-size: 3em; font-weight: bold; color: #d63384;"></div>
            <div id="english-clock" style="font-size: 1em; color: #666; margin-top: 5px;"></div>
        </div>
        <script>
        function updateClock() {
            const now = new Date();
            let h = now.getHours();
            let m = now.getMinutes();
            let s = now.getSeconds();
            
            // Pad zero
            h = h < 10 ? '0' + h : h;
            m = m < 10 ? '0' + m : m;
            s = s < 10 ? '0' + s : s;
            
            const timeStr = h + ':' + m + ':' + s;
            
            // Kannada numerals map
            const map = {'0':'೦', '1':'೧', '2':'೨', '3':'೩', '4':'೪', '5':'೫', '6':'೬', '7':'೭', '8':'೮', '9':'೯', ':':':'};
            
            let kTime = '';
            for (let char of timeStr) {
                kTime += map[char] || char;
            }
            
            document.getElementById('kannada-clock').innerText = kTime;
            document.getElementById('english-clock').innerText = now.toDateString();
        }
        setInterval(updateClock, 1000);
        updateClock();
        </script>
        """
        components.html(clock_html, height=200)

    with col_creative_2:
        st.subheader("📜 Kannada Wisdom (Nudimuthu)")
        
        quotes = [
            {"text": "ಕಾಯಕವೇ ಕೈಲಾಸ (Kayakave Kailasa)", "meaning": "Work is Worship", "author": "Basavanna"},
            {"text": "ದೇಶ ಸುತ್ತು ಕೋಶ ಓದು (Desha sutthu, Kosha odhu)", "meaning": "Travel the world, or read the books (to gain wisdom)", "author": "Proverb"},
            {"text": "ಮಾತು ಬೆಳ್ಳಿ, ಮೌನ ಬಂಗಾರ (Maatu belli, Mouna bangara)", "meaning": "Speech is silver, silence is golden", "author": "Proverb"},
            {"text": "ಕುಂಬಾರನಿಗೆ ವರುಷ, ದೊಣ್ಣೆಗೆ ನಿಮಿಷ (Kumbaranige varusha, donnege nimisha)", "meaning": "A potter takes a year to make a pot, a stick takes a minute to break it (Creation is hard, destruction is easy)", "author": "Proverb"},
            {"text": "ಹನಿ ಹನಿ ಕೂಡಿದರೆ ಹಳ್ಳ (Hani hani koodidare halla)", "meaning": "Many drops make a stream (Unity/Savings is strength)", "author": "Proverb"},
             {"text": "ಮಂಕುತಿಮ್ಮನ ಕಗ್ಗ (Mankuthimmana Kagga)", "meaning": "Life is a complex balance...", "author": "D.V. Gundappa"}
        ]
        
        if st.button("✨ Pearl of Wisdom"):
             q = random.choice(quotes)
             
             # Custom Card UI
             card_html = f"""
             <div style="
                background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
                padding: 20px;
                border-radius: 12px;
                border-left: 5px solid #FFC400;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                margin-top: 10px;
                color: #333;
             ">
                <h3 style="margin:0; color: #d63384; font-family: sans-serif;">{q['text']}</h3>
                <p style="margin-top:8px; font-style: italic; color: #555;">"{q['meaning']}"</p>
                <div style="text-align: right; font-weight: bold; color: #888; margin-top: 10px;">- {q['author']}</div>
             </div>
             """
             st.markdown(card_html, unsafe_allow_html=True)
        else:
             st.info("Click above to receive a nugget of wisdom!")

    # Removed Matrix Rain HTML to keep UI clean
# --- Tab 5: Kannada AI Lab (New) ---
# Import the nlp utils (assuming it's in the same folder)
try:
    import nlp_utils
except ImportError:
    st.error("nlp_utils.py not found. Please ensure the file exists.")
    nlp_utils = None

with tabs[4]:
    st.header("🤖 Kannada AI & NLP Lab")
    
    # Sub-tabs for the Lab
    lab_tabs = st.tabs(["🛠️ NLP Toolkit", "🧠 Models (Demo)", "🗣️ Voice & GenAI"])
    
    # --- Lab Tab 1: Toolkit ---
    with lab_tabs[0]:
        st.subheader("Text Preprocessing & Normalization")
        raw_text = st.text_area("Enter Kannada Text:", "ಒಂದಾನೊಂದು ಕಾಲದಲ್ಲಿ...   ರಾಜ  ಇದ್ದನು.", height=100)
        
        c1, c2, c3 = st.columns(3)
        if c1.button("Normalize"):
            if nlp_utils:
                norm_text = nlp_utils.normalize_kannada(raw_text)
                st.code(norm_text)
                st.info("Removed ZWJ/ZWNJ, normalized whitespace and unicode.")
        
        if c2.button("Tokenize"):
             if nlp_utils:
                tokens = nlp_utils.preprocess_text(raw_text)
                st.write(tokens)
                st.caption(f"Count: {len(tokens)}")

        if c3.button("Remove Stopwords"):
             if nlp_utils:
                clean_tokens = nlp_utils.preprocess_text(raw_text, remove_stopwords=True)
                st.write(clean_tokens)
                st.caption("Removed common words like ಮತ್ತು, ಒಂದು, etc.")

        st.divider()
        st.subheader("Text Simplification")
        st.text("Converts formal/complex Kannada to simple spoken Kannada.")
        complex_input = st.text_input("Formal Text:", "ನಾನು ಚಲನಚಿತ್ರ ನೋಡಲು ವಿಮಾನ ನಿಲ್ದಾಣಕ್ಕೆ ಹೋದೆ.")
        if st.button("Simplify Text"):
            if nlp_utils:
                simple_out = nlp_utils.simplify_kannada(complex_input)
                st.success(f"Simple: {simple_out}")

    # --- Lab Tab 2: Models ---
    with lab_tabs[1]:
        col_model_1, col_model_2 = st.columns(2)
        
        with col_model_1:
            st.markdown("### 🏷️ Topic Classification")
            st.caption("Detects if text is Sports, Politics, Cinema, etc.")
            
            cls_text = st.text_area("Text to Classify:", "ವಿರಾಟ್ ಕೊಹ್ಲಿ ಕ್ರಿಕೆಟ್ ಪಂದ್ಯದಲ್ಲಿ ಶತಕ ಬಾರಿಸಿದರು.")
            if st.button("Classify"):
                if nlp_utils:
                    category = nlp_utils.classify_text(cls_text)
                    st.metric("Predicted Topic", category)
                    
        with col_model_2:
            st.markdown("### 😃 Sentiment Analysis")
            st.caption("Detects Positive, Negative, or Neutral sentiment.")
            
            sent_text = st.text_area("Text for Sentiment:", "ಈ ಚಲನಚಿತ್ರ ತುಂಬಾ ಚೆನ್ನಾಗಿದೆ, ನನಗೆ ತುಂಬಾ ಇಷ್ಟವಾಯಿತು.")
            if st.button("Analyze Sentiment"):
                if nlp_utils:
                    label, score = nlp_utils.analyze_sentiment(sent_text)
                    st.metric("Sentiment", label, delta=score)

        st.divider()
        st.markdown("### 🌐 Mock Translation (English ↔ Kannada)")
        trans_input = st.text_input("English Text:", "hello world my name is Anagha")
        if st.button("Translate -> Kannada"):
            if nlp_utils:
                trans_out = nlp_utils.basic_translate_en_kn(trans_input)
                st.markdown(f"**Translation:** `{trans_out}`")
                st.caption("(Note: This is a demo using a simple dictionary lookup, not a full Neural MT model)")

    # --- Lab Tab 3: GenAI & Voice ---
    with lab_tabs[2]:
        # st.info("⚠️ These features are UI Demonstrations...") - Removed
        
        st.markdown("### 💬 Conversational Chatbot")
        with st.chat_message("assistant"):
            st.write("ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ ಕನ್ನಡ ಸಹಾಯಕ. (Hello! I am your Kannada assistant.)")
            
        user_query = st.chat_input("Ask something in Kannada...")
        if user_query:
            with st.chat_message("user"):
                st.write(user_query)
            with st.chat_message("assistant"):
                st.write(f"ನೀವು ಕೇಳಿದ್ದು: '{user_query}'. ಇದು ತುಂಬಾ ಸ್ವಾರಸ್ಯಕರ ಪ್ರಶ್ನೆ! (You asked: ... which is interesting!)")
                st.caption("Simulated Response")
        
        st.divider()
        
        c_gen_1, c_gen_2 = st.columns(2)
        
        with c_gen_1:
            st.markdown("### 🎙️ Voice Input (STT)")
            audio = st.file_uploader("Upload Audio (wav/mp3)", type=['wav', 'mp3'])
            if audio:
                st.audio(audio)
                st.success("Audio received. Transcribing... (Mock)")
                st.code("ನಾನು ಮನೆಗೆ ಹೋಗುತ್ತಿದ್ದೇನೆ...", language="text")
                
        with c_gen_2:
             st.markdown("### 📝 Content Gen")
             prompt = st.text_input("Topic:", "ಬೆಂಗಳೂರು (Bangalore)")
             if st.button("Generate Story"):
                 if nlp_utils:
                     story = nlp_utils.generate_story_start(prompt)
                     st.write(story)
                     
    # --- Eval Section ---
    st.divider()
    with st.expander("📊 Model Evaluation & Metrics"):
        st.write("Confusion Matrix for Classification Model (Mock Data)")
        import numpy as np
        conf_matrix = np.random.rand(5, 5)
        
        c_eval_1, c_eval_2 = st.columns([1, 2])
        with c_eval_1:
             fig_eval, ax_eval = plt.subplots(figsize=(4, 4)) # Smaller size
             im = ax_eval.imshow(conf_matrix, cmap='Blues')
             ax_eval.set_title("Confusion Matrix")
             ax_eval.axis('off')
             st.pyplot(fig_eval)
