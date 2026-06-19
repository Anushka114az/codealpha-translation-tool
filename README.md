# Project 1: Language Translation Tool (CodeAlpha AI Internship)

A multilingual translation web application featuring language auto-detection, translation to over 100+ target languages, a clean dual-pane responsive UI, and high-quality Text-to-Speech (TTS) synthesis.

## Features

* **Dual-Pane Interface**: Side-by-side design mimicking professional tools like Google Translate or DeepL.
* **Auto-Language Detection**: Automatically detects the input language from text patterns.
* **Multilingual Translation**: Seamless translation across 100+ languages using `deep-translator`.
* **Integrated Text-to-Speech (TTS)**: Converts the translated text into speech using Google Text-to-Speech (`gTTS`).
* **Easy Clipboard Copy**: Provides standard code block with a one-click copy button.
* **Premium Dark Theme**: Glassmorphic UI with vibrant modern colors.

---

## Folder Structure

```
project1_translation_tool/
├── app.py                     # Main Streamlit application
├── requirements.txt           # Python dependencies
├── README.md                  # Project instructions & details
└── docs/
    └── report.md              # Project report, Viva QA, LinkedIn/Resume templates
```

---

## Technical Stack

* **Language**: Python 3.8+
* **Framework**: Streamlit
* **Translation**: Deep Translator (Google Translate API)
* **Speech Synthesis**: gTTS (Google Text-to-Speech)

---

## Installation & Setup

### 1. Clone or Navigate to the Directory
```bash
cd project1_translation_tool
```

### 2. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app.py
```

Open https://github.com/Anushka114az/codealpha-translation-tool.git in your browser.
