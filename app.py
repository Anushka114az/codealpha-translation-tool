import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
from io import BytesIO
import traceback

# Page configuration
st.set_page_config(
    page_title="Universal Translator - CodeAlpha",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Premium Glassmorphism & Gradient Theme)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .main {
        background-color: #0f111a;
        color: #ffffff;
    }
    
    /* Title Styling */
    .title-gradient {
        background: linear-gradient(135deg, #00C6FF 0%, #0072FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    
    .subtitle {
        color: #a0aec0;
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 2.5rem;
    }
    
    /* Card / Container Styling */
    .translation-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
    }
    
    /* Button Hover Effects */
    .stButton>button {
        background: linear-gradient(135deg, #00C6FF 0%, #0072FF 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0, 114, 255, 0.4) !important;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 114, 255, 0.6) !important;
    }
    
    /* Custom Footer */
    .footer {
        text-align: center;
        margin-top: 4rem;
        color: #718096;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# App header
st.markdown("<h1 class='title-gradient'>🌐 Multilingual Translator Pro</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>A premium language translation tool with Auto-Detection & Speech Synthesis</p>", unsafe_allow_html=True)

# Fetch available languages
@st.cache_data
def get_languages():
    try:
        # Get language dictionary from deep-translator
        langs = GoogleTranslator().get_supported_languages(as_dict=True)
        # Sort languages alphabetically by name
        sorted_langs = dict(sorted(langs.items()))
        return sorted_langs
    except Exception as e:
        # Fallback dictionary if network call fails
        return {
            "english": "en",
            "spanish": "es",
            "french": "fr",
            "german": "de",
            "italian": "it",
            "portuguese": "pt",
            "russian": "ru",
            "chinese (simplified)": "zh-CN",
            "japanese": "ja",
            "korean": "ko",
            "hindi": "hi",
            "arabic": "ar"
        }

languages_dict = get_languages()
language_names = list(languages_dict.keys())

# Create a list for source languages (with auto-detect)
source_options = ["Auto Detect"] + [name.title() for name in language_names]
target_options = [name.title() for name in language_names]

# Main UI container
st.markdown("<div class='translation-card'>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Source Document")
    src_lang_name = st.selectbox("Select Source Language", source_options, index=0)
    source_text = st.text_area(
        "Enter text to translate...", 
        height=220, 
        placeholder="Type something here, e.g., 'Hello, welcome to my translation application!'"
    )

with col2:
    st.subheader("Translation Output")
    # Default to Spanish (if index is available) or English
    default_target_idx = target_options.index("Spanish") if "Spanish" in target_options else 0
    tgt_lang_name = st.selectbox("Select Target Language", target_options, index=default_target_idx)
    
    # Placeholder for output
    translated_text_box = st.empty()
    translated_text_box.text_area("Translation will appear here...", height=220, disabled=True, value="")

st.markdown("</div>", unsafe_allow_html=True)

# Translation logic
if st.button("Translate Text"):
    if not source_text.strip():
        st.warning("⚠️ Please enter some text to translate.")
    else:
        with st.spinner("Translating..."):
            try:
                # Map selectboxes to code
                target_code = languages_dict[tgt_lang_name.lower()]
                
                if src_lang_name == "Auto Detect":
                    # Initialize translator with auto detection
                    translator = GoogleTranslator(source='auto', target=target_code)
                else:
                    source_code = languages_dict[src_lang_name.lower()]
                    translator = GoogleTranslator(source=source_code, target=target_code)
                
                # Perform translation
                translated_result = translator.translate(source_text)
                
                # Display output in text area and save to session state for TTS/copying
                st.session_state["translated_text"] = translated_result
                st.session_state["target_code"] = target_code
                
                # Append to translation history
                if "history" not in st.session_state:
                    st.session_state["history"] = []
                # Avoid inserting duplicates back-to-back
                if not st.session_state["history"] or st.session_state["history"][0]["source"] != source_text or st.session_state["history"][0]["tgt_lang"] != tgt_lang_name:
                    st.session_state["history"].insert(0, {
                        "source": source_text,
                        "target": translated_result,
                        "src_lang": src_lang_name,
                        "tgt_lang": tgt_lang_name
                    })
                
            except Exception as e:
                st.error(f"❌ Translation failed. Error: {str(e)}")
                traceback.print_exc()

# If translation exists in session state, render output area and options
if "translated_text" in st.session_state:
    translated_text = st.session_state["translated_text"]
    target_code = st.session_state["target_code"]
    
    # Redraw the translated text box with the result
    with col2:
        translated_text_box.text_area("Translated Text", height=220, value=translated_text, key="res_text")
        
        # Display as a code block for easy copying
        st.caption("📋 Copy Text (click the icon in the top right of the box below):")
        st.code(translated_text, language="")
    
    # Text-to-Speech section
    st.markdown("<div class='translation-card'>", unsafe_allow_html=True)
    st.write("### 🔊 Audio Synthesis (Text-to-Speech)")
    
    # gTTS execution
    with st.spinner("Generating audio..."):
        try:
            # Generate speech audio
            tts = gTTS(text=translated_text, lang=target_code, slow=False)
            fp = BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            st.audio(fp, format="audio/mp3")
            st.success("✅ Audio generated successfully!")
        except Exception as e:
            st.info("ℹ️ Text-to-speech is not supported or failed for this language code. Playback is unavailable.")
            # st.error(str(e)) # keep UI clean
            
    st.markdown("</div>", unsafe_allow_html=True)

# Sidebar for History
with st.sidebar:
    st.markdown("<h2 style='color:#00C6FF; text-align:center;'>📜 Translation History</h2>", unsafe_allow_html=True)
    st.write("---")
    
    if "history" not in st.session_state:
        st.session_state["history"] = []
        
    if st.button("Clear History", key="clear_hist_btn"):
        st.session_state["history"] = []
        st.rerun()
        
    if len(st.session_state["history"]) == 0:
        st.info("No translations yet.")
    else:
        for idx, entry in enumerate(st.session_state["history"]):
            with st.expander(f"🔄 {entry['src_lang']} ➔ {entry['tgt_lang']}", expanded=(idx == 0)):
                st.markdown(f"**Original:**\n`{entry['source']}`")
                st.markdown(f"**Translation:**\n`{entry['target']}`")

# Footer
st.markdown("""
<div class='footer'>
    <p>AI Internship Project | Developed for CodeAlpha | © 2026</p>
</div>
""", unsafe_allow_html=True)
