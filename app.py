
import streamlit as st
import pandas as pd
import random
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import streamlit.components.v1 as components
import analyze_scripts
import nlp_utils
from gtts import gTTS
from io import BytesIO

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

st.set_page_config(page_title="Kannada Script Dashboard", layout="wide", page_icon="🏹")

# --- Custom CSS for Premium UI ---
st.markdown("""
<style>
    /* Main App Background - Royal Dark Theme (Deep Maroon/Sandalwood) */
    .stApp {
        /* Handled by config.toml but we can add texture here if needed */
    }
    
    /* Header Transparent */
    .stApp > header {
        background: transparent;
    }
    .main .block-container {
        padding-top: 2rem;
    }

    /* Tabs Container */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        padding-bottom: 2px;
    }

    /* Individual Tab Styling - Dark Royal Look */
    .stTabs [data-baseweb="tab"] {
        border-radius: 4px;
        padding: 8px 20px;
        background-color: #2d0808; /* Darker red-brown */
        border: 1px solid #5c1818;
        color: #ddd;
        font-weight: 500;
        transition: all 0.3s ease;
    }

    /* Tab Hover Effect (Gold Border) */
    .stTabs [data-baseweb="tab"]:hover {
        border-color: #FFD700; 
        color: #FFD700; /* Gold */
        background-color: #3b0e0e;
    }

    /* Selected Tab (Karnataka Red Background with Gold Text) */
    .stTabs [aria-selected="true"] {
        background-color: #D32F2F !important; /* Bright Karnataka Red */
        color: #FFD700 !important; /* Gold Text */
        border: 1px solid #FFD700;
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.2);
    }

    /* Button Styling */
    .stButton > button {
        border-radius: 6px;
        font-weight: 600;
        border: 1px solid #FFD700; /* Gold Border */
        background-color: transparent;
        color: #FFD700;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        background-color: #FFD700;
        color: #1a0404; /* Dark text on Gold bg */
        border-color: #FFD700;
        box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4);
    }

    /* Headings Typography */
    h1, h2, h3 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #FFD700 !important; /* Force Gold for headers */
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    /* Metric Values */
    [data-testid="stMetricValue"] {
        color: #FFD700 !important;
    }
    
    /* Custom divider line with Karnataka Colors */
    hr {
        border-top: 2px solid #FFD700; /* Gold */
        border-bottom: 2px solid #D32F2F; /* Red */
        border-left: none;
        border-right: none;
        height: 4px;
        background: transparent;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Info/Success Boxes Customization */
    .stAlert {
        background-color: #2d0808;
        color: #ddd;
        border: 1px solid #5c1818;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Info
with st.sidebar:
    st.title("🏹 Script Explorer")
    st.info("**Kannada** is one of the oldest Dravidian languages with a rich literary history.")
    st.write("---")
    st.markdown("### **ಸಿರಿಗನ್ನಡಂ ಗೆಲ್ಗೆ, ಸಿರಿಗನ್ನಡಂ ಬಾಳ್ಗೆ!** 💛❤️")
    st.caption("_May rich Kannada triumph, May rich Kannada live long!_")

st.title("🏹 Kannada & Indic Script Explorer")
st.markdown("#### Explore the **history**, **art**, and **utility** of the Kannada script.")

tabs = st.tabs(["🔬 Research", "🔡 Transliterate", "🎨 Creative", "🤖 AI & NLP Analytics"])


# --- Tab 1: Research Lab ---
with tabs[0]:
    st.header("🔬 Deep Research & Analysis")
    
    res_tabs = st.tabs(["📜 Script Evolution", "🧩 Morphological Analysis", "🎼 Chandassu (Meter)", "⚔️ Script Similarity"])
    
    # Subtab 1: Evolution
    with res_tabs[0]:
        st.subheader("Evolution of Indic Scripts")
        df = load_data()
        
        if df is not None:
            # 1. Growth Chart
            growth_df = analyze_scripts.get_indic_script_growth(df)
            
            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown("#### 📈 Digital Adoption (ISO Registration)")
                st.line_chart(growth_df, x='Date', y='Cumulative Count', color='#FF4B4B')
                st.caption("Cumulative growth of Indic scripts recognized in Unicode/ISO standards.")
                
            with c2:
                st.markdown("#### 🗓️ Latency Analysis")
                latency_df = analyze_scripts.compare_kannada_latency(df)
                if latency_df is not None:
                     # Filter for display
                     st.dataframe(latency_df[['English Name', 'Days Difference']].set_index('English Name'), height=300)
                     st.caption("Days +/- relative to Kannada's registration.")

            st.divider()
            
            # 2. Original Timeline (Enhanced)
            st.markdown("#### ⏳ Graphical Timeline")
            
            df_indic = df[df['Code'].isin(analyze_scripts.get_indic_scripts_list())].copy()
            df_indic['Date'] = pd.to_datetime(df_indic['Date'])
            df_indic = df_indic.sort_values('Date')
            
            fig, ax = plt.subplots(figsize=(10, 5))
            # Dynamic colors
            colors = ['red' if name == 'Kannada' else 'teal' for name in df_indic['English Name']]
            sizes = [250 if name == 'Kannada' else 100 for name in df_indic['English Name']]
            
            ax.scatter(df_indic['Date'], df_indic['English Name'], color=colors, s=sizes, zorder=3)
            ax.hlines(y=df_indic['English Name'], xmin=df_indic['Date'].min(), xmax=df_indic['Date'], color='skyblue', alpha=0.5, zorder=2)
            
            # Annotate
            k_row = df_indic[df_indic['English Name'] == 'Kannada']
            if not k_row.empty:
                 k_date = k_row.iloc[0]['Date']
                 ax.annotate('Kannada', (k_date, 'Kannada'), xytext=(10, 5), textcoords='offset points', color='red', weight='bold')

            ax.grid(axis='x', linestyle='--', alpha=0.7)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
            fig.autofmt_xdate()
            st.pyplot(fig)

    # Subtab 2: Morphology
    with res_tabs[1]:
        st.subheader("🧩 Morphological Analyzer (Akshara Analysis)")
        st.markdown("Analyze the composition of Kannada text: **Swaras, Vyanjanas, and Ottaksharas**.")
        
        morph_text = st.text_area("Enter Text for Analysis:", "ನಮಸ್ಕಾರ ಕನ್ನಡ", height=70, key="morph_input")
        
        if st.button("Analyze Morphology", key="btn_morph"):
            if hasattr(nlp_utils, 'analyze_morphology'):
                result = nlp_utils.analyze_morphology(morph_text)
                
                # Metrics Row
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Swaras (Vowels)", result['stats']['Swaras'])
                m2.metric("Vyanjanas (Consonants)", result['stats']['Vyanjanas'])
                m3.metric("Ottaksharas (Conjuncts)", result['stats']['Ottaksharas'])
                m4.metric("Total Aksharas", len(result['aksharas']))
                
                st.divider()
                st.markdown("#### 🔍 Akshara Breakdown")
                st.warning(" | ".join(result['aksharas']))
                
                # Visual Distribution
                st.markdown("#### 📊 Component Distribution")
                stats_data = result['stats']
                # Remove 0s for chart
                clean_stats = {k:v for k,v in stats_data.items() if v > 0}
                if clean_stats:
                    st.bar_chart(clean_stats)
                    
            if st.button("🔊 Play Original Text", key="tts_morph"):
                 try:
                    tts = gTTS(text=morph_text, lang='kn')
                    audio_bytes = BytesIO()
                    tts.write_to_fp(audio_bytes)
                    st.audio(audio_bytes, format='audio/mp3')
                 except Exception as e:
                    # Fallback or error
                    st.warning("Could not generate audio (Check internet/libraries).")
            else:
                st.error("nlp_utils.analyze_morphology not found. Please reload.")
                
    # Subtab 3: Chandassu
    with res_tabs[2]:
        st.subheader("🎼 Chandassu (Prosody Calculator)")
        st.markdown("Calculate the **Laghu (Light)** and **Guru (Heavy)** meter of a poetic line.")
        
        chand_text = st.text_input("Enter Line of Poetry:", "ಮಂಕುತಿಮ್ಮನ ಕಗ್ಗ", key="chand_input")
        
        if st.button("Calculate Meter", key="btn_chand"):
            if hasattr(nlp_utils, 'get_chandassu_meter'):
                # 1. Get meter
                meter = nlp_utils.get_chandassu_meter(chand_text)
                # 2. Get aksharas for alignment
                aksharas = nlp_utils.analyze_morphology(chand_text)['aksharas']
                
                st.divider()
                st.markdown("#### Result")
                
                # Create a specialized display
                # Need to zip Akshara with Meter Symbol
                
                html_out = "<div style='display: flex; gap: 10px; overflow-x: auto; padding-bottom: 10px;'>"
                
                for aksh, sym in zip(aksharas, meter):
                    color = "#FFC400" if sym == "-" else "#00d4ff" # Yellow for Guru, Blue for Laghu
                    label = "GURU" if sym == "-" else "LAGHU"
                    
                    html_out += f"""
                    <div style="text-align: center; border: 1px solid #333; padding: 10px; border-radius: 8px; min_width: 50px; background: #0e1117;">
                        <div style="font-size: 20px; font-weight: bold; color: {color};">{sym}</div>
                        <div style="font-size: 10px; color: #888;">{label}</div>
                        <div style="font-size: 18px; margin-top: 5px;">{aksh}</div>
                    </div>
                    """
                html_out += "</div>"
                
                st.markdown(html_out, unsafe_allow_html=True)
                
                # Count
                g_count = meter.count("-")
                l_count = meter.count("U")
                st.caption(f"Total: {len(meter)} | Guru (-): {g_count} | Laghu (U): {l_count}")

    # Subtab 4: Similarity
    with res_tabs[3]:
        st.subheader("⚔️ Script Similarity Index (Kannada vs Telugu)")
        st.markdown("Kannada and Telugu scripts are extremely similar. This tool compares them.")
        
        c_sim_1, c_sim_2 = st.columns(2)
        with c_sim_1:
            kn_sim_text = st.text_area("Kannada Text", "ನಮಸ್ಕಾರ ಕರ್ನಾಟಕ", height=80)
        with c_sim_2:
            # Auto-generate Telugu placeholder or let user type?
            # Let's show the Cognate generation
            st.info("Generating Telugu Cognate automatically...")
            
        if st.button("Compare Scripts"):
            sim_res = nlp_utils.calculate_script_similarity(kn_sim_text, "")
            
            with c_sim_2:
                 st.text_area("Telugu Cognate (Generated)", sim_res['converted'], height=80)
            
            st.metric("Visual Match Score", f"{sim_res['score']*100}%", "High Compatibility")
            st.success("These scripts share a near-identical structure with a unicode offset of 0x80.")

# --- Tab 2: Transliteration ---
with tabs[1]:
    st.header("English -> Kannada Transliteration")
    st.markdown("Type phonetically (e.g., *'kannada'* or *'namaskara'*)")
    
    input_text = st.text_input("Enter text:", "namaskara")
    
    if input_text:
        out = transliterate(input_text)
        st.markdown(f"### Output: `{out}`")
        st.markdown(f"# {out}") # Large display
        
        if st.button("🔊 Play Audio", key="tts_trans"):
            try:
                tts = gTTS(text=out, lang='kn')
                audio_bytes = BytesIO()
                tts.write_to_fp(audio_bytes)
                st.audio(audio_bytes, format='audio/mp3')
            except Exception as e:
                st.error(f"TTS Error: {e}")


# --- Tab 3: Creative Zone ---
with tabs[2]:

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

with tabs[3]:
    st.header("🤖 Kannada AI & NLP Analytics")
    
    # Sub-tabs for the Lab
    lab_tabs = st.tabs(["🛠️ NLP Toolkit", "🧠 Models (Prototype)", "🗣️ Voice & GenAI", "🤖 Vachana Gen"])
    
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

        st.divider()
        st.subheader("🗣️ Phonetic Hashing (Soundex)")
        st.text("Hashes words by sound to find similar pronunciations.")
        sound_input = st.text_input("Word to Hash:", "ಕಾಲೇಜು (College)", key="sound_input")
        if st.button("Generate Hash"):
             h = nlp_utils.kannada_phonetic_hash(sound_input)
             st.metric("Soundex Code", h)
             st.caption(f"Any word returning `{h}` sounds similar to input.")

        st.divider()
        st.subheader("✂️ Rule-Based Stemmer")
        st.text("Removes common suffixes (case markers, plurals).")
        stem_input = st.text_input("Word to Stem:", "ಕನ್ನಡಿಗರು (Kannadigas)", key="stem_input")
        if st.button("Find Root"):
             root = nlp_utils.simple_kannada_stemmer(stem_input)
             st.success(f"Root/Stem: {root}")

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
        st.markdown("### 🌐 Simulated Translation (English ↔ Kannada)")
        trans_input = st.text_input("English Text:", "hello world my name is Anagha")
        if st.button("Translate -> Kannada"):
            if nlp_utils:
                trans_out = nlp_utils.basic_translate_en_kn(trans_input)
                st.markdown(f"**Translation:** `{trans_out}`")
                st.caption("(Note: This uses a deterministic lookup for demonstration purposes.)")

    with lab_tabs[3]:
        st.markdown("### 📜 Markov Chain Vachana Generator")
        st.caption("A simple probabilistic AI that writes new Vachana-style lines based on training data.")
        
        start_word = st.selectbox("Start Word:", ["ನುಡಿದರೆ", "ಇವ", "ದಯವಿಲ್ಲದ", "ಮಾನವ", "ಆಚಾರವಿಲ್ಲದ"])
        gen_len = st.slider("Length (words):", 5, 20, 8)
        
        if st.button("✨ Generate Vachana"):
            if nlp_utils:
                gen_text = nlp_utils.markov_gen.generate(start_word, gen_len)
                st.markdown(f"**Generated:**")
                st.markdown(f"> *{gen_text}*" )
                
                # Audio for fun
                if st.button("🔊 Read Aloud", key="tts_gen"):
                     try:
                        tts = gTTS(text=gen_text, lang='kn')
                        audio_bytes = BytesIO()
                        tts.write_to_fp(audio_bytes)
                        st.audio(audio_bytes, format='audio/mp3')
                     except: pass
            else:
                st.error("Model Loading Failed")

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
                st.success("Audio received. Transcribing... (Simulated)")
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
        st.write("Confusion Matrix for Classification Model (Simulated Data)")
        import numpy as np
        conf_matrix = np.random.rand(5, 5)
        
        c_eval_1, c_eval_2 = st.columns([1, 2])
        with c_eval_1:
             fig_eval, ax_eval = plt.subplots(figsize=(4, 4)) # Smaller size
             im = ax_eval.imshow(conf_matrix, cmap='Blues')
             ax_eval.set_title("Confusion Matrix")
             ax_eval.axis('off')
             st.pyplot(fig_eval)
