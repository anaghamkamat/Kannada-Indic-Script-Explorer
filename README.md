
# 🏹 Kannada & Indic Script Explorer

A comprehensive interactive dashboard to explore the history, art, and computational aspects of the **Kannada script** and other Indic writing systems. Built with **Python** and **Streamlit**.

## 🌟 Features

### 1. 📊 Data Analysis
- **Timeline Visualization**: Interactively explore when various Indic scripts (Kannada, Telugu, Devanagari, etc.) were standardized in ISO 15924.
- **Highlighted Insights**: Visual emphasis on the Kannada script's timeline entry.

### 2. 🔡 Transliteration
- **English to Kannada**: Type phonetically in English (e.g., "namaskara") and get the corresponding Kannada script output instantly.
- **Rule-Based Engine**: Uses a custom mapping logic for vowels, consonants, and matras.

### 3. 🎮 Gamified Learning (Quiz)
- **Script Quiz**: Test your knowledge by identifying script codes (e.g., 'Knda', 'Deva').
- **Customizable**: Choose the number of questions via the Sidebar.
- **Scoring System**: Tracks your score and celebrates completion.

### 4. 🎨 Creative Zone
- **Kannada Digital Clock**: A live clock display using Kannada numerals (೦-೯).
- **Wisdom Generator**: Get random "Nuggets of Wisdom" (Vachanas/Proverbs) displayed in beautiful UI cards.

### 5. 🤖 Kannada AI & NLP Lab
A dedicated section for Computational Linguistics experiments:
- **NLP Toolkit**: Normalization, Tokenization, and Text Simplification tools.
- **Classification Demo**: Categorize text into Sports, Politics, etc.
- **Sentiment Analysis**: Detect positive/negative sentiment in Kannada text.
- **Mock GenAI**: UI demonstrations for Chatbots, Voice Input, and Translation.

## 🛠️ Installation

1. **Clone/Download** this repository.
2. Ensure you have **Python 3.8+** installed.
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

*(Note: `requirements.txt` should include `streamlit`, `pandas`, `matplotlib`)*

## 🚀 Usage

Run the application using Streamlit:

```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`.

## 📂 Project Structure

- `app.py`: Main application entry point containing the UI and logic.
- `nlp_utils.py`: Helper library for NLP tasks (normalization, sentiment, etc.).
- `df_iso15924_scripts.tsv`: Dataset containing ISO script codes and dates.
- `kannada_matrix.py`: (Legacy) Script for matrix rain effect.
- `transliterate.py`: Standalone script for transliteration logic.

## 🤝 Credits

Developed with ❤️ using the Streamlit framework. 
*Data Source: ISO 15924 Registration Authority.*
