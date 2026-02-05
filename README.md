# 🏹 Kannada & Indic Script Explorer

A comprehensive interactive dashboard to explore the history, art, and computational aspects of the **Kannada script** and other Indic writing systems. Built with **Python** and **Streamlit**.

## 🌟 Features

### 1. 📊 Research Lab
- **Script Evolution**: Timelines of Indic script standardization.
- **Morphological Analysis**: Breaks down Kannada words into Aksharas (Swaras/Vyanjanas).
- **Chandassu Calculator**: Analyzes poetic meter (Laghu/Guru).
- **Script Similarity**: Compares Kannada and Telugu structures.

### 2. 🔡 Transliteration
- **English to Kannada**: Type phonetically (e.g., "namaskara").
- **🔊 Text-to-Speech**: Listen to the transliterated output.

### 3. 🎨 Creative Zone
- **Kannada Digital Clock**: Live clock with Kannada numerals.
- **Wisdom Generator**: Random Vachanas/Proverbs.

### 4. 🤖 Kannada AI & NLP Lab
- **🤖 Vachana Generator**: Generates new poetic lines using a Markov Chain model.
- **Toolkit**: Rule-based Stemmer, Normalization, Tokenization.
- **Models**: Topic Classification, Sentiment Analysis.
- **Voice**: Mock Voice Input and Text-to-Speech demo.

## 🛠️ Installation

1. **Clone/Download** this repository.
2. Ensure you have **Python 3.8+** installed.
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

*(Note: `requirements.txt` includes `streamlit`, `pandas`, `gTTS`)*

## 🚀 Usage

Run the application:

```bash
streamlit run app.py
```

## 📂 Project Structure

- `app.py`: Main application UI.
- `nlp_utils.py`: Core logic for NLP, Morphology, and GenAI.
- `analyze_scripts.py`: Data analysis logic.
- `transliterate.py`: Transliteration engine.
- `df_iso15924_scripts.tsv`: ISO Data.

## 🤝 Credits

Developed with ❤️ using Streamlit.
